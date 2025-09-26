import os
from groq import Groq
 
def generate_tests_from_bdd():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
    with open("ai/bdd/generated.feature", "r", encoding="utf-8") as f:
        bdd_content = f.read()
 
    prompt = f"""
  Você é um especialista em automação de testes utilizando Playwright.

Converta o seguinte arquivo BDD (Gherkin) em código de teste automatizado funcional, incluindo:

Estrutura de testes com Playwright e TypeScript/JavaScript.

Definição clara de cenários, passos e seletores.

Boas práticas de automação (esperas, organização de código, tratamento de erros).

Comentários explicativos sobre cada passo do teste.

Forneça o código completo pronto para execução no Playwright Test Runner.

    BDD:
    {bdd_content}
    """
 
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
 
    tests_code = response.choices[0].message.content
 
    os.makedirs("ai/tests", exist_ok=True)
    with open("ai/tests/test_generated.ts", "w", encoding="utf-8") as f:
        f.write(tests_code)
 
 
if __name__ == "__main__":
    generate_tests_from_bdd()
 