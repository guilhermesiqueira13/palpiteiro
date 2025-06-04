# api/predict.py
import json
from .utils import historico

def handler(request, response):
    """
    Retorna JSON com { probabilidade, confrontos_utilizados }.
    Será chamado quando o front fizer POST /predict
    """

    # Permitir apenas método POST
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
        # Qualquer erro interno
        print("Erro interno em /predict:", e)
        response.set_status(500)
        response.set_header("Content-Type", "application/json")
        response.send(json.dumps({"erro": "Erro interno no servidor"}))
