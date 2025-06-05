# api/predict.py
import os
import sys
from flask import Flask, jsonify, request

sys.path.append(os.path.dirname(__file__))
from utils import historico

app = Flask(__name__)

@app.route("/", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Tenta pegar os dados JSON da requisição
        data = request.json
        if not data:
            return jsonify({"erro": "Dados não enviados ou mal formatados."}), 400

        # Verifica se os parâmetros necessários estão presentes
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
    
    except Exception as e:
        # Captura e retorna qualquer erro inesperado
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500

