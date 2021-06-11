"use strict";

// Goal is to create a map with markers
//  from locations entered in a form
// Need to determine data store (.csv to jsonify, json data)
// Need to determine data columns/attribute for marker
// Need to add a listener event when a marker is clicked 
//  to set content of the marker info to the opened info window 

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

    // Placeholder: Test code for multiple markers with placeholder for now
    // Placeholder dummy locations data array to test
    const locations = [
        ['Starbucks<br>\
        54 E 4th Ave, San Mateo, CA 94401<br>\
        <a href="https://goo.gl/maps/9USxLKVRiUKoKHpt8">Get Directions</a>', 37.57687869717359, -122.32175379773953],
        ['Redwood City', 37.48456569453062, -122.22140909355261],
        ['Burlingame', 37.578224053823284, -122.34378979745154],
        ['Oakland', 37.80429713799038, -122.26796619316501],
        ['Palo Alto', 37.44365208350075, -122.1478400745741],
        ['San Jose', 37.34026763807634, -121.92994914279588]
    ];

    // Placeholder: New info window to display the marker's information
    const infowindow = new google.maps.InfoWindow({});

    let marker, count;

    // Placeholder: Set marker to one location to test
    const sfmarker = new google.maps.Marker({
        position: sfCoords, // set to one coords for now. TODO: make it dynamic
        map: map
    });

    // Placeholder: Loop through locations to set marker for each location in array
    for (count = 0; count < locations.length; count++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[count][1],
                                                locations[count][2]),
                                                map: map,
                                                title: locations[count][0]
        });

    google.maps.event.addListener(marker, 'click', (function (marker, count) {
        return function () {
            infowindow.setContent(locations[count][0]);
            infowindow.open(map, marker);
        }
    }) (marker, count));
    }
}