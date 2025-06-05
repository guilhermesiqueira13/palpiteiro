// public/script.js
async function verificarProbabilidade() {
  const home = document.getElementById("home").value;
  const away = document.getElementById("away").value;
  const resultado = document.getElementById("resultado");

  const botao = document.getElementById("btn-check");
  const btnText = document.getElementById("btn-text");
  const loadingContainer = document.getElementById("loading-container");

  if (home === away) {
    resultado.textContent = "Escolha times diferentes.";
    resultado.style.color = "red";
    return;
  }

  // Inicia animação
  const startTime = Date.now();
  resultado.textContent = "";
  btnText.hidden = true;
  loadingContainer.removeAttribute("hidden");
  botao.disabled = true;

  let finalText = "";
  let finalColor = "black";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ time_mandante: home, time_visitante: away }),
    });

    const data = await res.json();
    if (res.ok && data?.probabilidade != null) {
      const prob = (data.probabilidade * 100).toFixed(2);
      finalText = `Probabilidade de Over 2.5 gols: ${prob}% (baseado nos últimos ${data.confrontos_utilizados} jogos)`;
      finalColor = "green";
    } else {
      finalText = "Erro na resposta da API.";
      finalColor = "red";
    }
  } catch (err) {
    finalText = "Erro ao conectar à API.";
    finalColor = "red";
  } finally {
    // Garante ciclo completo de 1s de loading
    const animationDuration = 1000;
    const elapsed = Date.now() - startTime;
    const remainder =
      (animationDuration - (elapsed % animationDuration)) % animationDuration;
    if (remainder > 0) {
      await new Promise((r) => setTimeout(r, remainder));
    }

    // Exibe resultado somente após o loading terminar
    resultado.textContent = finalText;
    resultado.style.color = finalColor;

    // Para a animação e restaura botão
    loadingContainer.setAttribute("hidden", "");
    btnText.hidden = false;
    botao.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const homeSelect = document.getElementById("home");
  const awaySelect = document.getElementById("away");

  try {
    const res = await fetch("/teams");
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `Status ${res.status}`);
    }
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
