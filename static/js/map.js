"use strict";

// Goal: To create a map with markers from stored information on the database
//
// TODO: Set current location or enter neighborhood address
// TODO: Convert address to lat/long for marker OR use address if there is a way
// TODO: Utilize the geocode to enter "location" (golden gate bridge) opposed address
//

/*-------------------------------------------------------------------*/
/*------------ Map section using Google Maps API --------------------*/
/*-------------------------------------------------------------------*/

// const map;

// Initialize google maps
//
function initMap() {
  // Default location to center the initial map view
  //
  const sfCoords = {
      lat: 37.601773,
      lng: -122.202870
  };

  // Create a new instance of Google Maps called "map"
  //
  const map = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: sfCoords,
        zoom: 10,
        mapTypeControlOptions: {
                mapTypeIds: ["roadmap", "satellite", "hybrid", "terrain", "styled_map"]
        }
      }
  );
  
  /*-------------------------------------------------------------------*/

  // Set info window to display the marker's information
  // Based on the jsonify "pets" data from server.py
  //
  const petInfo = new google.maps.InfoWindow({});

  /*-------------------------------------------------------------------*/

  // Get data from jsonify list of pets from server.py
  // Use data from database to set marker on map
  //
  $.get('/get/pets', (pets) => { 
      for (const pet of pets) {
        // Define the content of the infoWindow 
        // Use JS template literals (backticks) - similar to f-string in python
        // Using backticks (`) aka: template literals, to add jQuery into HTML 
        //
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
            //
            petMarker.addListener('click', (evt) => {
              console.log(evt) // for testing

              petInfo.close()
              petInfo.setContent(petInfoContent);
              petInfo.open(map, petMarker);
              // map.setZoom(20);
              // map.setCenter(marker.getPosition());
            });

            // petMarker.addListener("click", () => {
            //   map.setZoom(8);
            //   map.setCenter(marker.getPosition());
            // });

          }           
        }); 
      }
    }).fail(() => {
        alert((`Not able to retrieve pet data`));
    });

  // Create a style map in night mode
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
      ]
    );
    
    //Associate the styled map with the MapTypeId and set it to display.
    map.mapTypes.set('map_style', customStyledMap);
    map.setMapTypeId('map_style');
  });

  /*-------------------------------------------------------------------*/

    // Use geocode form field to add event when location is submitted
    // To find lost pets in the specified location
    //
    const geocoder = new google.maps.Geocoder();

    // // // Call geocodeAddress() when submit button is clicked
    // document.getElementById('geo_btn').addEventListener('click', () => {
    //   geocodeAddress(geocoder, map); 
    // });

    // Call geocodeAddress() when submit button is clicked
    $('#geo_btn').on('click', () => {
      geocodeAddress(geocoder, map); 
    });

}

/*-------------------------------------------------------------------*/
/*---------------------- Functions section --------------------------*/
/*-------------------------------------------------------------------*/

// Function to use geocode to zoom and add a marker on the map interactively
//
function geocodeAddress(geocoder, resultsMap) {
  const address = document.getElementById('address').value;

  geocoder.geocode({ address: address }, (results, status) => {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);

      new google.maps.Marker({
          map: resultsMap,
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

