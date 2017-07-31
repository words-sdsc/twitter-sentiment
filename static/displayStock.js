function displayStock(data) {
    // $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {

        // Create the chart
        var chart = Highcharts.stockChart('container', {

            chart: {
                height: 400
            },

            title: {
                text: 'Highstock Responsive Chart'
            },
        xAxis: {
          title: {
            enabled: true,
            text: 'Date'
          },
          type: 'datetime',
            dateTimeLabelFormats: {
                second: '%Y-%m-%d<br/>%H:%M:%S',
                minute: '%Y-%m-%d<br/>%H:%M',
                hour: '%Y-%m-%d<br/>%H:%M',
                day: '%Y<br/>%m-%d',
                week: '%Y<br/>%m-%d',
                month: '%Y-%m',
                year: '%Y'
            },
          startOnTick: true,
          endOnTick: true,
          showLastLabel: true
        },
            subtitle: {
                text: 'Click small/large buttons or change window size to test responsiveness'
            },

            rangeSelector: {
                selected: 1
            },

            series: [{
                name: 'AAPL Stock Price',
                data: {{tweetsList}},
                type: 'area',
                threshold: null,
                tooltip: {
                    valueDecimals: 2
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        chart: {
                            height: 300
                        },
                        subtitle: {
                            text: null
                        },
                        navigator: {
                            enabled: false
                        }
                    }
                }]
            }
        });


        $('#small').click(function () {
            chart.setSize(400);
        });

        $('#large').click(function () {
            chart.setSize(800);
        });

        $('#auto').click(function () {
            chart.setSize(null);
        });
    // });
}
