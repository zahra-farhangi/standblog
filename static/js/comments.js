document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('comment');


    function set_value(commentId) {
        // تنظیم parent_id در فیلد hidden فرم
        document.getElementById('parent_id').value = commentId;

        // انتخاب فرم
        const formSection = document.querySelector('.submit-comment');
        console.log(formSection);  // بررسی کنید که آیا بخش فرم پیدا می‌شود
        if (formSection) {
            // تغییر مکان فرم به محل نوشتن کامنت
            formSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            console.log('بخش فرم یافت نشد');
        }
    }

    // اینجا باید دکمه‌های "Reply" خود را پیدا کرده و برای هر کدام event listener را اضافه کنید
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.getAttribute('data-comment-id');
            set_value(commentId);
        });
    });


    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const body = document.getElementById('body').value.trim();
            const parentId = document.getElementById('parent_id').value;

            if (!body) {
                alert('بخش ارسال نظر نمی تواند خالی باشد.');
                return;
            }

            fetch(commentForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    body: body,
                    parent_id: parentId || null,
                }),
            })
                .then(response => {
                    if (response.headers.get('content-type')?.includes('application/json')) {
                        return response.json();
                    } else {
                        throw new Error('پاسخ نامعتبر از سرور');
                    }
                })
                .then(data => {
                    if (data.error) {
                        alert(`Error: ${data.error}`);
                    } else {
                        alert('نظر شما با موفقیت اضافه شد');
                        // افزودن کامنت جدید
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('هنگام ارسال نظر شما خطایی رخ داد.');
                });
        });
    }

    window.set_value = function (parentId) {
        document.getElementById('parent_id').value = parentId;
    };
});
