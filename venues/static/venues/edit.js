document.addEventListener('DOMContentLoaded', function (e) {

    let edit_button = document.querySelector('#edit-button');
    let save_button = document.querySelector('#save-button');

    edit_button.addEventListener('click', function () {
        let venue_data = edit_button.dataset;
        document.querySelector('#venue-container').style.display = 'none';
        let edit_form = document.querySelector('#venue-edit-container');
        edit_form.style.display = 'block';

        let address_field = edit_form.querySelector('#venue-address');
        let description_field = edit_form.querySelector('#venue-description');
        let url_field = edit_form.querySelector('#venue-url');

        address_field.value = venue_data.address;
        address_field.style.color = 'grey';

        description_field.value = venue_data.description;
        description_field.style.color = 'grey';

        url_field.value = venue_data.url;
        url_field.style.color = 'grey';


        save_button.addEventListener('click', element => {

            let csrftoken = getCookie('csrftoken');
            let name = venue_data.name;
            let id = document.querySelector('#edit-button').dataset.venue;
            let data = JSON.stringify({
                'id': id,
                'name': name,
                'description': description_field.value,
                'address': address_field.value,
                'url': url_field.value,
            });
            window.event.preventDefault();

            fetch('/edit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: data,
                    credentials: 'same-origin'
                })
                .then(response => response.json())
                .then(data => {
                    edit_form.style.display = 'none';
                    edit_button.dataset.address = data.address;
                    edit_button.dataset.url = data.url;
                    edit_button.dataset.description = data.description;
                    document.querySelector('address').innerHTML = data.address;
                    document.querySelector('#url').setAttribute('href', data.url);
                    document.querySelector('#description').innerHTML = data.description;
                    document.querySelector('#venue-container').style.display = 'block';
                    var venue = data.name;
                    let text = `La venue ${venue} è stata modificata con successo.`;
                    $(".modal-body").html(text);
                    $('#edit-modal').modal();
                })
        })
    })
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}