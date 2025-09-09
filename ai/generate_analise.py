import os
from groq import Groq

def analyze_playwright_logs(logs_dir="test-results/**/error-context.md"):
    """
    Lê automaticamente todos os arquivos de log do Playwright em uma pasta e
    usa a IA para analisar falhas e sugerir correções.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Cria pasta para salvar análises
    os.makedirs("ai/analysis", exist_ok=True)

    generated = False  # flag para saber se gerou arquivos

    # Varre todos os arquivos na pasta de logs
    for root, _, files in os.walk(logs_dir):
        for file in files:
            if file.endswith((".txt", ".log", ".json", ".md")):
                log_path = os.path.join(root, file)
                with open(log_path, "r", encoding="utf-8") as f:
                    log_content = f.read()

                prompt = f"""
                Você é um especialista em testes automatizados com Playwright.
                Analise o log abaixo e explique de forma clara e detalhada:
                1. Quais testes falharam.
                2. O motivo de cada falha.
                3. Sugestões de como corrigir os erros.

                Log do Playwright:
                {log_content}
                """

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": prompt}]
                )

                analysis = response.choices[0].message.content

                # Salva a análise com o mesmo nome do log
                analysis_filename = os.path.splitext(file)[0] + "_analysis.txt"
                output_file = os.path.join("ai/analysis", analysis_filename)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(analysis)

                print(f"Análise do log '{file}' salva em: {output_file}")
                generated = True

    # Se não gerar nenhum arquivo, cria um placeholder
    if not generated:
        placeholder = os.path.join("ai/analysis", "no_logs_analysis.txt")
        with open(placeholder, "w", encoding="utf-8") as f:
            f.write("Nenhum log encontrado para análise.")
        print(f"Nenhum log encontrado. Placeholder criado em: {placeholder}")


if __name__ == "__main__":
    analyze_playwright_logs()
