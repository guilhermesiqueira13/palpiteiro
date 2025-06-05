# api/teams.py
import os
import sys
from flask import Flask, jsonify

# 1) Garante que Python procure utils.py neste mesmo diretório
sys.path.append(os.path.dirname(__file__))

# 2) Tenta importar a lista de times de utils.py
try:
    from utils import times_disponiveis
except Exception as e:
    times_disponiveis = None
    traceback_str = None
    import traceback
    traceback_str = traceback.format_exc()

# 3) Cria a app Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_teams():
    # Se deu erro ao importar, devolve 500 com detalhes
    if times_disponiveis is None:
        return (
            jsonify({
                "erro": "Falha ao carregar dados dos times.",
                "detalhes": traceback_str
            }),
            500,
        )

    # Caso contrário, devolve 200 + JSON da lista de times
    return jsonify(times_disponiveis)

# 4) Expõe o app como "app", que o Vercel detecta como WSGI
#    (Não definimos “handler” aqui, pois o Vercel entende "app" do Flask)
