// document.addEventListener('DOMContentLoaded', function () {
//     const commentForm = document.getElementById('comment');
//
//
//     function set_value(commentId) {
//         // تنظیم parent_id در فیلد hidden فرم
//         document.getElementById('parent_id').value = commentId;
//
//         // انتخاب فرم
//         const formSection = document.querySelector('.submit-comment');
//         console.log(formSection);  // بررسی کنید که آیا بخش فرم پیدا می‌شود
//         if (formSection) {
//             // تغییر مکان فرم به محل نوشتن کامنت
//             formSection.scrollIntoView({ behavior: 'smooth' });
//         } else {
//             console.log('بخش فرم یافت نشد');
//         }
//     }
//
//     // اینجا باید دکمه‌های "Reply" خود را پیدا کرده و برای هر کدام event listener را اضافه کنید
//     document.querySelectorAll('.btn-primary').forEach(button => {
//         button.addEventListener('click', function () {
//             const commentId = this.getAttribute('data-comment-id');
//             set_value(commentId);
//         });
//     });
//
//
//     if (commentForm) {
//         commentForm.addEventListener('submit', function (event) {
//             event.preventDefault();
//
//             const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//             const body = document.getElementById('body').value.trim();
//             const parentId = document.getElementById('parent_id').value;
//
//             if (!body) {
//                 alert('بخش ارسال نظر نمی تواند خالی باشد.');
//                 return;
//             }
//
//             fetch(commentForm.action, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': csrfToken,
//                     'Content-Type': 'application/json',
//                     'X-Requested-With': 'XMLHttpRequest',
//                 },
//                 body: JSON.stringify({
//                     body: body,
//                     parent_id: parentId || null,
//                 }),
//             })
//                 .then(response => {
//                     if (response.headers.get('content-type')?.includes('application/json')) {
//                         return response.json();
//                     } else {
//                         throw new Error('پاسخ نامعتبر از سرور');
//                     }
//                 })
//                 .then(data => {
//                     if (data.error) {
//                         alert(`Error: ${data.error}`);
//                     } else {
//                         alert('نظر شما با موفقیت اضافه شد');
//                         // افزودن کامنت جدید
//                     }
//                 })
//                 .catch(error => {
//                     console.error('Error:', error);
//                     alert('هنگام ارسال نظر شما خطایی رخ داد.');
//                 });
//         });
//     }
//
//     window.set_value = function (parentId) {
//         document.getElementById('parent_id').value = parentId;
//     };
// });


document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('comment');

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const body = document.getElementById('body').value.trim();
            const parentId = document.getElementById('parent_id').value;

            if (!body) {
                alert('بخش ارسال نظر نمی‌تواند خالی باشد.');
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
                        addCommentToDOM(data.comment, parentId); // اضافه کردن کامنت به DOM
                        commentForm.reset(); // پاک کردن فرم پس از ارسال
                        document.getElementById('parent_id').value = ''; // پاک کردن parent_id
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('هنگام ارسال نظر شما خطایی رخ داد.');
                });
        });
    }

    // تابع برای اضافه کردن کامنت جدید به DOM
    function addCommentToDOM(comment, parentId) {
        let commentList;

        // اگر parentId وجود دارد، یعنی این کامنت ریپلای است
        if (parentId) {
            // پیدا کردن کامنت والد
            const parentComment = document.querySelector(`.btn-primary[data-comment-id="${parentId}"]`).closest('li');

            // پیدا کردن لیست پاسخ‌ها برای کامنت والد
            commentList = parentComment.querySelector('ul');

            // اگر لیست پاسخ‌ها وجود ندارد، آن را ایجاد کنیم
            if (!commentList) {
                commentList = document.createElement('ul');
                parentComment.appendChild(commentList);
            }
        } else {
            // در غیر این صورت، کامنت باید در لیست اصلی کامنت‌ها قرار گیرد
            commentList = document.querySelector('.sidebar-item.comments .content ul');
        }

        // ساختار HTML کامنت جدید
        const newComment = document.createElement('li');
        newComment.innerHTML = `
            <div class="author-thumb">
                <img src="${comment.profile_image}" style="vertical-align: middle;width: 50px;height: 50px; border-radius: 50%;" alt="user-image">
            </div>
            <div class="right-content">
                <h4>${comment.user}<span>${comment.created_at}</span></h4>
                <p>${comment.body}</p>
                ${parentId ? '' : `<button onclick="set_value(${comment.id})" class="btn btn-primary" data-comment-id="${comment.id}">Reply</button>`}
            </div>
        `;

        // افزودن کامنت به لیست کامنت‌ها
        commentList.appendChild(newComment);

        // اسکرول کردن به پایین برای دیدن کامنت جدید
        window.scrollTo(0, document.body.scrollHeight);
    }

});
