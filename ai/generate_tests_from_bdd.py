# ai/generate_tests_from_bdd.py
from groq import GroqClient
import os

client = GroqClient(os.environ.get("API_GROQ"))

def generate_test_code(feature_text):
    prompt = f"""
    Gere código de teste automatizado (Playwright em JS) baseado no seguinte BDD:
    {feature_text}
    """
    response = client.generate(prompt)
    return response.text

if __name__ == "__main__":
    bdd_folder = "bdd"
    tests_folder = "tests"
    os.makedirs(tests_folder, exist_ok=True)

    for file in os.listdir(bdd_folder):
        if file.endswith(".feature"):
            with open(os.path.join(bdd_folder, file), "r") as f:
                feature_text = f.read()
            test_code = generate_test_code(feature_text)
            with open(os.path.join(tests_folder, file.replace(".feature", ".spec.js")), "w") as f:
                f.write(test_code)
