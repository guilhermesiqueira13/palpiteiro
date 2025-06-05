# api/teams.py

import json
import os
import sys

# Garante que o Python procure utils.py no mesmo diretório deste arquivo
sys.path.append(os.path.dirname(__file__))

try:
    from utils import times_disponiveis
except Exception as e:
    times_disponiveis = None
    import traceback
    traceback_str = traceback.format_exc()


def handler(request, response):
    # Se falhou ao importar utils.py, devolve 500 em JSON
    if times_disponiveis is None:
        response.set_status(500)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({
            "erro": "Falha ao carregar dados dos times.",
            "detalhes": traceback_str
        }))
        return

    # Permite apenas GET /api/teams
    if request.method != "GET":
        response.set_status(405)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({"erro": "Método não permitido"}))
        return

    # Retorna a lista de times em JSON
    response.set_status(200)
    response.set_header("Content-Type", "application/json")
    response.send(json.dumps(times_disponiveis))
