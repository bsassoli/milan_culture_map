document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.follow-button').forEach(element =>
        element.addEventListener('click', (e) => {
            var follow_btn = e.target;
            if (follow_btn.dataset.action === 'unfollow') {                
                data = JSON.stringify({
                    'action': 'unfollow',
                    'venue': follow_btn.dataset.venue,
                });
            } 
            else {
                data = JSON.stringify({
                    'action': 'follow',
                    'venue': follow_btn.dataset.venue,
                });
            };
            follow(data);
        }))
})

function follow(data) {
    console.log('func');
    let csrftoken = getCookie('csrftoken');
    fetch('/follow', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: data,
            credentials: 'same-origin'
        })
    window.location.reload() // To refresh page.  
        
}


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