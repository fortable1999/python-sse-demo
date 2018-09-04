function listening(topics) {
    if (topics) {
        var es = new EventSource('/sse?topics='+topics);
    } else {
        var es = new EventSource('/sse');
    }
	es.onerror = function () {
		console.log('event error. retry.')
		es.close()
		listening(topics)
	}
    es.onmessage = function (event) {
        var messages_dom = document.getElementById('messages');
        var do_scroll = (messages_dom.scrollTop + messages_dom.offsetHeight) >= messages_dom.scrollHeight
        var message_dom = document.createElement('li');
        var content_dom = document.createTextNode(event.data);
        message_dom.appendChild(content_dom);
        messages_dom.appendChild(message_dom);
        // message_dom.scrollIntoView();
        if (do_scroll) {
            messages_dom.scrollTop = messages_dom.scrollHeight
        }
    };
}

document.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var topics = urlParams.get('topics');
	listening(topics);
});

