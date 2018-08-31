var container = document.getElementById('visualization');
var dataset = new vis.DataSet();

var options = {
	moveable: false,
	zoomable: false,
	drawPoints: false,
}

var graph2d = new vis.Graph2d(container, dataset, options);

function fetch(topic) {
  $.getJSON( "/histogram",
    {"topic": topic}
  ).done(function(data){
	dataset.clear();
	console.log(dataset);
    dataset.update(data);
	graph2d.fit();
 });
}

var urlParams = new URLSearchParams(window.location.search);
var topics = urlParams.get('topics');
fetch(topics)
setInterval(fetch, 5000, topics)
