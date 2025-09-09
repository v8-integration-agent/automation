import requests

def get_bdds():
    with open('ai/bdd/prompts/generated_bdds.txt', 'r') as file:
        return file.readlines()

def send_bdd_to_groq(bdd):
    # Supondo que temos uma API do GROQ
    response = requests.post("https://api.groq.com/generate_tests", data={"bdd": bdd})
    return response.json()

def save_tests(tests):
    with open('ai/tests/generated_tests.py', 'w') as file:
        for test in tests:
            file.write(test + '\n')

bdds = get_bdds()
all_tests = []
for bdd in bdds:
    tests = send_bdd_to_groq(bdd)
    all_tests.extend(tests)

save_tests(all_tests)
print("Testes gerados e salvos com sucesso.")