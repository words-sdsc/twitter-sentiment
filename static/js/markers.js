(function (window, document, undefined) {
  L.DisasterMarkers = {};
  L.DisasterMarkers.version = '0.0.1';
  L.DisasterMarkers.Icon = L.Icon.extend({
    options: {
      iconSize: [35, 45],
      iconAnchor: [17, 42],
      popupAnchor: [1, -32],
      shadowAnchor: [10, 12],
      shadowSize: [36, 16],
      className: 'disaster-marker',
      markerColor: 'blue',
      iconColor: 'white'
    },

    initialize: function (options) {
      options = L.Util.setOptions(this, options);
    },

    createIcon: function () {
      var div = document.createElement('div');
      var options = this.options;

      this._setIconStyle(div, 'icon-' + options.markerColor);
      return div;
    },

    createShadow: function () {
      var div = document.createElement('div');
      this._setIconStyle(div, 'shadow');
      return div;
    },

    _setIconStyle: function (marker, type) {
      var options = this.options,
      size = L.point(options[name === 'shadow' ? 'shadowSize' : 'iconSize']),
      anchor;

      if (name === 'shadow') {
        anchor = L.point(options.shadowAnchor || options.iconAnchor);
      } else {
        anchor = L.point(options.iconAnchor);
      }

      if (!anchor && size) {
        anchor = size.divideBy(2, true);
      }

      marker.className = 'disaster-marker-' + type + ' ' + options.className;

      if (anchor) {
        marker.style.marginLeft = (-anchor.x) + 'px';
        marker.style.marginTop  = (-anchor.y) + 'px';
      }

      if (size) {
        marker.style.width  = size.x + 'px';
        marker.style.height = size.y + 'px';
      }
    }
  });

  L.DisasterMarkers.icon = function (options) {
    return new L.DisasterMarkers.Icon(options);
  };

}(this, document));
