# api/predict.py
import os, sys
from flask import Flask, jsonify, request

sys.path.append(os.path.dirname(__file__))
from utils import historico

app = Flask(__name__)

# Rota que responde ao POST em /predict
@app.route("/", methods=["POST"])
def predict():
    # A lógica do seu código para processar a requisição POST
    data = request.json
    time_mandante = data.get("time_mandante")
    time_visitante = data.get("time_visitante")
    
    if not time_mandante or not time_visitante or time_mandante == time_visitante:
        return jsonify({"erro": "Times inválidos."}), 400

    chave = (time_mandante, time_visitante)
    total, overs = historico.get(chave, (0, 0))

    if total > 0:
        prob = overs / total
        confrontos_utilizados = total
    else:
        total_geral = sum(v[0] for v in historico.values())
        overs_geral = sum(v[1] for v in historico.values())
        prob = (overs_geral / total_geral) if total_geral else 0.0
        confrontos_utilizados = 0

    return jsonify({
        "probabilidade": float(prob),
        "confrontos_utilizados": int(confrontos_utilizados)
    })

# A aplicação Flask será automaticamente descoberta pelo Vercel, então nada mais precisa ser feito aqui.
