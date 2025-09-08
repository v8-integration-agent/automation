import os, sys, requests, re

OLLAMA = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL  = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct')
PROMPT_SYS = open('ai/prompts/tests_system.txt', 'r', encoding='utf-8').read()

HEADER = """import { test, expect } from '@playwright/test';\n"""

def ollama_convert(gherkin: str) -> str:
    r = requests.post(f"{OLLAMA}/api/generate", json={
        'model': MODEL,
        'prompt': f"{PROMPT_SYS}\n\nFEATURE:\n{gherkin}\n\nSAÍDA:",
        'stream': False
    }, timeout=600)
    r.raise_for_status()
    return r.json()['response']

if __name__ == '__main__':
    src_dir = sys.argv[1] if len(sys.argv) > 1 else 'bdd'
    os.makedirs('tests/ai_generated', exist_ok=True)
    for name in os.listdir(src_dir):
        if not name.endswith('.feature'): continue
        gh = open(os.path.join(src_dir, name), 'r', encoding='utf-8').read()
        ts = ollama_convert(gh)
        # Segurança: garante import básico
        if not ts.strip().startswith('import'): ts = HEADER + ts
        out_name = os.path.splitext(name)[0] + '.spec.ts'
        with open(os.path.join('tests/ai_generated', out_name), 'w', encoding='utf-8') as f:
            f.write(ts)
        print('✔ Test gerado:', out_name)