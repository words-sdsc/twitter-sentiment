function displayChart(chartData) {
  $(function() {
    $('#container').highcharts({
      chart: {
        type: 'scatter',
        zoomType: 'xy'
      },
      title: {
        text: 'Sentiment Over Time ({{table_choice}})'
      },
      subtitle: {
        text: 'Made with <3'
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

        series: {
          dateGrouping: {
              approximation: 'average',
          }
        }
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
