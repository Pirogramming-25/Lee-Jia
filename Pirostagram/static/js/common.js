// CSRF 토큰 가져오기
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
const CSRF_TOKEN = getCookie('csrftoken');

// JSON POST 요청
async function ajaxPost(url, data = {}) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return res.json();
}

// 바디 없이 POST (삭제 등)
async function ajaxDelete(url) {
    const res = await fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
    });
    return res.json();
}