document.addEventListener('DOMContentLoaded', function() {
	var urlParams = new URLSearchParams(window.location.search);
	var topics = urlParams.get('topics');
	if (topics) {
		var es = new EventSource('/sse?topics='+topics);
	} else {
		var es = new EventSource('/sse');
	}
    es.onmessage = function (event) {
        var messages_dom = document.getElementById('messages');
        var message_dom = document.createElement('p');
        var content_dom = document.createTextNode(event.data);
        message_dom.appendChild(content_dom);
        messages_dom.appendChild(message_dom);
    };
});

