(function () {
  const btn = document.getElementById("run-btn");
  const input = document.getElementById("input-text");
  const loading = document.getElementById("loading");
  const result = document.getElementById("result");
  const errorBox = document.getElementById("error");
  const historyList = document.getElementById("history-list");

  // 비로그인 사용자 전용: JS 배열에만 저장. 새로고침하면 사라짐.
  const guestHistory = [];

  function renderResult(data) {
    result.innerHTML = "";
    result.appendChild(el("h3", null,
      `감정: ${data.label} (신뢰도 ${pct(data.score)})`));

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

  function addHistoryItem(label, text) {
    // 비로그인 사용자 화면 갱신용
    guestHistory.unshift({ label, text, time: new Date() });
    if (guestHistory.length > 5) guestHistory.pop();

    historyList.innerHTML = "";
    guestHistory.forEach((h) => {
      const li = el("li");
      li.appendChild(el("div", "h-label", h.label));
      li.appendChild(el("div", "h-text",
        h.text.length > 80 ? h.text.slice(0, 80) + "…" : h.text));
      li.appendChild(el("div", "h-time",
        h.time.toLocaleString()));
      historyList.appendChild(li);
    });
  }

  function addServerHistoryItem(label, text) {
    // 로그인 사용자: 서버 저장은 이미 됨. 화면 앞쪽에 즉시 반영.
    const li = el("li");
    li.appendChild(el("div", "h-label", label));
    li.appendChild(el("div", "h-text",
      text.length > 80 ? text.slice(0, 80) + "…" : text));
    li.appendChild(el("div", "h-time", new Date().toLocaleString()));

    // 안내용 empty 항목이 있으면 제거
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
    const data = await runInference("/sentiment/run/", { text },
      { btn, input, loading, result, errorBox });
    if (!data) return;

    renderResult(data);

    if (window.IS_AUTHENTICATED) {
      addServerHistoryItem(data.label, text);
    } else {
      addHistoryItem(data.label, text);
    }
  });
})();