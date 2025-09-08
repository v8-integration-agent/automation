import os, sys, json, requests
from docx import Document
from markdown_it import MarkdownIt

OLLAMA = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL  = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct')

PROMPT_SYS = open('ai/prompts/bdd_system.txt', 'r', encoding='utf-8').read()

def load_text(path: str) -> str:
    if path.lower().endswith('.docx'):
        doc = Document(path)
        return '\n'.join(p.text for p in doc.paragraphs)
    if path.lower().endswith('.md'):
        return open(path, 'r', encoding='utf-8').read()
    # .doc simples (se convertido previamente para .docx)
    return open(path, 'r', encoding='utf-8', errors='ignore').read()

def ollama(prompt: str) -> str:
    r = requests.post(f"{OLLAMA}/api/generate", json={
        'model': MODEL,
        'prompt': f"{PROMPT_SYS}\n\nREQUISITOS:\n{prompt}\n\nSAÍDA:",
        'stream': False
    }, timeout=600)
    r.raise_for_status()
    return r.json()['response']

if __name__ == '__main__':
    src_dir = sys.argv[1] if len(sys.argv) > 1 else 'requirements'
    os.makedirs('bdd', exist_ok=True)
    for name in os.listdir(src_dir):
        if not name.lower().endswith(('.docx', '.md', '.txt')):
            continue
        raw = load_text(os.path.join(src_dir, name))
        out = ollama(raw)
        feat_name = os.path.splitext(name)[0].lower().replace(' ', '_') + '.feature'
        with open(os.path.join('bdd', feat_name), 'w', encoding='utf-8') as f:
            f.write(out)
        print('✔ BDD gerado:', feat_name)