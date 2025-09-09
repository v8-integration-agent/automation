import subprocess
from pathlib import Path

bdd_file = Path("bdd/scenarios.feature")
output_dir = Path("tests")
output_dir.mkdir(exist_ok=True)

with open(bdd_file, "r", encoding="utf-8") as f:
    bdd = f.read()

prompt = f"""
Você é um engenheiro de testes.
Converta os cenários BDD abaixo em código automatizado Playwright (JavaScript):

{bdd}
"""

result = subprocess.run(
    ["ollama", "run", "mistral"],
    input=prompt.encode("utf-8"),
    capture_output=True
)

output_file = output_dir / "test.spec.js"
with open(output_file, "wb") as f:
    f.write(result.stdout)

print(f"Testes gerados em {output_file}")
