// 게시글 삭제 (Ajax)
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        if (!confirm('삭제할까요?')) return;
        const postId = btn.dataset.postId;
        const data = await ajaxDelete(`/posts/${postId}/delete/`);
        if (data.success) {
            btn.closest('.post-card').remove();
        }
    });
});

// 좋아요 토글 (Ajax)
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        console.log("하트 버튼 클릭됨!"); // 👈 1단계 확인용
        const postId = btn.dataset.postId;
        const data = await ajaxPost(`/posts/${postId}/like/`);
        console.log("서버에서 받은 데이터:", data); // 👈 2단계 확인용

        const heartIcon = btn.querySelector('.heart-icon');
        console.log("찾은 SVG 아이콘 요소:", heartIcon); // 👈 3단계 확인용 (만약 null이 뜨면 HTML 구조가 다른 것)

        if (heartIcon) {
            if (data.liked) {
                heartIcon.classList.add('active');
                console.log("active 클래스 추가됨");
            } else {
                heartIcon.classList.remove('active');
                console.log("active 클래스 제거됨");
            }
        } else {
            console.error(".heart-icon을 찾을 수 없습니다. HTML 코드를 확인하세요.");
        }

        btn.querySelector('.like-count').textContent = data.like_count;
    });
});

// 댓글 작성 (Ajax)
document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const wrapper = form.closest('.comments');
        const postId = wrapper.dataset.postId;
        const input = form.querySelector('.comment-input');
        const content = input.value.trim();
        if (!content) return;

        const data = await ajaxPost(`/posts/${postId}/comment/`, { content });
        if (data.success) {
            const list = wrapper.querySelector('.comment-list');
            list.insertAdjacentHTML('beforeend', `
                <div class="comment" data-comment-id="${data.comment_id}">
                    <b>${data.author}</b>
                    <span class="comment-content">${data.content}</span>
                    <button class="comment-edit-btn">수정</button>
                    <button class="comment-delete-btn">삭제</button>
                </div>
            `);
            input.value = '';

            // 댓글 개수 갱신
            const countSpan = wrapper.closest('.post-card').querySelector('.comment-count');
            countSpan.textContent = parseInt(countSpan.textContent) + 1;

            attachCommentHandlers();
        }
    });
});

// 댓글 수정/삭제 (동적 요소 대비 함수화)
function attachCommentHandlers() {
    document.querySelectorAll('.comment-delete-btn').forEach(btn => {
        btn.onclick = async () => {
            const commentDiv = btn.closest('.comment');
            const id = commentDiv.dataset.commentId;
            const data = await ajaxDelete(`/posts/comment/${id}/delete/`);
            if (data.success) {
                const postCard = commentDiv.closest('.post-card');
                commentDiv.remove();
                const countSpan = postCard.querySelector('.comment-count');
                countSpan.textContent = parseInt(countSpan.textContent) - 1;
            }
        };
    });

    document.querySelectorAll('.comment-edit-btn').forEach(btn => {
        btn.onclick = async () => {
            const commentDiv = btn.closest('.comment');
            const id = commentDiv.dataset.commentId;
            const span = commentDiv.querySelector('.comment-content');
            const newContent = prompt('수정할 내용', span.textContent.trim());
            if (!newContent) return;
            const data = await ajaxPost(`/posts/comment/${id}/update/`, { content: newContent });
            if (data.success) span.textContent = data.content;
        };
    });
}
attachCommentHandlers();

// 모든 추천 팔로우 버튼들을 선택합니다.
document.querySelectorAll('.suggest-follow-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const username = btn.dataset.username;
        const data = await ajaxPost(`/users/${username}/follow/`);
        
        // 버튼 내부의 이미지 태그 선택
        const icon = btn.querySelector('.follow-icon');
        
        if (icon) {
            // 서버에서 넘어온 팔로우 유무 상태(data.is_following)에 따라 이미지 src 교체
            // ⚠️ 이미지 파일명이 프로젝트와 다르면 이 부분을 알맞게 수정하세요!
            if (data.is_following) {
                icon.src = "/static/images/user-round-minus.svg";
                icon.alt = "unfollow";
            } else {
                icon.src = "/static/images/user-round-plus.svg";
                icon.alt = "follow";
            }
        }
        
        // 만약 현재 페이지에 내 팔로워 카운터가 있다면 업데이트 (프로필 페이지 등 대응)
        const counter = document.getElementById('follower-count');
        if (counter) counter.textContent = data.follower_count;
    });
});