import json
import os
import sys

# Ajusta path para importar utils.py
sys.path.append(os.path.dirname(__file__))
try:
    from utils import times_disponiveis
except Exception as e:
    times_disponiveis = None
    import traceback
    traceback_str = traceback.format_exc()

def handler(request, response):
    # Se utils falhar, devolve 500 em JSON
    if times_disponiveis is None:
        response.set_status(500)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({
            "erro": "Falha ao carregar dados dos times.",
            "detalhes": traceback_str
        }))
        return

    # Só GET permitido
    if request.method != "GET":
        response.set_status(405)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({"erro": "Método não permitido"}))
        return

    response.set_status(200)
    response.set_header("Content-Type", "application/json")
    response.send(json.dumps(times_disponiveis))
