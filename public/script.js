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

  // Inicia animação de loading
  const startTime = Date.now();
  resultado.textContent = "";
  btnText.hidden = true;
  loadingContainer.removeAttribute("hidden");
  botao.disabled = true;

  let finalText = "";
  let finalColor = "black";

  try {
    // Requisição para /predict (serverless Python)
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ time_mandante: home, time_visitante: away }),
    });

    const payload = await res.json();
    if (res.ok && payload.probabilidade != null) {
      const prob = (payload.probabilidade * 100).toFixed(2);
      finalText = `Probabilidade de Over 2.5 gols: ${prob}% (baseado nos últimos ${payload.confrontos_utilizados} jogos)`;
      finalColor = "green";
    } else {
      const erroMsg = payload.erro || "Erro na resposta da API.";
      finalText = `Erro: ${erroMsg}`;
      finalColor = "red";
      console.error("Payload de erro do predict:", payload);
    }
  } catch (err) {
    finalText = "Erro ao conectar à API.";
    finalColor = "red";
    console.error("Exceção no fetch /predict:", err);
  } finally {
    // Garante que o loading fique visível por pelo menos 1s
    const animationDuration = 1000;
    const elapsed = Date.now() - startTime;
    const remainder =
      (animationDuration - (elapsed % animationDuration)) % animationDuration;
    if (remainder > 0) {
      await new Promise((r) => setTimeout(r, remainder));
    }

    // Exibe o resultado ou erro
    resultado.textContent = finalText;
    resultado.style.color = finalColor;

    // Finaliza animação e restaura botão
    loadingContainer.setAttribute("hidden", "");
    btnText.hidden = false;
    botao.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const homeSelect = document.getElementById("home");
  const awaySelect = document.getElementById("away");
  const resultado = document.getElementById("resultado");

  try {
    const res = await fetch("/teams");
    const payload = await res.json();

    if (res.ok && Array.isArray(payload)) {
      payload.forEach((t) => {
        const o1 = document.createElement("option");
        o1.value = t;
        o1.textContent = t;
        homeSelect.appendChild(o1);

        const o2 = document.createElement("option");
        o2.value = t;
        o2.textContent = t;
        awaySelect.appendChild(o2);
      });
    } else {
      console.error("Payload inesperado de /teams:", payload);
      resultado.textContent = "Erro ao carregar times.";
      resultado.style.color = "red";
    }
  } catch (err) {
    console.error("Erro ao conectar em /teams:", err);
    resultado.textContent = "Erro ao carregar times.";
    resultado.style.color = "red";
  }
});
