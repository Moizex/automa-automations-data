import fitz  # PyMuPDF
import re
import csv
import os

# 📁 Caminho da pasta com os PDFs
pasta_pdfs = r'Z:\DECCM NL 2025\04 RELATÓRIO FINAL\PDF\06 JUNHO\Peti'

# 📄 Caminho do arquivo de saída
saida_csv = r'Z:\DECCM NL 2025\04 RELATÓRIO FINAL\PDF\06 JUNHO\Peti\Dados\dados_extraidos.csv'

# Função para extrair os dados do texto do PDF
def extrair_dados(texto):
    dados = {}

    # Número do processo: após "Processo" e termina com .1000
    processo_match = re.search(r'Processo\s+(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', texto)
    dados['numero_processo'] = processo_match.group(1) if processo_match else ''

    # Número do inquérito: após "Número do Inquérito no Executivo" e termina com /2025
    inquerito_match = re.search(r'Número do Inquérito no Executivo\s+(\d+/2025)', texto)
    dados['numero_inquerito'] = inquerito_match.group(1) if inquerito_match else ''

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
                dados['caminho_pdf'] = caminho_pdf  # ✅ adiciona o caminho completo
                todos_os_dados.append(dados)
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

# Escreve os dados em um arquivo CSV
with open(saida_csv, 'w', newline='', encoding='utf-8') as csvfile:
    campos = ['arquivo', 'numero_processo', 'numero_inquerito', 'caminho_pdf']
    writer = csv.DictWriter(csvfile, fieldnames=campos)
    writer.writeheader()
    writer.writerows(todos_os_dados)

print(f'Dados extraídos com sucesso para: {saida_csv}')

#
# import fitz  # PyMuPDF
# import re
# import csv
# import os
#
# # 📁 Caminho da pasta com os PDFs (substitua pelo caminho real no seu computador)
# pasta_pdfs = r'Z:\DECCM NL 2025\04 RELATÓRIO FINAL\PDF\06 JUNHO\Peti'  # <- Altere aqui
#
# # 📄 Caminho do arquivo de saída
# saida_csv = r'Z:\DECCM NL 2025\04 RELATÓRIO FINAL\PDF\06 JUNHO\Peti\Dados\dados_extraidos.csv'
#
#
# # Função para extrair os dados do texto
# def extrair_dados(texto):
#     dados = {}
#
#     # Número do processo: após "Processo" e termina com .1000
#     processo_match = re.search(r'Processo\s+(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', texto)
#     dados['numero_processo'] = processo_match.group(1) if processo_match else ''
#
#     # Número do inquérito: após "Número do Inquérito no Executivo" e termina com /2025
#     inquerito_match = re.search(r'Número do Inquérito no Executivo\s+(\d+/2025)', texto)
#     dados['numero_inquerito'] = inquerito_match.group(1) if inquerito_match else ''
#
#     return dados
#
# # Lista para armazenar todos os dados extraídos
# todos_os_dados = []
#
# # Percorre todos os PDFs na pasta e subpastas
# for raiz, _, arquivos in os.walk(pasta_pdfs):
#     for arquivo in arquivos:
#         if arquivo.lower().endswith('.pdf'):
#             caminho_pdf = os.path.join(raiz, arquivo)
#             try:
#                 doc = fitz.open(caminho_pdf)
#                 texto_completo = ''
#                 for pagina in doc:
#                     texto_completo += pagina.get_text()
#                 doc.close()
#
#                 dados = extrair_dados(texto_completo)
#                 dados['arquivo'] = arquivo
#                 todos_os_dados.append(dados)
#             except Exception as e:
#                 print(f"Erro ao processar {arquivo}: {e}")
#
# # Escreve os dados em um CSV
# with open(saida_csv, 'w', newline='', encoding='utf-8') as csvfile:
#     campos = ['arquivo', 'numero_processo', 'numero_inquerito']
#     writer = csv.DictWriter(csvfile, fieldnames=campos)
#     writer.writeheader()
#     writer.writerows(todos_os_dados)
#
# print(f'Dados extraídos com sucesso para: {saida_csv}')
#
