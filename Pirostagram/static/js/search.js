document.querySelectorAll('.search-follow-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const username = btn.dataset.username;
        const data = await ajaxPost(`/users/${username}/follow/`);
        btn.textContent = data.is_following ? 'unfollow' : 'follow';
    });
});