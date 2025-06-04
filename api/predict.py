import json
import os
import sys

# Garante que utils.py (no mesmo diretório) seja importado corretamente
sys.path.append(os.path.dirname(__file__))
try:
    from utils import historico
except Exception as e:
    historico = None
    import traceback
    tb_utils = traceback.format_exc()


def handler(request, response):
    # Se falhou ao importar utils, retorna 500 em JSON
    if historico is None:
        response.set_status(500)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({
            "erro": "Falha ao carregar histórico.",
            "detalhes": tb_utils
        }))
        return

    # Só aceita POST
    if request.method != "POST":
        response.set_status(405)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({"erro": "Método não permitido"}))
        return

    try:
        dados = request.json  # já é um dict Python
        time_mandante = dados.get("time_mandante")
        time_visitante = dados.get("time_visitante")

        # Validação mínima
        if not time_mandante or not time_visitante or time_mandante == time_visitante:
            response.set_status(400)
            response.set_header("Content-Type", "application/json")
            response.send(json.dumps({"erro": "Times inválidos."}))
            return

        chave = (time_mandante, time_visitante)
        total, overs = historico.get(chave, (0, 0))

        if total > 0:
            prob = overs / total
            confrontos_utilizados = total
        else:
            # se não houve confrontos diretos, usar média geral
            total_geral = sum(v[0] for v in historico.values())
            overs_geral = sum(v[1] for v in historico.values())
            prob = (overs_geral / total_geral) if total_geral else 0.0
            confrontos_utilizados = 0

        response.set_status(200)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({
            "probabilidade": float(prob),
            "confrontos_utilizados": int(confrontos_utilizados)
        }))
    except Exception as e:
        tb = traceback.format_exc()
        response.set_status(500)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({
            "erro": "Erro interno no servidor",
            "detalhes": tb
        }))
