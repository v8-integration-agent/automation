import requests

def get_criterios_de_aceite():
    with open('requirements/criterios.md', 'r') as file:
        return file.read()

def send_to_groq(criterios):
    # Supondo que temos uma API do GROQ
    response = requests.post("https://api.groq.com/generate_bdd", data={"criterios": criterios})
    return response.json()

def save_bdds(bdds):
    with open('ai/bdd/prompts/generated_bdds.txt', 'w') as file:
        for bdd in bdds:
            file.write(bdd + '\n')

criterios = get_criterios_de_aceite()
bdds = send_to_groq(criterios)
save_bdds(bdds)
print("BDDs gerados e salvos com sucesso.")