// This file includes JavaScript functionality that's related to the embedded Google map

var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'),{
       center: {lat: -34.397, lng: 150.644},
       zoom: 8
    })
}
