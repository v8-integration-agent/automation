import os, json, requests

OLLAMA = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL  = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct')
SYS    = open('ai/prompts/failure_analyst_system.txt', 'r', encoding='utf-8').read()

REPORT = 'report.json'
OUTDIR = 'ai/analysis'

os.makedirs(OUTDIR, exist_ok=True)

if not os.path.exists(REPORT):
    open(os.path.join(OUTDIR, 'summary.md'), 'w').write('# Sem report.json\n')
    raise SystemExit(0)

report = json.load(open(REPORT, 'r', encoding='utf-8'))

failures = []
for suite in report.get('suites', []):
    for spec in suite.get('specs', []):
        for test in spec.get('tests', []):
            for r in test.get('results', []):
                if r.get('status') == 'failed':
                    err = (r.get('error', {}) or {}).get('stack', '')
                    att = r.get('attachments', [])
                    shots = [a.get('path') for a in att if a.get('name','').startswith('screenshot')]
                    traces = [a.get('path') for a in att if 'trace' in (a.get('name',''))]
                    failures.append({
                        'title': test.get('title',''),
                        'file': spec.get('file',''),
                        'error': err,
                        'screenshots': shots,
                        'traces': traces,
                    })

if not failures:
    open(os.path.join(OUTDIR, 'summary.md'), 'w', encoding='utf-8').write('✅ Todos os testes passaram.')
    raise SystemExit(0)

context = json.dumps({'failures': failures}, ensure_ascii=False, indent=2)

resp = requests.post(f"{OLLAMA}/api/generate", json={
    'model': MODEL,
    'prompt': f"{SYS}\n\nREPORT CONTEXTO:\n{context}\n\nSAÍDA:",
    'stream': False
}, timeout=600)
resp.raise_for_status()
summary = resp.json()['response']

with open(os.path.join(OUTDIR, 'summary.md'), 'w', encoding='utf-8') as f:
    f.write(summary)

print('✔ Análise gerada em ai/analysis/summary.md')