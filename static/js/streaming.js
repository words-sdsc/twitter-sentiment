function hasActiveShape(layerGroup, shapeType) {
  var flag = false;

  layerGroup.eachLayer( (layer) => {
    var color = layer.options.color;
    if (color === Colors.darkred && layer instanceof shapeType)
      flag = true;
  });

  return flag;
}


var Mapbox = {
  satellite: 'mapbox.satellite',
  streets: 'mapbox.streets',
  outdoors: 'mapbox.outdoors',
  url: 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?' +
    'access_token={accessToken}',
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">' +
    'OpenStreetMap</a> contributors, <a href="http://creativecommons.org/' +
    'licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.' +
    'com">Mapbox</a>',
  accessToken: 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3' +
    'gifQ.rJcFIG214AriISLbB6B5aw',
};

var Colors = {
  // Negative sentiment
  red: 'rgba(247, 46, 70, .5)',

  // Neutral sentiment
  blue: 'rgba(81, 185, 255, .5)',

  // Positive sentiment
  green: 'rgba(48, 229, 81, .5)',

  // Active bounding box
  darkred: '#893231',

  // Non-active bounding box
  black: '#000000'
};

var map;
var chart;

var boundingBox;
var geolocation;

var namespace = '/streaming';
var protocol = location.protocol;
var port = location.port;
var domain = document.domain;


// Connect to the Socket.IO server.
// The connection URL has the following format:
//     http[s]://<domain>:<port>[/<namespace>]
var socket = io.connect(protocol + '//' + domain + ':' + port + namespace);

var drawnItems = new L.FeatureGroup();

drawnItems.on('click', function(e) {

  const clickedLayer = e.layer;

  if (clickedLayer instanceof L.Circle) {
    const latlng = clickedLayer.getLatLng();
    const radius = clickedLayer.getRadius();
    geolocation = [latlng.lat, latlng.lng, radius / 1000];
  } else {
    const latlngs = clickedLayer.getLatLngs()[0];

    // retrieve only the southwest and northeast longtitude and latitude
    boundingBox = latlngs.filter((el, idx) => [0, 2].includes(idx));

    // transform into format accepted by Twitter API
    // [longtitude, latitude, longtitude, latitude]
    boundingBox = boundingBox.map( (elem) => [elem.lng, elem.lat] );
    boundingBox = [].concat.apply([], boundingBox);
  }


  if (clickedLayer.options.color == Colors.darkred)
    style = { color: Colors.black, weight: 2, opacity: 0.7}
  else
    style = { color: Colors.darkred, weight: 4, opacity: 0.9}

  clickedLayer.setStyle(style);

  drawnItems.eachLayer( (layer) => {
    if (layer !== clickedLayer) {
      layer.setStyle({ color: Colors.black, weight: 2, opacity: 0.7 });
    }
  });
});

var drawOptions = {
  position: 'topleft',
  draw: {
    polyline: false,
    polygon: false,
    circlemarker: false,
    marker: false,
    circle: {
      shapeOptions: { color: Colors.black, weight: 2, opacity: 0.7 }
    },
    rectangle: {
      shapeOptions: { color: Colors.black, weight: 2, opacity: 0.7 }
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
        $("#chart-container").show();
        message = {'hashtag': input.value, 'flow type': 'historical'};

        if (hasActiveShape(drawnItems, L.Rectangle))
          message['bounding box'] = bounding_box;

        socket.emit('start_stream', message);
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
    div.id = 'chart-container';
    return div
  }
});
var chartControl = new ChartControl();

$(function() {
  /* Leaflet */

  var satellite = L.tileLayer(Mapbox.url, {
    id: Mapbox.satellite,
    attribution: Mapbox.attribution,
    accessToken: Mapbox.accessToken
  });
  var streets = L.tileLayer(Mapbox.url, {
    id: Mapbox.streets,
    attribution: Mapbox.attribution,
    accessToken: Mapbox.accessToken
  });
  var outdoors = L.tileLayer(Mapbox.url, {
    id: Mapbox.outdoors,
    attribution: Mapbox.attribution,
    accessToken: Mapbox.accessToken
  });


  map = L.map('leaflet-map-container', {
    center: [36.89, -119.58],
    zoom: 6,
    layers: [streets]
  });

  var baseMaps = {
    'Streets': streets,
    'Outdoors': outdoors,
    'Satellite': satellite
  };

  var overlayMaps = {
    'Live': drawnItems,
    'Historical': drawnItems
  };

  L.control.layers(baseMaps).addTo(map);

  map.addLayer(drawnItems);
  map.addControl(drawnControl);
  map.addControl(hashtagControl);
  map.addControl(chartControl);

  map.on(L.Draw.Event.CREATED, function (e) {
    drawnItems.addLayer(e.layer);
  });


  /* Generating a cross symbol to place on sentiment analysis charts. The
   * cross symbol is meant to close down the chart and stop the stream flow when
   * clicked.
   */
  $.extend(Highcharts.Renderer.prototype.symbols, {
      exit: function(x, y, width, height) {
        return [ "M", x, y,
                 "L", x + width, y + height,
                 "M", x, y + height,
                 "L", x + width, y ]
      }
  });

  /* Chart configuration */
  chart = Highcharts.chart('chart-container', {
    credits: {
      enabled: false
    },
    lang: {
      empty: ''
    },
    chart: {
      type: 'scatter',
      zoomType: '',
      height: 400,
      width: 500
    },
    title: {
      text: 'Sentiment Over Time '
    },
    exporting: {
      buttons: {
        contextButton: {
          enabled: false
        },
        exportingButton: {
          text: '',
          _titleKey: 'empty',
          symbol: 'exit'
        }
      }
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
    console.log("Hide retweets");
    chart.series[1].hide();
  });
  $('#showRetweets').click(function () {
    console.log("Show retweets");
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

  $("#disconnect-btn").click(function() {
    socket.emit('stop_stream');
    return false;
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
