var messages = [];

// function printMessage(){
// 	if (messages.length == 0) {
// 		return 
//     }
// 	var messages_dom = document.getElementById('seamless-scrollarea');
//
// 	var do_scroll = (messages_dom.scrollTop + messages_dom.offsetHeight) >= messages_dom.scrollHeight
//
// 	var df = document.createDocumentFragment();
// 	for (var idx in messages) {
// 		var li = document.createElement('li');
// 		li.appendChild(document.createTextNode(messages[idx]));
// 		df.appendChild(li);
// 	}
// 	messages_dom.appendChild(df);
// 	messages = [];
// 	var message_count = messages_dom.getElementsByTagName('li').length;
// 	message_dom.scrollIntoView();
// 	if (message_count > 5000){
// 		messages_dom.removeChild(messages_dom.firstChild);
// 	}
//
// 	if (do_scroll) {
// 		messages_dom.scrollTop = messages_dom.scrollHeight;
// 	}
// }



data = [];

function listening(topics) {
    if (topics) {
        var es = new EventSource('/sse?topics='+topics);
    } else {
        var es = new EventSource('/sse');
    }
	es.onerror = function () {
		console.log('event error. retry.');
		es.close();
		listening(topics);
	}
    es.onmessage = function (event) {
        console.log('on message');
        var text = document.createTextNode(event.data);
		data.push(text);
    	scrollBlockBottom(getBlockDataMaxBlock() - 1);
    };
}

document.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var topics = urlParams.get('topics');
	// setInterval(printMessage, 1000);
	listening(topics);
});

seamlessInitialize(0);
