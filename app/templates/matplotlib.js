function updateChartSrc(){
    var nation = $("#nation option:selected").text()
    var updatedData = $.get('/mpl/'.concat(nation));
    updatedData.done(function(results){
        $("img[name=population]").attr("src", results.src)
    });
}



$("#nation").on('change', updateChartSrc);
