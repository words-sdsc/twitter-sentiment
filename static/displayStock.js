function displayStock(idName, tableName, dataT) {
$.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {

    // Create the chart
    Highcharts.stockChart("container2", {

        // Range of display for data.. e.g. 1day, 4months, 13months
        rangeSelector: {
            selected: 4
        },

        // Graph Title
        title: {
            text: tableName
        },

        // xAXis Attributes
        xAxis: {
          title: {
            enabled: true,
            text: 'Date'
          },
          type: 'datetime',
          startOnTick: true,
          endOnTick: true,
          showLastLabel: true
        },

        // Plot options to average the data points
        plotOptions: {
            series: {
                // Allows for dictionary format despite high data amount > 1000
                turboThreshold: 0,

                // Average plots by day
                dataGrouping: {
                    forced: true,
                    units: [
                        ['day', [1]]
                    ]
                },

                // Execute JS onClick
                point: {
                    events: {
                        click: function() {
                            alert('Hello!2');
                            console.log("This x = " + this.x);
                            console.log("This y = " + this.y)
                            console.log("This tweetID = " + this.tweetId);
                        }
                    }
                }
            }
        },

        series: [{
            name: 'Cato',
            // Set up regression line
            regression: true,
            regressionSettings: {
                    type: 'polynomial',
                    color:  'rgba(229, 70, 52, .7)'
            },

            data: dataT,
            marker: {
                enabled: true,
                radius: 3
            },
            shadow: true,
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});
}
