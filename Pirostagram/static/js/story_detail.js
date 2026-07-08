const imgs = document.querySelectorAll('.story-img');
let idx = 0;

document.getElementById('prev-btn').onclick = () => {
    if (idx > 0) {
        imgs[idx].style.display = 'none';
        idx--;
        imgs[idx].style.display = '';
    }
};
document.getElementById('next-btn').onclick = () => {
    if (idx < imgs.length - 1) {
        imgs[idx].style.display = 'none';
        idx++;
        imgs[idx].style.display = '';
    }
};