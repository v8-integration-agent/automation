import subprocess
import sys
from pathlib import Path

criterios_file = Path(requirements/criterios.md)
output_dir = Path("bdd")
output_dir.mkdir(exist_ok=True)

with open(criterios_file, "r", encoding="utf-8") as f:
    criterios = f.read()

prompt = f"""
Você é um especialista em QA.
Com base nos critérios de aceite abaixo, gere cenários de BDD em formato Gherkin (.feature):

{criterios}
"""

result = subprocess.run(
    ["ollama", "run", "mistral"],
    input=prompt.encode("utf-8"),
    capture_output=True
)

output_file = output_dir / "scenarios.feature"
with open(output_file, "wb") as f:
    f.write(result.stdout)

print(f"BDD gerado em {output_file}")
