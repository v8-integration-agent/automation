import os
import glob
from groq import Groq

def analyze_playwright_logs(logs_dir="test-results"):
    """
    Lê automaticamente todos os arquivos de log do Playwright em uma pasta e
    usa a IA para analisar falhas e sugerir correções.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Cria pasta para salvar análises
    os.makedirs("ai/analysis", exist_ok=True)

    generated = False  # flag para saber se gerou arquivos

    # Busca todos os arquivos dentro de test-results
    log_files = glob.glob(os.path.join(logs_dir, "**/*"), recursive=True)

    for log_path in log_files:
        if log_path.endswith((".txt", ".log", ".json", ".md")):
            with open(log_path, "r", encoding="utf-8") as f:
                log_content = f.read()

            if not log_content.strip():
                continue  # pula arquivos vazios

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
            filename = os.path.splitext(os.path.basename(log_path))[0] + "_analysis.txt"
            output_file = os.path.join("ai/analysis", filename)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(analysis)

            print(f"Análise do log '{log_path}' salva em: {output_file}")
            generated = True

    # Se não gerar nenhum arquivo, cria um placeholder
    if not generated:
        placeholder = os.path.join("ai/analysis", "no_logs_analysis.txt")
        with open(placeholder, "w", encoding="utf-8") as f:
            f.write("Nenhum log encontrado para análise.")
        print(f"Nenhum log encontrado. Placeholder criado em: {placeholder}")


if __name__ == "__main__":
    analyze_playwright_logs()
