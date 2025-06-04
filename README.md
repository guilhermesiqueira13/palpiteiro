# Palpiteiro

Aplicação simples em Flask que fornece a probabilidade de uma partida ter mais de 2,5 gols.
As probabilidades são calculadas com base no histórico de confrontos presente em `dados_futebol.csv`,
sem utilização de modelos de aprendizado de máquina.

## Como executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie a API:
   ```bash
   python app.py
   ```
3. Acesse `http://localhost:5000` em um navegador para testar a aplicação.

