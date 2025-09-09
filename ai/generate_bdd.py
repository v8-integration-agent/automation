import os
from groq import Groq
 
def generate_bdd_from_criteria():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
    with open("ai/requirements/criterios.md", "r", encoding="utf-8") as f:
        criterios = f.read()
 
    prompt = f"""
    Você é um especialista em BDD.
    Com base nos seguintes critérios de aceite, gere cenários no formato Gherkin (Given, When, Then).
 
    Critérios:
    {criterios}
    """
 
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
 
    bdd = response.choices[0].message.content
 
    os.makedirs("ai/bdd", exist_ok=True)
    with open("ai/bdd/generated.feature", "w", encoding="utf-8") as f:
        f.write(bdd)
 
if __name__ == "__main__":
    generate_bdd_from_criteria()