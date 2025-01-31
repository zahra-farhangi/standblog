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
        commentForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const body = document.getElementById('body').value.trim();
            const parentId = document.getElementById('parent_id').value || null;

            if (!body) {
                alert('بخش ارسال نظر نمی‌تواند خالی باشد.');
                return;
            }

            try {
                const response = await fetch(commentForm.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({
                        body: body,
                        parent_id: parentId,
                    }),
                });

                const contentType = response.headers.get('content-type');

                if (!response.ok) {
                    throw new Error(`خطای سرور: ${response.status} - ${response.statusText}`);
                }

                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();

                    if (data.error) {
                        throw new Error(data.error);
                    }

                    // ✅ اضافه کردن کامنت به DOM
                    const newComment = addCommentToDOM(data.comment, parentId);

                    // ✅ بعد از اضافه شدن کامنت، اسکرول را روی آن اجرا کنیم
                    setTimeout(() => {
                        newComment.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 200);

                    // ✅ پاک کردن فیلدها
                    commentForm.reset();
                    document.getElementById('parent_id').value = '';

                } else {
                    throw new Error('پاسخ نامعتبر از سرور (احتمالاً JSON نیست)');
                }

            } catch (error) {
                console.error('Error:', error);
                alert(`خطا: ${error.message}`);
            }
        });
    }

    function addCommentToDOM(comment, parentId) {
        let commentList;

        if (parentId) {
            const parentComment = document.querySelector(`.btn-primary[data-comment-id="${parentId}"]`).closest('li');
            commentList = parentComment.querySelector('ul');

            if (!commentList) {
                commentList = document.createElement('ul');
                commentList.classList.add('replies');
                parentComment.appendChild(commentList);
            }
        } else {
            commentList = document.querySelector('.sidebar-item.comments .content ul');
        }

        const newComment = document.createElement('li');

        // ✅ رفع خطای DOMTokenList
        if (parentId) {
            newComment.classList.add('replied');
        }

        newComment.innerHTML = `
            <div class="author-thumb">
                <img src="${comment.profile_image}" style="vertical-align: middle;width: 50px;height: 50px; border-radius: 50%;" alt="user-image">
            </div>
            <div class="right-content">
                <h4>${comment.user}<span>${comment.created_at}</span></h4>
                <p>${comment.body}</p>
                ${parentId ? '' : `<button onclick="set_value(${comment.id})" class="btn btn-primary mb-3" data-comment-id="${comment.id}">Reply</button>`}
            </div>
        `;

        commentList.insertBefore(newComment, commentList.firstChild);
        return newComment;
    }
});
