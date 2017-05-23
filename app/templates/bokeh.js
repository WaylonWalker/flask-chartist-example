function updateChart(){
console.log('updated div/scripts')
  var nation = $("#nation option:selected").text()
  var updatedData = $.get('/pybokeh/'.concat(nation));

  updatedData.done(function(results){

    $("#bokeh-pop-plot").html(results.div);
    $("#bokeh-pop-script").html(results.script);


  });

  console.log('updated div/scripts')

}

$('#update').on('click', updateChart)
$('#nation').on('change', updateChart)