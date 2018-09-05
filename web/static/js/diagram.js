var container = document.getElementById('visualization');
var groups = new vis.DataSet();
groups.add({
	id: 0,
	style: {strock: 'blue'}
})
var dataset = new vis.DataSet();

var options = {
	moveable: false,
	zoomable: false,
	drawPoints: false,
}

var graph2d = new vis.Graph2d(container, dataset, options);

function fetch(topic, start, end, interval) {
  $.getJSON( "/histogram",
    {"topic": topic, "start": start, "end": end, "interval": interval}
  ).done(function(data){
	dataset.clear();
    dataset.update(data);
	graph2d.fit();
 });
}

var urlParams = new URLSearchParams(window.location.search);
var topics = urlParams.get('topics');
var start = urlParams.get('start');
var end = urlParams.get('end');
var interval = urlParams.get('interval');
if (interval === null) {
	interval = 5000;
}
fetch(topics, start, end, interval)
setInterval(fetch, interval, topics, start, end, interval)
