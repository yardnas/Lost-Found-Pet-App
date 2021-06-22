"use strict";

// Goal: To create a map with markers from stored information on the database
//
// done: Set current location or enter neighborhood address
// done: Convert address to lat/long for marker OR use address if there is a way
// done: Utilize the geocode to enter "location" (golden gate bridge) opposed address
//

/*-------------------------------------------------------------------*/
/*-------------------- Main Map Function Section --------------------*/
/*-------------------------------------------------------------------*/

/*---------- Start of the Map Function -----------*/

// Attach all event listeners in this function where the 'map' obj is in-scope
// Initialize the google map
function initMap() {

  // Create a new instance of Google Maps called "map"
  const map = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: {
          // Set to SF coordinates to start
          lat: 37.601773,
          lng: -122.202870
        },
        zoom: 10,
      }
  );

  /*-------- Pet Info Window & Marker section ------*/

  // Set info window to display the marker's info based on jsonify "pets" in server
  const petInfo = new google.maps.InfoWindow({});

  $.get('/get/pets', (pets) => { 
      for (const pet of pets) {

        // Define the content of the infoWindow 
        // Use JS template literals (backticks) - similar to f-string in python
        // Using backticks (`) aka: template literals, to add jQuery into HTML 
        const petInfoContent = (` 
          <div class="window-content">
            <div class="pet-thumbnail">
              <img src="${pet.petImage}" width="150" height="130"></img>
            </div>
  
            <ul class="pet-info">
              <li><b>Pet name: </b> ${pet.petName} </li>
              <li><b>Pet breed: </b> ${pet.petBreed} </li>
              <li><b>Pet color: </b> ${pet.petColor} </li>
              <li><b>Last seen: </b> ${pet.lastAddress} </li>
              <li><b>Pet owner: </b> ${pet.petOwner}</li>
            </ul>
          </div>
        `);

          // Define latitude and longitude needed for marker
          // Use geocode to convert an address to its latitude and longitude
          const geocoder = new google.maps.Geocoder();
          const address = `${pet.lastAddress}`

          geocoder.geocode( { 'address': address}, function(results, status) {
        
          if (status == google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();

            // Define marker and set position by lat and long
            // For marker: position is required (latlng)
            const petMarker = new google.maps.Marker({
              position: {
                  lat: latitude,
                  lng: longitude
              },
              title: `Pet ID: ${pet.petId}`,
              map: map,
              icon: { // custom icon
                url: '/static/img/paw_marker.png',
                scaledSize: {
                  width: 40,
                  height: 40
                }
              }
            });

            // Define event handling when marker is clicked
            // To show pet information content for each marker
            petMarker.addListener('click', (evt) => {
              console.log(evt) // for testing

              petInfo.close()
              petInfo.setContent(petInfoContent);
              petInfo.open(map, petMarker);

            });

          }           
        }); 
      }
    }).fail(() => {
        alert((`Not able to retrieve pet data`));
    });

  /*--------------- Style Map section --------------*/
  
  // Create a style map in night mode
  // TODO: Add style map to the maptypeid
  $('#custom-style').on('click', () => {
    const customStyledMap = new google.maps.StyledMapType(
      [
        { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
        { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
        { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
        {
          featureType: "administrative.locality",
          elementType: "labels.text.fill",
          stylers: [{ color: "#d59563" }],
        },
        {
          featureType: "poi",
          elementType: "labels.text.fill",
          stylers: [{ color: "#d59563" }],
        },
        {
          featureType: "poi.park",
          elementType: "geometry",
          stylers: [{ color: "#263c3f" }],
        },
        {
          featureType: "poi.park",
          elementType: "labels.text.fill",
          stylers: [{ color: "#6b9a76" }],
        },
        {
          featureType: "road",
          elementType: "geometry",
          stylers: [{ color: "#38414e" }],
        },
        {
          featureType: "road",
          elementType: "geometry.stroke",
          stylers: [{ color: "#212a37" }],
        },
        {
          featureType: "road",
          elementType: "labels.text.fill",
          stylers: [{ color: "#9ca5b3" }],
        },
        {
          featureType: "road.highway",
          elementType: "geometry",
          stylers: [{ color: "#746855" }],
        },
        {
          featureType: "road.highway",
          elementType: "geometry.stroke",
          stylers: [{ color: "#1f2835" }],
        },
        {
          featureType: "road.highway",
          elementType: "labels.text.fill",
          stylers: [{ color: "#f3d19c" }],
        },
        {
          featureType: "transit",
          elementType: "geometry",
          stylers: [{ color: "#2f3948" }],
        },
        {
          featureType: "transit.station",
          elementType: "labels.text.fill",
          stylers: [{ color: "#d59563" }],
        },
        {
          featureType: "water",
          elementType: "geometry",
          stylers: [{ color: "#17263c" }],
        },
        {
          featureType: "water",
          elementType: "labels.text.fill",
          stylers: [{ color: "#515c6d" }],
        },
        {
          featureType: "water",
          elementType: "labels.text.stroke",
          stylers: [{ color: "#17263c" }],
        },
      ],
    );
    
    // Associate the styled map with the MapTypeId and set it to display
    map.mapTypes.set('map_style', customStyledMap);
    map.setMapTypeId('map_style');
  });

  /*--------- Find Specific Location on thhe Map --------*/

  // To find lost pets in the specified location, use geocode form field
  // Call geocodeAddress() when the geo-btn submit is clicked
  const geocoder = new google.maps.Geocoder();

  $('#geo_btn').on('click', () => {
    geocodeAddress(geocoder, map); 
  });

}

/*-------------------------------------------------------------------*/
/*------------------- Geocoding Function Section --------------------*/
/*-------------------------------------------------------------------*/

// Use geocode to zoom and add a marker on the map interactively
function geocodeAddress(geocoder, map) {
  const address = document.getElementById('address').value;

  geocoder.geocode({ address: address }, (results, status) => {
    if (status === 'OK') {

      // Zoom in on the geocode location on the map
      map.setCenter(results[0].geometry.location);
      map.setZoom(15);

      // Create marker on the map based on the geocode location
      new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
      });

    } else {
          alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}


  /* 
  https://developers.google.com/maps/documentation/javascript/geocoding
  Geocoding Request object literal conains the following fields:
      {
      address: string,
      location: LatLng,
      placeId: string,
      bounds: LatLngBounds,
      componentRestrictions: GeocoderComponentRestrictions,
      region: string
      }
  
  */

