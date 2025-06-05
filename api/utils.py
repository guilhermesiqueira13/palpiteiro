import os
import csv
from collections import defaultdict

# Pasta deste arquivo
BASE_DIR = os.path.dirname(__file__)

# Caminho completo para o CSV
CSV_PATH = os.path.join(BASE_DIR, "dados_futebol.csv")

# Estrutura: historico[(mandante, visitante)] = [total_jogos, overs_count]
historico = defaultdict(lambda: [0, 0])
# Conjunto para coletar todos os times
times_disponiveis = set()

# Carrega o CSV ao importar este módulo
with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # Pula cabeçalho, se presente
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
        registro[0] += 1  # total_jogos incrementa em 1
        if gols_totais > 2.5:
            registro[1] += 1  # overs_count incrementa em 1

        times_disponiveis.update([mandante, visitante])

# Ordena a lista final de times em ordem alfabética
times_disponiveis = sorted(times_disponiveis)