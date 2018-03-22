function displayMirroredVolume(idName, tableName, dataT) {
      var posData = [{}];
      var negData = [{}];
      // Parition positive and negatives, Duplicate neutrals
      for(var i = 0; i < dataT.length; i++) {          
          if(dataT[i]['y'] >=0 ) {
              posData.push({ x : dataT[i]['x'], y : dataT[i]['y'] });
          } 

          else if (dataT[i]['y'] <= 0 ) {
              negData.push({ x : dataT[i]['x'], y : dataT[i]['y'] });
          }
      }

    $(document).ready(function() {
       var chart =     // Create the chart
    Highcharts.stockChart("container4", {

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
            },

        },

        series: [{
            name: 'Positive Sentiment Count',
            type: 'area',

            data: posData,
            marker: {
                enabled: true,
                radius: 3
            },
            shadow: true,
            tooltip: {
                valueDecimals: 2
            },
            color: 'rgba(48, 229, 81, .5)' // Red

        },
        {
            name: 'Negative Sentiment Count',
            type: 'area',

            data: negData,
            marker: {
                enabled: true,
                radius: 3
            },
            shadow: true,
            tooltip: {
                valueDecimals: 2
            },
            color: 'rgba(247, 46, 70, .5)' // Green
        }]
    });

       //console.log(dataT);

    }); // End of doc ready function
} // End of display mirrored volume