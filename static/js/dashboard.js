const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggle-btn');
const main = document.getElementById('main');

toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    main.classList.toggle('shrink');
});


document.getElementById("ticketForm").addEventListener("submit", function(event) {
    event.preventDefault();  // جلوگیری از ارسال معمولی فرم

    let formData = new FormData(this);

    fetch(this.action, {  // ارسال به همان ویو contact_us
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"  // مشخص کردن درخواست AJAX
        }
    })
    .then(response => response.json())  // تبدیل پاسخ به JSON
    .then(data => {
        if (data.message) {
            document.getElementById("responseMessage").innerHTML = `<p style="color: green">${data.message}</p>`;
            document.getElementById("ticketForm").reset();  // پاک کردن فرم
        } else if (data.error) {
            document.getElementById("responseMessage").innerHTML = `<p style="color: red">${data.error}</p>`;
        }
    })
    .catch(error => {
        document.getElementById("responseMessage").innerHTML = `<p style="color: red">خطایی رخ داد!</p>`;
    });
});