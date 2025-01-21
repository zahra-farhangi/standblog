const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggle-btn');
const main = document.getElementById('main');

toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    main.classList.toggle('shrink');
});
