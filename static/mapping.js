var JRoutingMapper = {
  updateMap: function (source, destination, time) {
  // Make request to /routing that responds with lat/long's for route
    $.ajax({
      url: 'routing',
      type: 'GET',
      data: {
        source: source,
        destination: destination,
        time: time
      },
      success: function (data) {
        // Update the line and symbol
        // JRoutingMapper.clearLines();
        var max_eta = 0
        for (var i = 0; i < data.etas.length; i += 1) {
          if (data.etas[i] > max_eta) {
            max_eta = data.etas[i]
          }
        };
        for (var i = 0; i < data.etas.length; i += 1) {
          JRoutingMapper.drawPolyline(data.points[i], data.etas[i], max_eta, i);
        };
        JRoutingMapper.writeOutput(data.etas);
      }
    })
  },

  // TODO: Make sure you clear old polylines and symbols
  drawPolyline: function (points, eta, max_eta, line_no) {
    var coords = [];
    for (var i = 0; i < points.length; i += 1) {
      coords.push(new google.maps.LatLng(points[i][0], points[i][1]));
    }
    
    var colors = ['blue', 'red', 'green', 'black'];
    
    var symbol = {
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        strokeColor: colors[line_no % colors.length]
      },
      offset: '100%'
    }

    // Create the polyline and add the symbol to it via the 'icons' property.
    var line = new google.maps.Polyline({
      path: coords,
      icons: [symbol],
      map: JRoutingMapper.map
    });

    JRoutingMapper.animateCircle(line, max_eta, eta);
  },

  animateCircle: function (line, max_eta, eta) {
    var count = 0;
    window.setInterval(function() {
      count = (count + 1) % (max_eta * 100);
      // speed += 0.01;
      var icons = line.get('icons');
      if (count / eta >= 100) {
        icons[0].offset = '100%';
      } else {
        icons[0].offset = (count / eta) + '%';
      };
      line.set('icons', icons);
    }, 5);
  },

  writeOutput: function (etas) {
    var colors = ['blue', 'red', 'green', 'black'];
    var clusters = ['Aggressive Drivers', 'Normal Drivers', 'Slow Drivers', 'Google Maps Route']
    var out = ''
    for (var i = 0; i < etas.length; i += 1) {
      out += "<div class='symbol' style='border: 6px solid " + colors[i%4] + ";'></div>"
      out += '<p>' + clusters[i] + '</p>'
      out += '<p>ETA: ' + String(etas[i]) + ' Minutes</p>'
    }
    document.getElementById('out-box').innerHTML=out;
  },

// <p><div #symbol style='color': blue></div>5</p>

  initialize: function () {
    
    var locations = [
      ['Bondi Beach', -33.890542, 151.274856, 4],
      ['Coogee Beach', -33.923036, 151.259052, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]
    ];

    var myLatlng = new google.maps.LatLng(37.7833, -122.4167);
    
    var mapOptions = {
      center: new google.maps.LatLng(37.7833, -122.4167),
      zoom: 13
    };

    JRoutingMapper.map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
      
    var marker, i;

    for (i = 0; i < locations.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
      });

    // When user has submitted source and destination
    $('#nav-box').find('form').on('submit', function (e) {
      e.preventDefault();
      var target = $(e.target);
      var source = target.find('input[name="source"]').val();
      var destination = target.find('input[name="destination"]').val();
      var time = target.find('select').val();
      JRoutingMapper.updateMap(source, destination, time);
    })

    var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Hello World!'
      });
  }
}

google.maps.event.addDomListener(window, 'load', JRoutingMapper.initialize);
