async function verificarProbabilidade() {
  const home = document.getElementById("home").value;
  const away = document.getElementById("away").value;
  const resultado = document.getElementById("resultado");

  if (home === away) {
    resultado.textContent = "Escolha times diferentes.";
    resultado.style.color = "red";
    return;
  }

  resultado.textContent = "Calculando...";
  resultado.style.color = "black";

  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        time_mandante: home,
        time_visitante: away,
      }),
    });

    const data = await res.json();
    if (res.ok && data?.probabilidade != null) {
      resultado.textContent = `Probabilidade de Over 2.5 gols: ${(
        data.probabilidade * 100
      ).toFixed(2)}% (baseado em ${data.confrontos_utilizados} jogos)`;
      resultado.style.color = "green";
    } else {
      resultado.textContent = "Erro na resposta da API.";
      resultado.style.color = "red";
    }
  } catch (err) {
    resultado.textContent = "Erro ao conectar à API.";
    resultado.style.color = "red";
  }
}
