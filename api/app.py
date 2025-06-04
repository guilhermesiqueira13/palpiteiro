from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from collections import defaultdict

# Inicializar app Flask
app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})  # Libera CORS para tudo


# Carregar dados de confrontos para calcular probabilidades
historico = defaultdict(lambda: [0, 0])  # (total_jogos, overs)
times_disponiveis = set()

with open('dados_futebol.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    cabecalho = next(reader, None)  # pula cabecalho
    for row in reader:
        if len(row) < 4:
            continue
        mandante, visitante = row[0], row[1]
        if not mandante or not visitante or mandante == 'NaN' or visitante == 'NaN':
            continue
        try:
            gols = float(row[2]) + float(row[3])
        except ValueError:
            continue
        key = (mandante, visitante)
        registro = historico[key]
        registro[0] += 1
        if gols > 2.5:
            registro[1] += 1
        times_disponiveis.update([mandante, visitante])

times_disponiveis = sorted(times_disponiveis)



@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/teams')
def listar_times():
    """Retorna a lista de times reconhecidos."""
    return jsonify(sorted(times_disponiveis))

@app.route('/predict', methods=['POST'])
def prever():
    try:
        dados = request.get_json()

        time_mandante = dados.get('time_mandante')
        time_visitante = dados.get('time_visitante')

        if not time_mandante or not time_visitante or time_mandante == time_visitante:
            return jsonify({'erro': 'Times inválidos.'}), 400

        chave = (time_mandante, time_visitante)
        total, overs = historico.get(chave, (0, 0))

        if total > 0:
            prob = overs / total
            confrontos_utilizados = total
        else:
            # usa media geral caso nao haja confrontos entre os times
            total_geral = sum(v[0] for v in historico.values())
            overs_geral = sum(v[1] for v in historico.values())
            prob = overs_geral / total_geral if total_geral else 0.0
            confrontos_utilizados = 0

        return jsonify({
            'probabilidade': float(prob),
            'confrontos_utilizados': int(confrontos_utilizados)
        })

    except Exception as e:
        print("Erro interno:", e)
        return jsonify({'erro': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
