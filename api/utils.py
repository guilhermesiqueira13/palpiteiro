# api/utils.py
import csv
from collections import defaultdict
import os # This import was missing!

# Carrega os dados do arquivo CSV
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "dados_futebol.csv")

# Dicionário para armazenar os históricos de jogos
historico = defaultdict(lambda: [0, 0])

# Conjunto para coletar todos os times
times_disponiveis = set() # Add this to collect available teams

# Carrega os dados do CSV
try:
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        _ = next(reader, None)  # Pula cabeçalho
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

            times_disponiveis.update([mandante, visitante]) # Update the set with teams

except Exception as e:
    print(f"Erro ao carregar CSV: {e}")

# Ordena a lista final de times em ordem alfabética (for consistency with previous discussions)
times_disponiveis = sorted(times_disponiveis)