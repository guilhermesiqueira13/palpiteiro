from flask import Flask, jsonify
import os, sys

sys.path.append(os.path.dirname(__file__))
try:
    from utils import times_disponiveis
except:
    times_disponiveis = []
    import traceback
    traceback_str = traceback.format_exc()

app = Flask(__name__)

# Rota raiz permanece igual
@app.route("/", methods=["GET"])
def get_teams_root():
    if not times_disponiveis:
        return jsonify({"erro": "Falhou importar utils"}), 500
    return jsonify(times_disponiveis)

# Nova rota /teams, apenas para teste local
@app.route("/teams", methods=["GET"])
def get_teams_alias():
    return get_teams_root()

if __name__ == "__main__":
    # Ao rodar python teams.py, o Flask inicia em http://127.0.0.1:5000/
    app.run(debug=True, host="0.0.0.0", port=5000)
