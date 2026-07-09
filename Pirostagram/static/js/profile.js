const followBtn = document.querySelector('.follow-btn');
if (followBtn) {
    followBtn.addEventListener('click', async (e) => {
        // 이벤트가 다른 곳으로 퍼지거나 꼬이는 것을 방지
        e.preventDefault(); 
        
        const username = followBtn.dataset.username;
        const data = await ajaxPost(`/users/${username}/follow/`);
        
        // 버튼 내부의 이미지 아이콘 선택
        const icon = followBtn.querySelector('.follow-icon');
        
        if (icon) {
            // 1. 서버 결과에 따라 이미지 src와 alt만 정확히 변경
            if (data.is_following) {
                icon.src = "/static/images/user-round-minus.svg";
                icon.alt = "unfollow";
            } else {
                icon.src = "/static/images/user-round-plus.svg";
                icon.alt = "follow";
            }
            
            // ⚠️ [핵심] 다른 스크립트가 글자를 강제로 채우는 것을 방지하기 위해 
            // 버튼 내부의 텍스트 노드(글자들)를 완전히 비워버리고 이미지 아이콘만 유지합니다.
            followBtn.childNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE) {
                    node.textContent = ''; // 글자 강제 삭제
                }
            });
        }
        
        // 프로필 페이지 내의 팔로워 숫자 실시간 업데이트
        const counter = document.getElementById('follower-count');
        if (counter) counter.textContent = data.follower_count;
    });
}