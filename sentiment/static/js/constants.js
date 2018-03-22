var Mapbox = {
  satellite   : 'mapbox.satellite',
  streets     : 'mapbox.streets',
  outdoors    : 'mapbox.outdoors',
  url         : 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.pn' +
                'g?access_token={accessToken}',
  attribution : 'Map data &copy; <a href="http://openstreetmap.org">' +
                'OpenStreetMap</a> contributors, <a href="http://'    +
                'creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA'   + 
                '</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  accessToken : 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBn' +
                'dHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
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

/* for each sentiment class, the value determines the upper boundary where the
 * sentiment zone extends on the highchart.
 *
 * NOTE: undefined means the zone stretches to the last value in the series
 */
var Boundary = {
  negative: -5,
  neutral:   5,
  positive: undefined
}

var Zones = [
  {
    value: Boundary.negative,
    color: Colors.red
  }, {
    value: Boundary.neutral,
    color: Colors.blue
  }, {
    value: Boundary.positive,
    color: Colors.green
  }
];
