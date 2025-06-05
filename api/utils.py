import os
import csv
from collections import defaultdict

# A pasta onde este arquivo .py está localizado
BASE_DIR = os.path.dirname(__file__)

# Caminho completo do CSV. Em ambientes como o Vercel, o arquivo pode ficar em
# um diretório diferente dependendo de como a função foi empacotada. Primeiro
# tenta-se ler no mesmo diretório deste arquivo; caso não exista, procura dentro
# de um subdiretório "api" (mantém compatibilidade com execuções locais e em
# serverless).
CSV_PATH = os.path.join(BASE_DIR, "dados_futebol.csv")
if not os.path.exists(CSV_PATH):
    alt_path = os.path.join(BASE_DIR, "api", "dados_futebol.csv")
    if os.path.exists(alt_path):
        CSV_PATH = alt_path
    else:
        raise FileNotFoundError(f"dados_futebol.csv não encontrado em {CSV_PATH} ou {alt_path}")

# historico[(mandante, visitante)] = [total_jogos, overs_count]
historico = defaultdict(lambda: [0, 0])

# Conjunto para recolher todos os times
times_disponiveis = set()

# Carrega CSV ao importar este módulo
with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # Pula cabeçalho (se houver)
    _ = next(reader, None)

    for row in reader:
        if len(row) < 4:
            continue
        mandante, visitante = row[0], row[1]
        if not mandante or not visitante or mandante == "NaN" or visitante == "NaN":
            continue
        try:
            gols_totais = float(row[2]) + float(row[3])
        except ValueError:
            continue

        chave = (mandante, visitante)
        registro = historico[chave]
        registro[0] += 1  # total_jogos
        if gols_totais > 2.5:
            registro[1] += 1  # overs_count

        times_disponiveis.update([mandante, visitante])

# Ordena a lista de times para retornar sempre em ordem alfabética
times_disponiveis = sorted(times_disponiveis)
