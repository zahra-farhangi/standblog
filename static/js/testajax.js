// function like(slug, id){
//     var element = document.getElementById("like")
//     var count = document.getElementById("count")
//     $.get(`/articles/like/${slug}/${id}`).then(response =>{
//         if(response['response'] === "liked"){
//             element.className = "fa fa-heart"
//             count.innerText = Number(count.innerText) + 1
//         }else{
//             element.className = "fa fa-heart-o"
//             count.innerText = Number(count.innerText) - 1
//         }
//     })
// }


function like(slug, id) {
    const csrfToken = $('meta[name="csrf-token"]').attr('content'); // گرفتن CSRF Token

    const element = document.getElementById("like");
    const count = document.getElementById("count");

    $.ajax({
        url: `/articles/like/${slug}/${id}/`,
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            if (response.response === "liked") {
                element.className = "fa fa-heart";
                count.innerText = Number(count.innerText) + 1;
            } else if (response.response === "unliked") {
                element.className = "fa fa-heart-o";
                count.innerText = Number(count.innerText) - 1;
            }
        },
        error: function(xhr) {
            if (xhr.status === 403 || xhr.status === 405) {
                window.location.href = '/account/login/';
            } else {
                console.log("Error: " + xhr.status + " " + xhr.statusText);  // نمایش خطا در کنسول
            }
        }
    });
}
