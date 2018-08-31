var container = document.getElementById('visualization');
var dataset = new vis.DataSet({});
var graph2d = new vis.Graph2d(container, dataset);

function update(topic) {}
function fetch(topic) {
  $.getJSON( "/histogram",
    {"topic": topic}
  ).done(function(data){
	dataset.clear()
    dataset.update(data)
  });
}

var urlParams = new URLSearchParams(window.location.search);
var topics = urlParams.get('topics');
fetch(topics)
setInterval(fetch, 15000, topics)
