/**
 * Displays line chart on the web browser.
 * Param: idName - ID of tag that will be the chart's container
 *        title - Name of the SQL table chosen, (Graph Title)
 *        chartData - Array containing all the plot points of the chart
 *                    where each element = [plot.x (time), plot.y (sentiment)]
 */
function displayChart(idName, title, chartData) {
  // JQUERY Method to start up highcharts
  $(function() {
    $(idName).highcharts({
      // Declare chart type and basic information
      chart: {
        type: 'scatter',
        zoomType: 'xy'
      },
      title: {
        text: 'Sentiment Over Time ' + title
      },
      subtitle: {
        text: 'Made with <3'
      },

      // Set up xAxis Attributes
      xAxis: {
        title: {
          enabled: true,
          text: 'Date'
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
      },
      yAxis: {
        title: {
          text: 'Sentiment'
        }
      },
      legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 100,
        y: 70,
        floating: true,
        backgroundColor: '#FFFFFF',
        borderWidth: 1
      },

      plotOptions: {
        scatter: {
          marker: {
            radius: 5,
            states: {
              hover: {
                enabled: true,
                lineColor: 'rgb(100,100,100)'
              }
            }
          },
          states: {
            hover: {
              marker: {
                enabled: false
              }
            }
          }
        },
      },

      series: [{
        // Display Linear Regression
        regression: true,
        
        // Title of Each Point
        name: 'Sentiment',

        // Change colors based on POSITIVE, NEGATIVE, NEUTRAL
        zones: [
          {
              // Negatie - Red
              value: -5,
              color: 'rgba(247, 46, 70, .5)' 
          }, {
              // Neutral - Blue
              value: 5,
              color: 'rgba(81, 185, 255, .5)'
          }, {
              // Positive - Green
              color: 'rgba(48, 229, 81, .5)'
          }
        ],

        pointInterval: 86400000,

        // Pointer description
        pointDescriptionFormatter: function() {
          return 'The value for <b>' + this.x + '</b> is <b>' + this.y + '</b>, in series '+ this.series.name;
      },
          data: chartData
      }]
    });
  }); 
}
