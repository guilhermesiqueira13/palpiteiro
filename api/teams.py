# api/teams.py
import json
from .utils import times_disponiveis  # importa a lista já ordenada

def handler(request, response):
    """
    Retorna a lista de times em JSON.
    Será chamado quando o front fizer GET /teams
    """
    # Monta a resposta
    response.set_status(200)
    response.set_header("Content-Type", "application/json")
    response.send(json.dumps(times_disponiveis))
