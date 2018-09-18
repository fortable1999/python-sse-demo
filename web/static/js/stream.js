data = [];
function printMessage(){
	var do_scroll = (
		(getNextBlock() !== null && getNextBlock().offsetTop + getNextBlock().offsetHeight <= window.innerHeight) ||
		(getNextBlock() === null && getCurrentBlock().offsetTop + getCurrentBlock().offsetHeight <= window.innerHeight)
	)

	if (do_scroll) {
    	scrollBlockBottom(getBlockDataMaxBlock() - 1);
	}
}

function listening(topics) {
    if (topics) {
        var es = new EventSource('/sse?topics='+topics);
    } else {
        var es = new EventSource('/sse');
    }
	es.onerror = function () {
		es.close();
		listening(topics);
	}
    es.onmessage = function (event) {
		var text = event.data;
		data.push(text);
    	// scrollBlockBottom(getBlockDataMaxBlock() - 1);
    };
}

document.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var topics = urlParams.get('topic');
	setInterval(printMessage, 2000);
	listening(topics);
});

seamlessInitialize(0);
