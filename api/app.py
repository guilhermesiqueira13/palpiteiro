import os
from flask import Flask, jsonify, request, send_from_directory

# Garante que o Python encontre utils.py
import sys
sys.path.append(os.path.dirname(__file__))
from utils import historico, times_disponiveis

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "..", "public")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")

@app.route("/")
def index():
    """Serve a página inicial estática."""
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/teams", methods=["GET"])
def get_teams():
    """Retorna a lista de times disponíveis."""
    return jsonify(times_disponiveis)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Dados não enviados ou mal formatados."}), 400

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
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
