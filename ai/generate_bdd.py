# ai/generate_bdd.py
from groq import GroqClient

client = GroqClient(os.environ.get("API_GROQ"))

def generate_bdd(file_path):
    with open(file_path, "r") as f:
        criteria = f.read()

    prompt = f"""
    Transforme os seguintes critérios de aceite em cenários BDD no padrão Gherkin:
    {criteria}
    """

    response = client.generate(prompt)
    return response.text

if __name__ == "__main__":
    import sys
    import os

    requirements_folder = sys.argv[1]  # ex: 'requirements'
    bdd_folder = "bdd"
    os.makedirs(bdd_folder, exist_ok=True)

    for filename in os.listdir(requirements_folder):
        if filename.endswith(".md"):
            output = generate_bdd(os.path.join(requirements_folder, filename))
            with open(os.path.join(bdd_folder, filename.replace(".md", ".feature")), "w") as f:
                f.write(output)
