document.addEventListener('DOMContentLoaded', function() {
    var es = new EventSource('/sse');
    es.onmessage = function (event) {
        var messages_dom = document.getElementById('messages');
        var message_dom = document.createElement('p');
        var content_dom = document.createTextNode(event.data);
        message_dom.appendChild(content_dom);
        messages_dom.appendChild(message_dom);
    };
});

