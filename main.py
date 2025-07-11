import fitz  # PyMuPDF
import re
import csv
import os

# 📁 Caminho da pasta com os PDFs
pasta_pdfs = r'Z:\DECCM NL 2025\04 RELATORIO FINAL\PDF\07 JULHO\Peti'

# 📄 Caminho do arquivo de saída
saida_csv = r'Z:\DECCM NL 2025\04 RELATORIO FINAL\PDF\07 JULHO\Peti\Dados\dados_extraidos.csv'

# Garante que a pasta de saída exista
os.makedirs(os.path.dirname(saida_csv), exist_ok=True)

# Função para extrair os dados do texto do PDF
def extrair_dados(texto):
    dados = {}

    # Número do processo
    processo_match = re.search(r'Processo\s+(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', texto)
    dados['numero_processo'] = processo_match.group(1) if processo_match else ''

    # Número do inquérito
    inquerito_match = re.search(r'Número do Inquérito no Executivo\s+(\d+/2025)', texto)
    dados['numero_inquerito'] = inquerito_match.group(1) if inquerito_match else ''

    # Data e hora do cadastro
    data_cadastro_match = re.search(r'Data do Cadastro\s+(\d{2}/\d{2}/\d{4})\s+às\s+(\d{2}:\d{2}:\d{2})', texto)
    if data_cadastro_match:
        dados['data_cadastro'] = data_cadastro_match.group(1)
        dados['hora_cadastro'] = data_cadastro_match.group(2)
    else:
        dados['data_cadastro'] = ''
        dados['hora_cadastro'] = ''

    return dados

# Lista para armazenar todos os dados extraídos
todos_os_dados = []

# Percorre todos os PDFs na pasta e subpastas
for raiz, _, arquivos in os.walk(pasta_pdfs):
    for arquivo in arquivos:
        if arquivo.lower().endswith('.pdf'):
            caminho_pdf = os.path.join(raiz, arquivo)
            try:
                doc = fitz.open(caminho_pdf)
                texto_completo = ''
                for pagina in doc:
                    texto_completo += pagina.get_text()
                doc.close()

                dados = extrair_dados(texto_completo)
                dados['arquivo'] = arquivo
                dados['caminho_pdf'] = caminho_pdf
                todos_os_dados.append(dados)
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

# Escreve os dados em um arquivo CSV
with open(saida_csv, 'w', newline='', encoding='utf-8') as csvfile:
    campos = [
        'arquivo',
        'numero_processo',
        'numero_inquerito',
        'data_cadastro',
        'hora_cadastro',
        'caminho_pdf'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=campos)
    writer.writeheader()
    writer.writerows(todos_os_dados)

print(f'Dados extraídos com sucesso para: {saida_csv}')
