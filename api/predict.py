# api/predict.py
import os
import sys
from flask import Flask, request, jsonify

sys.path.append(os.path.dirname(__file__))

try:
    from utils import historico
except Exception as e:
    historico = None
    import traceback
    traceback_str = traceback.format_exc()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def predict():
    # Se histório não carregou, devolve erro
    if historico is None:
        return (
            jsonify({
                "erro": "Falha ao carregar histórico.",
                "detalhes": traceback_str
            }),
            500,
        )

    data = request.get_json(silent=True) or {}
    time_mandante = data.get("time_mandante")
    time_visitante = data.get("time_visitante")

    # Validações básicas
    if not time_mandante or not time_visitante or time_mandante == time_visitante:
        return jsonify({"erro": "Times inválidos."}), 400

    chave = (time_mandante, time_visitante)
    total, overs = historico.get(chave, (0, 0))

    if total > 0:
        prob = overs / total
        confrontos_utilizados = total
    else:
        # Se não houve confrontos diretos, usa média geral
        total_geral = sum(v[0] for v in historico.values())
        overs_geral = sum(v[1] for v in historico.values())
        prob = (overs_geral / total_geral) if total_geral else 0.0
        confrontos_utilizados = 0

    return jsonify({
        "probabilidade": float(prob),
        "confrontos_utilizados": int(confrontos_utilizados)
    })

# Expõe o app Flask
