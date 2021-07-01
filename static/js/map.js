// Google Map API functionality section //

"use strict";

/*-------------------------------------------------------------------*/
/*-------------------------- Scope: Map Section ---------------------*/
/*-------------------------------------------------------------------*/
//  MVP: 
//    [√] To create a map with markers from stored information on the database 
//    [√] Set current location or enter neighborhood address
//    [√] Convert address to lat/long for marker OR use address if there is a way
//    [√] Utilize the geocode to enter "location" (golden gate bridge) opposed address
//
//  Nice-to-have:
//    [√] Add zoom on click for existing markers
//    [√] Add pan to and marker when user click on map
//    [√] Geo locate my location
//    [√] Night mode for map
//    [ ] Add nightmode on map along side the map type nav (map|satellite)
//    [ ] Separate the map styles code block to another js file (mapStyles.js)

/*-------------------------------------------------------------------*/
/*------------------- Function: Main Map Section --------------------*/
/*-------------------------------------------------------------------*/

// Attach all event listeners to this function where the 'map' obj is in-scope
// 
function initMap() { 

  // Create a new instance of Google Maps called "map"
  // Set default coordinates to SF
  //
  const map = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: {
          // Set to SF coordinates to start
          // 37.62138086303597, -122.37901977480048
          // lat: 37.601773,
          // lng: -122.305419
          lat: 37.621380,
          lng: -122.379019
        },
        zoom: 10,
      }
  );

  // User can click on map to create a marker
  // Will place marker and pan to specified location
  //
  map.addListener("click", (e) => {
    placeMarkerAndPanTo(e.latLng, map);
  });

  /*--------------------------------------------------------*/
  /*----------- Pet Info Window & Marker section -----------*/
  /*--------------------------------------------------------*/

  // Set info window to display the marker's info based on jsonify "pets" in server
  const petInfo = new google.maps.InfoWindow({});

  $.get('/api/pets', (pets) => { 
      for (const pet of pets) {

        // Define the content of the infoWindow 
        // Using backticks (`) aka: template literals, to add jQuery into HTML
        //
        const petInfoContent = (` 
          <div class="window-content">
            <div class="pet-thumbnail">
              <img src="${pet.petImage}" width="155" height="130"></img>
            </div>

            <div class="pet-info">
              <b>Pet Name: </b> ${pet.petName}<br>
              <b>Contact: </b> <a href="mailto:${pet.userEmail}"> ${pet.userEmail} </a><br>
              <b>Pet Owner: </b> ${pet.petOwner}<br>
              <b>Pet Breed: </b> ${pet.petBreed}<br>
              <b>Pet Color: </b> ${pet.petColor}<br>
              <b>Last Seen: </b> ${pet.lastAddress}<br>
            </div>

          </div>
        `);

          // Define latitude and longitude needed for marker
          // Use geocode to convert an address to its latitude and longitude
          //
          const geocoder = new google.maps.Geocoder();
          const address = `${pet.lastAddress}`

          geocoder.geocode( { 'address': address}, function(results, status) {
        
          if (status == google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();

            // Define marker and set position by lat and long
            // For marker: position is required (latlng)
            //
            const petMarker = new google.maps.Marker({
              position: {
                  lat: latitude,
                  lng: longitude
              },
              // title: `Pet ID: ${pet.petId}`,
              title: `Pet Name: ${pet.petName}`,
              map: map,
              // animation: google.maps.Animation.DROP,
              icon: { // add a custom icon to mark lost pets
                url: '/static/img/paw_marker.png',
                scaledSize: {
                  width: 45,
                  height: 45
                }
              }
            });

            // Define event handling when marker is clicked
            // To show pet information content for each marker
            //
            petMarker.addListener('click', (evt) => {
              petInfo.close()
              petInfo.setContent(petInfoContent);
              petInfo.open(map, petMarker);
              map.setZoom(13);

            });
          }           
        }); 
      }
    }).fail(() => {
        alert((`Not able to retrieve pet data`));
    });

  /*--------------------------------------------------------*/
  /*------------------- Style Map section ------------------*/
  /*--------------------------------------------------------*/
  
  // Create a style map in night mode (google maps)
  // TODO: Add style map to the maptypeid
  //
  $('#custom-style').on('click', () => {
    const customMapType = new google.maps.StyledMapType(
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
      { name: "Styled Map" }
    );
    
    // Associate the styled map with the MapTypeId and set it to display
    //
    map.mapTypes.set('styled_map', customMapType);
    map.setMapTypeId('styled_map');
  });

  /*--------------------------------------------------------*/
  /*------------- Find Lost Pets on Map Section -------------*/
  /*--------------------------------------------------------*/

  // To find lost pets in the specified location, use geocode form field
  // Call geocodeAddress() when the geo-btn submit is clicked
  //
  const geocoder = new google.maps.Geocoder();

  $('#geo_btn').on('click', () => {
    geocodeAddress(geocoder, map); 
  });


  // On click, geo locate user's location
  // If browser supports and is enabled for location detection
  // TODO: Decide whether to incorporate (most people likely have privacy on)
  //
  $('#locate-me').on('click', () => {

    // If the browser has geolocation enabled -> store as global obj: "navigator"
    //
    if (navigator.geolocation) {
      // `navigator.geolocation.getCurrentPosition` takes in two args:
      //    1. function call when get location is successful
      //    2. function call when get location is unsuccessful
      //
      navigator.geolocation.getCurrentPosition(
        // The success function:
        (currPosition) => {
          alert('Going to your location now!');

          map.setCenter({
            lat: currPosition.coords.latitude,
            lng: currPosition.coords.longitude
          });
          map.setZoom(12);
        },
        // The unsuccessful function:
        () => {
          alert('Unable to get your location :(');
        }
      );
    } else {
      alert(`Your browser doesn't support geolocation`);
    }
  });
}

/*-------------------------------------------------------------------*/
/*--------------------  Function: Geocode Address  ------------------*/
/*-------------------------------------------------------------------*/

// Use geocode to zoom and add a marker on the map interactively
//
function geocodeAddress(geocoder, map) {
  const address = document.getElementById('address').value;

  geocoder.geocode({ address: address }, (results, status) => {
    if (status === 'OK') {

      // Zoom in on the geocode location on the map
      //
      map.setCenter(results[0].geometry.location);
      map.setZoom(12);

      // Create marker on the map based on the geocode location
      //
      new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          animation: google.maps.Animation.DROP
      });

    } else {
          alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

/*-------------------------------------------------------------------*/
/*------------  Function: Pan to location on click ------------------*/
/*-------------------------------------------------------------------*/

// Place marker and pan to the location when user clicks on map
//
function placeMarkerAndPanTo(latLng, map) {

  map.setZoom(14);

  // new google.maps.Marker({
  //   position: latLng,
  //   map: map,
  // });

  map.panTo(latLng);
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

