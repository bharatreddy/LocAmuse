// Javascript for the locamuse func
// Written by Bharat Kunduri


// Update the html with Our ratings



function cRatUpdate(locsAdd) {


    var cRat=document.getElementById("combined");
    var yRat=document.getElementById("yelp");
    var faRat=document.getElementById("fsall");
    var ftRat=document.getElementById("fstrnd");

    var clTel=document.getElementById("clickTeller");

    clTel.style.display = "none"
    
    

    if (cRat.style.display == "none") {
      cRat.style.display = "block";
    } 

    if (yRat.style.display == "block") {
      yRat.style.display = "none";
    }

    if (faRat.style.display == "block") {
      faRat.style.display = "none";
    }

    if (ftRat.style.display == "block") {
      ftRat.style.display = "none";
    }

    
    if ( locsAdd != undefined ) {
      initialize( locsAdd )

    }
    
    // {% for cloc in comlocs %}
    //   cRatAddList[acnt] = {{cloc.address}}
    // {% endfor %}
    // initialize( cRatAddList )

}

// Update the html with YELP ratings and ofcourse remove the previous one

function yRatUpdate(locsAdd) {


    var cRat=document.getElementById("combined");
    var yRat=document.getElementById("yelp");
    var faRat=document.getElementById("fsall");
    var ftRat=document.getElementById("fstrnd");

    var clTel=document.getElementById("clickTeller");

    clTel.style.display = "none"

    if (cRat.style.display == "block") {
      cRat.style.display = "none";
    } 

    if (yRat.style.display == "none") {
      yRat.style.display = "block";
    }

    if (faRat.style.display == "block") {
      faRat.style.display = "none";
    }

    if (ftRat.style.display == "block") {
      ftRat.style.display = "none";
    }

    if ( locsAdd != undefined ) {
      initialize( locsAdd )

    }

}

// Update the html with FS ratings and ofcourse remove the previous one

function fARatUpdate(locsAdd) {


    var cRat=document.getElementById("combined");
    var yRat=document.getElementById("yelp");
    var faRat=document.getElementById("fsall");
    var ftRat=document.getElementById("fstrnd");

    var clTel=document.getElementById("clickTeller");

    clTel.style.display = "none"

    if (cRat.style.display == "block") {
      cRat.style.display = "none";
    } 

    if (yRat.style.display == "block") {
      yRat.style.display = "none";
    }

    if (faRat.style.display == "none") {
      faRat.style.display = "block";
    }

    if (ftRat.style.display == "block") {
      ftRat.style.display = "none";
    }

  if ( locsAdd != undefined ) {
        initialize( locsAdd )

      }


}

// Update the html with FS Trending locations and ofcourse remove the previous one

function fTRatUpdate(locsAdd) {


    var cRat=document.getElementById("combined");
    var yRat=document.getElementById("yelp");
    var faRat=document.getElementById("fsall");
    var ftRat=document.getElementById("fstrnd");

    var clTel=document.getElementById("clickTeller");

    clTel.style.display = "none"

    if (cRat.style.display == "block") {
      cRat.style.display = "none";
    } 

    if (yRat.style.display == "block") {
      yRat.style.display = "none";
    }

    if (faRat.style.display == "block") {
      faRat.style.display = "none";
    }

    if (ftRat.style.display == "none") {
      ftRat.style.display = "block";
    }

    if ( locsAdd != undefined ) {
      initialize( locsAdd )

    }


}

// Google Map stuff

function initialize( addressList ) {

  // Some basic options

  var mapOptions = {
    zoom: 14,
    center: new google.maps.LatLng(37.23, -80.4178),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  // The map object
  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  // Set the traffic layer
  var trafficLayer = new google.maps.TrafficLayer();
  trafficLayer.setMap(map);

  // Set the weather and cloud layer
  var weatherLayer = new google.maps.weather.WeatherLayer({
    temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
  });
  weatherLayer.setMap(map);

  // comment out the cloud layer for now
  // var cloudLayer = new google.maps.weather.CloudLayer();
  // cloudLayer.setMap(map);

  // Check if we have any addresses to overplot
  if ( addressList!=undefined ){

    for(var i=0; i<addressList.length; i++){
            // Plot the marker and info box
            codeAddress(addressList[i],map)    
    }
    

  }
  

}

function loadScript() {

  var script = document.createElement('script');
  script.type = 'text/javascript';

  // srcString = 'https://maps.googleapis.com/maps/api/js?key='+process.env.GMAP_KEY+'&sensor=false&libraries=weather&' +
  //     'callback=initialize';

  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyA-XSopZ4PzDMfAdsJu-g0r9RRxBLA-PfU&sensor=false&libraries=weather&' +
      'callback=initialize';


  
  document.body.appendChild(script);


}


// Google geocoding address to lat-lon for plotting on the maps
function codeAddress(address, map) {
  var geocoder;
  geocoder = new google.maps.Geocoder();

  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      // plot the marker

      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          title:address
      });
      
      // Add a info window
      var iw1 = new google.maps.InfoWindow({
       content: address
     });

      // Add a listenere to plot the info window
      google.maps.event.addListener(marker, "click", function (e) { iw1.open(map, this); });

    } else {
      console.log('Geocode was not successful for the following reason: ' + status);
    }
  });
}



// The initial function to search for locations
// Taken from Google APIS examples

// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initLocSrch() {

  // add the jquery functionality
  var script = document.createElement('script');
  script.src = 'http://jqueryjs.googlecode.com/files/jquery-1.2.6.min.js';
  script.type = 'text/javascript';
  document.getElementsByTagName('head')[0].appendChild(script);

  // Create the autocomplete object, restricting the search
  // to geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
      { types: ['geocode'] });
  // When the user selects an address from the dropdown,
  // populate the address fields in the form.
  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    fillInAddress();
  });


}

// The START and END in square brackets define a snippet for our documentation:
// [START region_fillform]
function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();

  // get the formatted address  
  var formAddress = place['formatted_address']

  // this is the root location of the app
  // $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
  // console.log( $SCRIPT_ROOT )
  for (var component in componentForm) {
    document.getElementById(component).value = '';
    document.getElementById(component).disabled = false;
  }

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
      document.getElementById(addressType).value = val;
    }
  }
  // console.log(formAddress)
  var url = "http://localhost:5000/resdisp/"+formAddress;
  // console.log(place)
  window.open (url,'_self',false);



}
// [END region_fillform]

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = new google.maps.LatLng(
          position.coords.latitude, position.coords.longitude);
      autocomplete.setBounds(new google.maps.LatLngBounds(geolocation,
          geolocation));
    });
  }
}
// [END region_geolocation]
