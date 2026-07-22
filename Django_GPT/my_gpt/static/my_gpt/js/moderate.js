(function () {
  const btn = document.getElementById("run-btn");
  const input = document.getElementById("input-text");
  const loading = document.getElementById("loading");
  const result = document.getElementById("result");
  const errorBox = document.getElementById("error");
  const historyList = document.getElementById("history-list");

  function renderResult(data) {
    result.innerHTML = "";
    result.appendChild(el("h3", null,
      `최고 위험 레이블: ${data.highest_label} (${pct(data.highest_score)})`));

    if (Array.isArray(data.all_scores) && data.all_scores.length) {
      const ul = el("ul", "score-list");
      data.all_scores.forEach((s) => {
        const li = el("li");
        li.appendChild(el("span", null, s.label));
        li.appendChild(el("span", null, pct(s.score)));
        ul.appendChild(li);
      });
      result.appendChild(ul);
    }
  }

  function prependHistory(label, text) {
    const li = el("li");
    li.appendChild(el("div", "h-label", label));
    li.appendChild(el("div", "h-text",
      text.length > 80 ? text.slice(0, 80) + "…" : text));
    li.appendChild(el("div", "h-time", new Date().toLocaleString()));

    const empty = historyList.querySelector(".h-empty");
    if (empty) empty.remove();

    historyList.insertBefore(li, historyList.firstChild);
    while (historyList.children.length > 5) {
      historyList.removeChild(historyList.lastChild);
    }
  }

  btn.addEventListener("click", async () => {
    const text = input.value.trim();
    if (!text) {
      errorBox.textContent = "분석할 문장을 입력해주세요.";
      return;
    }
    const data = await runInference("/moderate/run/", { text },
      { btn, input, loading, result, errorBox });
    if (!data) return;

    renderResult(data);
    prependHistory(data.highest_label, text);
  });
})();