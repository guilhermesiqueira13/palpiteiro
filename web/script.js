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
    const res = await fetch("/predict", {
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

document.addEventListener("DOMContentLoaded", async () => {
  const homeSelect = document.getElementById("home");
  const awaySelect = document.getElementById("away");

  try {
    const res = await fetch("/teams");
    const teams = await res.json();
    teams.forEach((t) => {
      const optHome = document.createElement("option");
      optHome.value = t;
      optHome.textContent = t;
      homeSelect.appendChild(optHome);

      const optAway = document.createElement("option");
      optAway.value = t;
      optAway.textContent = t;
      awaySelect.appendChild(optAway);
    });
  } catch (err) {
    console.error("Erro ao carregar times", err);
  }
});

