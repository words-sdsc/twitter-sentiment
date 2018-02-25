var map;
var sentiment;
var volume;

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
    geolocation = latlng.lat + "," +  latlng.lng + "," +
                  Math.floor(radius / 1000) + "km";
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

var HashtagsControl = L.Control.extend({
  options: {
    position: 'bottomleft',
  },
  onAdd: function(map) {
    var div = L.DomUtil.create('div');

    div.id = "hashtags-container";
    div.innerHTML = `
      <ul>
      <li class="orange"><a href="#"></a></li>
      <li class="purple"><a href="#"></a></li>
      <li class="green"><a href="#"></a></li>
      </ul>`;

    L.DomEvent.disableClickPropagation(div);

    return div;
  }
});
var hashtagsControl = new HashtagsControl();

var SearchControl = L.Control.extend({
  options: {
    position: 'topright',
    type: 'text',
    name: 'hashtag',
    placeholder: 'Twitter Hashtag (e.g. #sdsc)'
  },
  onAdd: function(map) {
    var input = L.DomUtil.create('input', 'hashtag-input');

    input.type = this.options.type;
    input.placeholder = this.options.placeholder;
    input.name = this.options.name;

    L.DomEvent.disableClickPropagation(input);

    L.DomEvent.on(input, 'keydown', function(e) {
      if (e.keyCode === 13) {
        $(".highcharts").show();
        message = {'hashtag': input.value, 'flow type': 'live'};

        if (hasActiveShape(drawnItems, L.Rectangle))
          message['bounding box'] = boundingBox;
        else if (hasActiveShape(drawnItems, L.Circle))
          message['geolocation'] = geolocation;

        socket.emit('start_stream', message);
      }
    });

    return input;
  }
});

var searchControl = new SearchControl();

var ChartControl = L.Control.extend({
  options: {
    position: 'bottomright'
  },
  onAdd: function (map) {
    var container = L.DomUtil.create('div', 'highcharts');
    var table = L.DomUtil.create('table');
    var tbody = L.DomUtil.create('tbody');

    var tr = Array(3).fill().map((_,i) => L.DomUtil.create('tr'));
    var td = Array(3).fill().map((_,i) => L.DomUtil.create('td'));

    var sentiment = L.DomUtil.create('div');
    var volume = L.DomUtil.create('div');

    sentiment.id = 'sentiment';
    volume.id = 'volume';

    container.appendChild(table);
    table.appendChild(tbody);

    tr.forEach((r) => tbody.appendChild(r));
    td.forEach((d, i) => tr[i].appendChild(d));

    td[1].appendChild(sentiment)
    td[2].appendChild(volume);
    return container
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

  var baseMaps = {
    'Streets': streets,
    'Outdoors': outdoors,
    'Satellite': satellite
  };

  map = L.map('map', {
    center: [36.89, -119.58],
    zoom: 6,
    layers: [streets]
  });

  L.control.layers(baseMaps).addTo(map);

  map.addLayer(drawnItems);
  map.addControl(drawnControl);
  map.addControl(searchControl);
  map.addControl(hashtagsControl);
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
  volume = Highcharts.chart('volume', {

    title:   {text: 'Sentiment Volume'},
    credits: {enabled: false},

    chart: {
      width: 500,
      height: 300
    },

    exporting: {
      buttons: {
        contextButton: {enabled: false}
      }
    },

    yAxis: {
      min: 0,
      title: {
        text: 'Volume'
      }
    },

    xAxis: {
      type: 'datetime',
      title: {
        text: 'Date'
      },
      startOnTick: true,
      endOnTick: true,
      showLastLabel: true
    },

    series: [{
      name: 'Unique Tweets',
      data: []
    },
    {
      name: 'Total',
      data: []
    }]
  });

  sentiment = Highcharts.chart('sentiment', {

    title:   { text: 'Sentiment Analysis' },
    credits: { enabled: false },

    lang: {
      empty: ''
    },

    chart: {
      type: 'scatter',
      zoomType: '',
      width: 500,
      height: 300
    },


    exporting: {
      buttons: {
        contextButton: {
          enabled: false
        },
        exportingButton: {
          text: '',
          _titleKey: 'empty',
          onclick: function(e) {
            socket.emit('stop_stream');
            $('.highcharts').hide();
          },
          symbol: 'exit'
        }
      }
    },

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
        }

      }
    },

    series: [{
      name: 'Tweets',
      zones: Zones,
      data: []
    },
    {
      name: 'Retweets',
      zones: Zones,
      data: []
    }]
  });


  /* AJAX call to get the top 3 hashtags on CALFIRE */
  $.ajax({
    url: protocol + '//' + domain + ':' + port + '/hashtags',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      const nodes = Array.from(getChildrenOfElement('hashtags-container', 'a'));
      const zipped = nodes.map(function(node, i) {
        return [node, data['result'][i]];
      });

      zipped.forEach(function(elem) {
        elem[0].innerHTML = elem[1];
      });
    },
    error: function (request, error) {
    }
  });

  const nodes = Array.from(getChildrenOfElement('hashtags-container', 'a'));
  nodes.forEach(function(node) {
    node.addEventListener('click', function(e) {
      const hashtag = node.innerHTML;
      $('.highcharts').show();
      socket.emit('start_stream', {'hashtag': hashtag, 'flow type': 'live'});
    });
  });

  /* Websockets */

  // Event handler for server sent data.
  // The callback function is invoked whenever the server emits data
  // to the client. The data is then displayed in the "Received"
  // section of the page.
  var unique = 0;
  var total = 0;
  socket.on('response', function(msg) {
    var milliseconds = Date.parse(msg.created_at);
    var now = Date.now();
    total = total + 1;

    // Dynamically add points to the first series
    if( msg.retweeted ) {
      unique = unique + 1;
      sentiment.series[1].addPoint([milliseconds, msg.sentiment * 100]);
      volume.series[0].addPoint([now, unique]);
    } else {
      sentiment.series[0].addPoint([milliseconds, msg.sentiment * 100]);
    }
    volume.series[1].addPoint([now, total]);
  });

  $("#disconnect-btn").click(function() {
    socket.emit('stop_stream');
    return false;
  });
});
