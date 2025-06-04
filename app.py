from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# Inicializar app Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Libera CORS para tudo

# Carregar modelo e scaler
modelo = joblib.load('modelo_over25_final_model.pkl')
scaler = joblib.load('scaler.pkl')

# Times usados no treinamento
# Times disponíveis no modelo treinado
times_disponiveis = [
    "Gremio",
    "Botafogo",
    "Cuiaba",
    "Fluminense",
    "Bahia",
    "Atletico Goianiense",
]

@app.route('/predict', methods=['POST'])
def prever():
    try:
        dados = request.get_json()

        time_mandante = dados.get('time_mandante')
        time_visitante = dados.get('time_visitante')

        if not time_mandante or not time_visitante or time_mandante == time_visitante:
            return jsonify({'erro': 'Times inválidos.'}), 400

        # One-hot encoding
        linha = {f'home_{t}': 0 for t in times_disponiveis}
        linha.update({f'away_{t}': 0 for t in times_disponiveis})

        if f'home_{time_mandante}' in linha:
            linha[f'home_{time_mandante}'] = 1
        if f'away_{time_visitante}' in linha:
            linha[f'away_{time_visitante}'] = 1

        # Garante que as colunas estejam na mesma ordem do scaler
        df = pd.DataFrame([linha], columns=scaler.feature_names_in_)
        df_scaled = scaler.transform(df)
        prob = modelo.predict_proba(df_scaled)[0][1]

        return jsonify({
            'probabilidade': float(prob),
            'confrontos_utilizados': 50
        })

    except Exception as e:
        print("Erro interno:", e)
        return jsonify({'erro': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
