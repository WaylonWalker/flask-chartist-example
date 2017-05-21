var mychart;

var nation = $("#nation option:selected").text()
var getData = $.get('/data/'.concat(nation));

getData.done(function(results){

  var data = {
    labels: results.labels,
    series: [
      results.results
      ]
  };

  mychart = new Chartist.Line('.ct-chart', data);

})

function updateChart(){
  var nation = $("#nation option:selected").text()

  var updatedData = $.get('/data/'.concat(nation));

  updatedData.done(function(results){
  var data = {
    labels: results.labels,
    series: [
      results.results
      ]
  };

  mychart.update(data)
  });

}

$('#update').on('click', updateChart)
$('#nation').on('change', updateChart)