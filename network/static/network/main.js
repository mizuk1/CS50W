document.addEventListener('DOMContentLoaded', function () {
    // Listen for each edit button
    const editButtons = document.querySelectorAll(".edit");
    editButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            show_form(event);
        });
    });

    // Listen for each submit button
    const submitButtons = document.querySelectorAll(".edit-post");
    submitButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            edit_post(event, button.value);
        });
    });

    // Listen for each like button
    const likeButtons = document.querySelectorAll(".like");
    likeButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            send_like(event, button.dataset.number);
        });
    });
});

function show_form(event) {
    const element = event.target;
    const id = element.value;
    // Remove button
    element.style.display = 'none';

    // Show form
    const formElement = document.getElementById(id);
    formElement.style.display = 'block';
}

function edit_post(event, id) {
    const body = document.querySelector(`#text${id}`).value;

    fetch(`http://127.0.0.1:8000/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: body
        })
    })
        .then(response => response.json())
        .then(result => {
            document.querySelector(`button[value="${id}"].edit`).style.display = "block";
            const formElement = document.getElementById(id);
            formElement.style.display = 'none';
            document.querySelector(`p[value="${id}"]`).innerHTML = result.text;
        });
}


function send_like(event, id) {
    // Ask if user like the post
    fetch(`http://127.0.0.1:8000/like/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.liked == true) {
                fetch(`http://127.0.0.1:8000/rem_like/${id}`)
                    .then(response => response.json())
                    .then(result => {
                        document.querySelector(`p[data-p="${id}"]`).innerHTML = result.likes;
                    });
            } else {
                fetch(`http://127.0.0.1:8000/add_like/${id}`)
                    .then(response => response.json())
                    .then(result => {
                        document.querySelector(`p[data-p="${id}"]`).innerHTML = result.likes;
                    });
            }
        });
}