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

// Initialize google maps 
function initMap() {
  // For now, static coordinates
  // TODO: set coordinates based on current location or submitted address
  //
  const sfCoords = {
      lat: 37.601773,
      lng: -122.202870
  };

  // Create a new Google Maps called "map"
  //
  const map = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: sfCoords,
        zoom: 10
      }
  );


  // Set info window to display the marker's information
  // Based on the jsonify "pets" data from server.py
  //
  const petInfo = new google.maps.InfoWindow({});

  // Get request from server -> route will return a jsonify list of pets in server.py
  //
  $.get('/get/pets', (pets) => { 
      for (const pet of pets) {
        // Define the content of the infoWindow 
        // Use JS template literals (backticks) - similar to f-string in python
        // template literals are surrounded with {}
        const petInfoContent = (` 
          <div class="window-content">
            <div class="pet-thumbnail">
              <img src="${pet.petImage}" width="150" height="120"></img>
            </div>
  
            <ul class="pet-info">
              <li><b>Pet name: </b> ${pet.petName} </li>
              <li><b>Pet breed: </b> ${pet.petBreed} </li>
              <li><b>Pet color: </b> ${pet.petColor} </li>
              <li><b>Last seen: </b> ${pet.lastAddress} </li>
            </ul>
          </div>
        `);

          // To convert address to lat and long for marker
          // Define the lat and long from given address using geocode to convert
          //
          const geocoder = new google.maps.Geocoder();
          const address = `${pet.lastAddress}`

          // console.log(address) // for testing
        
          geocoder.geocode( { 'address': address}, function(results, status) {
        
          if (status == google.maps.GeocoderStatus.OK) {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();
            // alert('latitude is' + latitude + '' + 'longitude is' + longitude);
            // console.log(latitude) // for testing
            // console.log(typeof latitude) // for testing
            // console.log(longitude) // for testing
            // console.log(typeof longitude) // for testing

            // Define marker and set position by lat and long
            // For marker: position is req (latlng) and map (optional) for which map
            //
            const petMarker = new google.maps.Marker({
              position: {
                  lat: latitude,
                  lng: longitude
              },
              title: `Pet ID: ${pet.petId}`,
              map: map
            });
            console.log(petMarker)

            // Define event handling when marker is clicked
            // To show pet information content for each marker
            //
            petMarker.addListener('click', () => {
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

    // Use geocode form field to add event when location is submitted
    //
    const geocoder = new google.maps.Geocoder();

    // Call geocodeAddress() when submit is clicked
    document.getElementById('geo_btn').addEventListener('click', () => {
      geocodeAddress(geocoder, map); 
    });
}

/*-------------------------------------------------------------------*/

// Function to use geocode to add marker on the map interactively
// TODO: Need to save the marker and store in database 
//
// To geocode an address and place marker at the returned lat & long values
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

