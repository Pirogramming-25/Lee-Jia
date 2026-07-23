function getCookie(name) {
  const parts = document.cookie ? document.cookie.split(";") : [];
  for (const p of parts) {
    const c = p.trim();
    if (c.startsWith(name + "=")) {
      return decodeURIComponent(c.slice(name.length + 1));
    }
  }
  return null;
}

async function runInference(url, payload, ui) {
  const { btn, input, loading, result, errorBox } = ui;
  btn.disabled = true;
  input.disabled = true;
  loading.hidden = false;
  errorBox.textContent = "";
  result.innerHTML = "";

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      errorBox.textContent = data.error || `요청 실패 (${res.status})`;
      return null;
    }
    return data.result;
  } catch (e) {
    errorBox.textContent = "서버와 통신하지 못했습니다.";
    return null;
  } finally {
    btn.disabled = false;
    input.disabled = false;
    loading.hidden = true;
  }
}

function pct(v) {
  return `${(v * 100).toFixed(2)}%`;
}

function el(tag, className, text) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined) e.textContent = text;
  return e;
}