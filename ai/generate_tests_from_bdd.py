import os
from groq import Groq
 
def generate_tests_from_bdd():
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
    with open("ai/bdd/generated.feature", "r", encoding="utf-8") as f:
        bdd_content = f.read()
 
    prompt = f"""
    Você é um especialista em automação de testes.
    Converta o seguinte arquivo BDD em código de testes automatizados usando Python e pytest-bdd.
 
    BDD:
    {bdd_content}
    """
 
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
 
    tests_code = response.choices[0].message.content
 
    os.makedirs("ai/tests", exist_ok=True)
    with open("ai/tests/test_generated.py", "w", encoding="utf-8") as f:
        f.write(tests_code)
 
 
if __name__ == "__main__":
    generate_tests_from_bdd()
 