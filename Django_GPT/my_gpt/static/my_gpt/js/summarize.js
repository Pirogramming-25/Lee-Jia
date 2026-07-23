(function () {
  const btn = document.getElementById("run-btn");
  const input = document.getElementById("input-text");
  const loading = document.getElementById("loading");
  const result = document.getElementById("result");
  const errorBox = document.getElementById("error");
  const historyList = document.getElementById("history-list");

  function renderResult(data) {
    result.innerHTML = "";
    result.appendChild(el("h3", null, "요약 결과"));

    const box = el("div", "summary-box", data.summary);
    result.appendChild(box);

    const meta = el("ul", "score-list");
    const rows = [
      ["원문 길이", `${data.original_length}자`],
      ["요약문 길이", `${data.summary_length}자`],
      ["요약 비율", `${data.ratio}%`],
    ];
    rows.forEach(([k, v]) => {
      const li = el("li");
      li.appendChild(el("span", null, k));
      li.appendChild(el("span", null, v));
      meta.appendChild(li);
    });
    result.appendChild(meta);
  }

  function prependHistory(summary) {
    const li = el("li");
    li.appendChild(el("div", "h-label", "요약 결과"));
    li.appendChild(el("div", "h-text",
      summary.length > 120 ? summary.slice(0, 120) + "…" : summary));
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
    if (text.length < 100) {
      errorBox.textContent = "요약할 문서는 100자 이상 입력해주세요.";
      return;
    }
    const data = await runInference("/summarize/run/", { text },
      { btn, input, loading, result, errorBox });
    if (!data) return;

    renderResult(data);
    prependHistory(data.summary);
  });
})();