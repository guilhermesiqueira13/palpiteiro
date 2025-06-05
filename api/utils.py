import os
import csv
from collections import defaultdict

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "dados_futebol.csv")

# historico[(mandante, visitante)] = [total_jogos, overs_count]
historico = defaultdict(lambda: [0, 0])
times_disponiveis = set()

with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    _ = next(reader, None)  # pula cabeçalho, se houver
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
        registro[0] += 1
        if gols_totais > 2.5:
            registro[1] += 1

        times_disponiveis.update([mandante, visitante])

times_disponiveis = sorted(times_disponiveis)
