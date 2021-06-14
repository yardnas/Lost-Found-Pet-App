"use strict";

// Goal is to create a map with markers
// TODO: Set current location or enter neighborhood address

function initMap() {
    const sfCoords = {
        lat: 37.601773,
        lng: -122.202870
    };

    // Create a new Google Maps map
    const map = new google.maps.Map(
        document.querySelector('#map'),
        {
          center: sfCoords,
          zoom: 10
        }
    );

    // Set info window to display the marker's information
    // const infowindow = new google.maps.InfoWindow({}); //for testing static
    const petInfo = new google.maps.InfoWindow({});


    // Getting info with AJAX
    // Get request from server -> route will return a list of pets in server.py
    $.get('/get/pets', (pets) => { 
        for (const pet of pets) {
          // Define the content of the infoWindow ("/static/img/dog_bulldog.jpg" )
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

            const petMarker = new google.maps.Marker({
                position: {
                    lat: pet.capLat,
                    lng: pet.capLong
                },
                title: `Pet ID: ${pet.petId}`,
                map: map
            });

            petMarker.addListener('click', () => {
                petInfo.close()
                petInfo.setContent(petInfoContent);
                petInfo.open(map, petMarker);
            });
        }
    }).fail(() => {
        alert((`Not able to retrieve pet data`));
    });

    // let marker, count;

    // // Placeholder: Set marker to one location to test
    // const sfmarker = new google.maps.Marker({
    //     position: sfCoords, // set to one coords for now. TODO: make it dynamic
    //     map: map
    // });

    // // Placeholder: Loop through locations to set marker for each location in array
    // for (count = 0; count < locations.length; count++) {
    //     marker = new google.maps.Marker({
    //         position: new google.maps.LatLng(locations[count][1],
    //                                             locations[count][2]),
    //                                             map: map,
    //                                             title: locations[count][0]
    //     });

    // google.maps.event.addListener(marker, 'click', (function (marker, count) {
    //     return function () {
    //         infowindow.setContent(locations[count][0]);
    //         infowindow.open(map, marker);
    //     }
    // }) (marker, count));
    // }

    // User to enter location where pet was last seen
    // Geocode the location to get its coordinates and add a marker on the map
    // $('#geocode-pet-address').on('click', () => { //on click listening
    //     const petLastAddress = prompt('Enter a location'); 

    //     const geocoder = new google.maps.Geocoder(); // creating a new geocoder object
    //     geocoder.geocode({ address: petLastAddress }, (results, status) => { 
    //     if (status === 'OK') {
    //         // Get the coordinates of the user's location
    //         const petLocation = results[0].geometry.location; //taking result[0] - getting back an array of results and grabbing the coordinate

    //         // Create a marker
    //         const petLocationMarker = new google.maps.Marker({
    //         position: petLocation, // pet location marker, position is the lat/long coordinates. 
    //                                 //for marker need position and map
    //         map: map
    //         });

    //         // Zoom in on the geolocated location
    //         map.setCenter(userLocation); // zooming into the location, search and then zoom. setting cetner of map to zoom locaftino
    //         map.setZoom(10);
    //     } else {
    //         alert(`Geocode was unsuccessful for the following reason: ${status}`); // otherwise get the alert
    //     }
    //     });
    // });

    const geocoder = new google.maps.Geocoder();
    document.getElementById("submit").addEventListener("click", () => {
    geocodeAddress(geocoder, map);
  });
}

function geocodeAddress(geocoder, resultsMap) {
    const address = document.getElementById("address").value;
    geocoder.geocode({ address: address }, (results, status) => {
      if (status === "OK") {
        resultsMap.setCenter(results[0].geometry.location);

        new google.maps.Marker({
            map: resultsMap,
            position: results[0].geometry.location,
        });
      } else {
            alert("Geocode was not successful for the following reason: " + status);
      }
    });
  }

