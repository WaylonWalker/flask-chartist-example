var data = {
    'size': {
        'height': 300
    },
    'data': {
        'x': 'x',
        'type': 'line',
        'axes': {
            'Australia': 'y',
            'x': 'y'
        },
        'columns': [
        [
        'Australia',
        '14.6159',
        '14.92326',
        '15.16178',
        '15.34807',
        '15.51048',
        '15.69524',
        '15.90042',
        '16.13672',
        '16.40073',
        '16.6806',
        '16.95624',
        '17.20212',
        '17.41893',
        '17.6078',
        '17.78109',
        '17.97563',
        '18.19585',
        '18.41526',
        '18.62084',
        '18.83025',
        '19.05319',
        '19.29426',
        '19.53494',
        '19.76654',
        '19.99508',
        '20.23235',
        '20.48947',
        '20.74963',
        '21.00731',
        '21.26264',
        '21.51575'
        ],
        [
        'x',
        '1980',
        '1981',
        '1982',
        '1983',
        '1984',
        '1985',
        '1986',
        '1987',
        '1988',
        '1989',
        '1990',
        '1991',
        '1992',
        '1993',
        '1994',
        '1995',
        '1996',
        '1997',
        '1998',
        '1999',
        '2000',
        '2001',
        '2002',
        '2003',
        '2004',
        '2005',
        '2006',
        '2007',
        '2008',
        '2009',
        '2010'
        ]
        ]
    },
    'subchart': {
        'show': false
    },
    'point': {
        'show': false
    },
    'grid': {
        'x': {
            'show': false
        },
        'y': {
            'show': false
        }
    },
    'axis': {
        'x': {
            'tick': {
                'count': 10
            }
        },
        'y': {
            'tick': {
                'format': ''
            }
        },
        'y2': {
            'tick': {}
        }
    },
    'zoom': {}
};
data['axis']['y']['tick']['format'] = d3.format('')
data['axis']['y2']['tick']['format'] = d3.format('')
data['bindto']='#chart'
var chart = c3.generate(data);

function load_data(country) {
    var xhr = new XMLHttpRequest();

    xhr.open('GET', 'http://127.0.0.1:5000/' + country);
    xhr.send(null);
    results = JSON.parse(xhr.responseText.result)
    document.getElement
    return data

}



function updateChart(){
  var nation = $("#nation option:selected").text()

  var updatedData = $.get('/c3data/'.concat(nation));
  updatedData.done(function(results){

  var data = {
    labels: results.labels,
    series: [
      results.results
      ]
  };

  chart.load(updatedData.responseJSON)
  });

}



$( document ).ready(updateChart)
// $('#update').on('click', updateChart)
$('#nation').on('change', updateChart)