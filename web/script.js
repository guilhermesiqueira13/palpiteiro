async function verificarProbabilidade() {
  const home = document.getElementById("home").value;
  const away = document.getElementById("away").value;
  const resultado = document.getElementById("resultado");

  // Elementos do botão para animação de loading
  const botao = document.getElementById("btn-check");
  const btnText = document.getElementById("btn-text");
  const loadingContainer = document.getElementById("loading-container");

  if (home === away) {
    resultado.textContent = "Escolha times diferentes.";
    resultado.style.color = "red";
    return;
  }

  // Guarda os valores que serão exibidos após o delay
  let finalText = "";
  let finalColor = "black";

  // Marca o início do carregamento
  const startTime = Date.now();

  // ===== Inicia animação de “Calculando...” com 3 dots =====
  resultado.textContent = ""; // limpa texto anterior
  btnText.hidden = true; // esconde “Ver Probabilidade”
  loadingContainer.removeAttribute("hidden"); // mostra “Calculando” + dots
  botao.disabled = true; // desabilita o botão enquanto carrega

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
    // ===== Garante que o loading complete pelo menos 1 ciclo de 1s =====
    const animationDuration = 1000; // duração de um ciclo em milissegundos
    const elapsed = Date.now() - startTime;
    const remainder =
      (animationDuration - (elapsed % animationDuration)) % animationDuration;
    if (remainder > 0) {
      await new Promise((r) => setTimeout(r, remainder));
    }

    // ===== Após o delay, exibe o resultado (texto e cor) =====
    resultado.textContent = finalText;
    resultado.style.color = finalColor;

    // ===== Para animação e restaura botão =====
    loadingContainer.setAttribute("hidden", "");
    btnText.hidden = false; // mostra “Ver Probabilidade” novamente
    botao.disabled = false; // reabilita o botão
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
