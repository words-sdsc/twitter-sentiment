var Colors = {
  // Negative - Red
  red: 'rgba(247, 46, 70, .5)',

  // Neutral - Blue
  blue: 'rgba(81, 185, 255, .5)',

  // Positive - Green
  green: 'rgba(48, 229, 81, .5)'
};

var map;
var chart;

var namespace = '/streaming';
var protocol = location.protocol;
var port = location.port;
var domain = document.domain;

// Connect to the Socket.IO server.
// The connection URL has the following format:
//     http[s]://<domain>:<port>[/<namespace>]
var socket = io.connect(protocol + '//' + domain + ':' + port + namespace);

var drawnItems = new L.FeatureGroup();
var drawOptions = {
  position: 'topleft',
  draw: {
    polyline: false,
    polygon:  false,
    circle:   false,
    rectangle: {
      shapeOptions: { color: '#5A0888', weight: 4 }
    }
  },
  edit: {
    featureGroup: drawnItems
  }
};
var drawnControl = new L.Control.Draw(drawOptions);

var HashTagControl = L.Control.extend({
  options: {
    position: 'topright',
    type: 'text',
    name: 'hashtag',
    placeholder: 'Twitter Hashtag (e.g. #sdsc)'
  },
  onAdd: function (map) {
    var input = L.DomUtil.create('input', 'hashtag-input');

    input.type = this.options.type;
    input.placeholder = this.options.placeholder;
    input.name = this.options.name;

    L.DomEvent.disableClickPropagation(input);

    L.DomEvent.on(input, 'keydown', function(e) {
      if (e.keyCode === 13) {
        socket.emit('start_stream', { hashtag : input.value });
      }
    });

    return input;
  }
});
var hashtagControl = new HashTagControl();

var ChartControl = L.Control.extend({
  options: {
    position: 'bottomright'
  },
  onAdd: function (map) {
    var div = L.DomUtil.create('div');
    div.id = 'highcharts-chart-container';
    return div
  }
});
var chartControl = new ChartControl();

$(function() {
  /* Leaflet */
  map = L.map('leaflet-map-container', { center: [38.4404, -122.7141], zoom: 13});

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      maxZoom: 18,
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
      '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="http://mapbox.com">Mapbox</a>',
      id: 'mapbox.streets',
      accessToken: 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
  }).addTo(map);

  map.addLayer(drawnItems);
  map.addControl(drawnControl);
  map.addControl(hashtagControl);
  map.addControl(chartControl);

  map.on(L.Draw.Event.CREATED, function (e) {
    if (e.layerType === 'rectangle')
      console.log(e.layer.getLatLngs());
    drawnItems.addLayer(e.layer);
  });

  /* Highcharts */
  chart = Highcharts.chart('highcharts-chart-container', {
    credits: {
      enabled: false
    },
    // Declare chart type and basic information
    chart: {
      type: 'scatter',
      zoomType: '',
      height: 400,
      width: 500
    },
    title: {
      text: 'Sentiment Over Time '
    },
    // Set up xAxis Attributes
    xAxis: {
      type: 'datetime',
      title: {
        text: 'Date'
      },
      startOnTick: true,
      endOnTick: true,
      showLastLabel: true
    },
    yAxis: {
      lineWidth: 1,
      min: -100,
      max: 100,
      title: {
        text: 'Sentiment'
      }
    },
    plotOptions: {
      scatter: {
        // Allows for dictionary format despite high data amount > 1000
        turboThreshold: 0,

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
        point: {
          events: {
            click: function() {
              alert("Tweet Text:\n" + this.text);
              console.log("This x = " + this.x);
              console.log("This y = " + this.y)
              //console.log("This tweetID = " + this.tweetId);
              console.log("This tweetText = " + this.text)
            }
          }
        }
      }
    },

    series: [{
      // Title of Each Point
      name: 'Sentiment',

      // Change colors based on POSITIVE, NEGATIVE, NEUTRAL
      zones: [
      {
        // Negative
        value: -5,
        color: Colors.red
      }, {
        // Neutral
        value: 5,
        color: Colors.blue
      }, {
        // Positive
        color: Colors.green
      }
      ],

      //pointInterval: 1000,

      // Pointer description
      pointDescriptionFormatter: function() {
        return 'The value for <b>' + this.x + '</b> is <b>' + this.y + '</b>, in series '+ this.series.name;
      },
      data: []
    },
    {	// Series dedicated for retweets

      // Display Linear Regression
      regression: true,
      regressionSettings: {
        type: 'polynomial',
        color:  'rgba(229, 70, 52, .7)'
      },

      // Title of Each Point
      name: 'Sentiment',

      // Change colors based on POSITIVE, NEGATIVE, NEUTRAL
      zones: [
      {
        // Negatie
        value: -5,
        color: Colors.red
      }, {
        // Neutral
        value: 5,
        color: Colors.blue
      }, {
        // Positive
        color: Colors.green
      }
      ],

      //pointInterval: 1000,

      // Pointer description
      pointDescriptionFormatter: function() {
        return 'The value for <b>' + this.x + '</b> is <b>' + this.y + '</b>, in series '+ this.series.name;
      },
      data: []
    }]
  });


  $('#hideRetweets').click(function () {
    console.log("Hide retweets")
      chart.series[1].hide();
  });
  $('#showRetweets').click(function () {
    console.log("Show retweets")
      chart.series[1].show();
  });

  /* Websockets */

  // Event handler for server sent data.
  // The callback function is invoked whenever the server emits data
  // to the client. The data is then displayed in the "Received"
  // section of the page.
  socket.on('response', function(msg) {
    $('#log').append('<br>' + $('<div/>')
             .text('Received #' + msg.sentiment + ': ' + msg.text + " AT " + msg.created_at)
             .html());
    console.log("Retweeted: " + msg.retweeted);

    var milliseconds = Date.parse(msg.created_at);
    // Dynamically add points to the first series
    if( msg.retweeted ) {
      chart.series[1].addPoint([milliseconds, msg.sentiment * 100]);
      //chart.series[1].addPoint(msg.sentiment * 100, true, false, true);
    } else {
      chart.series[0].addPoint([milliseconds, msg.sentiment * 100]);
      //chart.series[0].addPoint(msg.sentiment * 100, true, false, true);
    }
  });

  // Interval function that tests message latency by sending a "ping"
  // message. The server then responds with a "pong" message and the
  // round trip time is measured.
  var ping_pong_times = [];
  var start_time;
  window.setInterval(function() {
    start_time = (new Date).getTime();
    socket.emit('my_ping');
  }, 1000);

  // Handler for the "pong" message. When the pong is received, the
  // time from the ping is stored, and the average of the last 30
  // samples is average and displayed.
  socket.on('my_pong', function() {
    var latency = (new Date).getTime() - start_time;
    ping_pong_times.push(latency);
    ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
    var sum = 0;
    for (var i = 0; i < ping_pong_times.length; i++)
      sum += ping_pong_times[i];
    $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
  });
});

