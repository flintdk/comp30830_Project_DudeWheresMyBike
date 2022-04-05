"use strict";

var varGlobStations;
var varGlobStationSelected;

// This function is called onload.  It's the 'parent process' if you like that
// kicks off all the work...
async function onLoad() {
    varGlobStations = await getStationsJson();

}

// Function to initialize and add the map
async function initMap() {
    // We load the stations on page load.  Yes - that means that if a new
    // station is added while the user is on a page that it won't be displayed.
    // That event is so unlikely, we consider the requirement for a page refresh
    // to get the new station to display to be acceptable.
    let stations = await getStationsJson();

    // Location of Dublin
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // Map, centered at Dublin
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: dublin,
    });

    // Markers
    // 'stations' is a nice javascript object.  We could "for station in stations"
    // over it, or pick it apart by hand, or whatever!!
    // Intial marker, positioned at Dublin
    // const marker = new google.maps.Marker({
    //     position: dublin,
    //     map: map,
    //     icon: 'bikeIcon.svg'
    // });
    for (let key in stations) {
        let station = stations[key];
        //console.log(station.stationName, station.number);
        var marker = new google.maps.Marker({
            position: {
                lat: station.latitude,
                lng: station.longitude
            },
            map: map,
            icon: {
                url: "/img/bikeIcon.svg",
                scaledSize: new google.maps.Size(42, 42)
            },
            title: station.stationName,
            station_number: station.number,
            
        });
        // marker.addListener("click", () => {
        //     map.setZoom(8);
        //     map.setCenter(marker.getPosition());
        //   });

        let contentString = '<div id="content"><h1>' + station.stationName + '</h1></div>' +
            '<div id="station_availability">Availability:</div>';
        // let contentString = '<div id="content"><h1>' + station.stationName + '</h1></div>' +
        //     '<div id="station_details"><table>' +
        //     '<tr><td>Station name: :</td><td>' + station.stationName + '</td></tr>' +
        //     '<tr><td>Station address: :</td><td>' + station.address + '</td></tr>' +
        //     '<tr><td>Station latitude: :</td><td>' + station.latitude + '</td></tr>' +
        //     '<tr><td>Station longitude: :</td><td>' + station.longitude + '</td></tr>' +
        //     '<tr><td>Station banking: :</td><td>' + station.banking + '</td></tr>' +
        //     '<tr><td>Station bonus: :</td><td>' + station.bonus + '</td></tr>' +
        //     '</div>';
        
        let infoWindow = new google.maps.InfoWindow({ content: contentString });

        // Listener
        marker.addListener('click', function() { infoWindow.open(map, marker); })
        // Following from Lecture notes - not sure what the difference is yet!
        // But it adds a chart... so leaving for reference.
        //google.maps.event.addListener(marker, 'click', function() { drawInfoWindowChart(this); } );
    }

}

// + "SET stationName = \"" + station['name'] + "\", " \
// + "address = \"" + station['address'] + "\", " \
// + "latitude = " + str(station['lat']) + ", " \
// + "longitude = " + str(station['lng']) + ", " \
// + "banking = " + str(station['banking']) + ", " \
// + "bonus = " + str(station['bonus']) + " " \
// + "WHERE number = " + str(station['number']) + " " \
// + "and contractName = \"dublin\";")

// What follows are a pair of functions to:
//   -> first get
//   -> and then display
// our stations data in json format.  We might never use these once the dudeWMB
// site is final. But its a helpful exercise to make sure we can access JSON data
// sourced from an endpoint in the dudeWMB Flask app, using JavaScript fetch()
async function getStationsJson() {
    // There is a good example on using JavaScript fetch here:
    //      https://www.javascripttutorial.net/javascript-fetch-api/
    // I chose not to reproduce that content here (because it's much easier to
    // read on the web with pictures etc.).  If you want to explore JavaScript
    // fetch, please start there.

    // Key concept: A Promise is an object representing the eventual completion or failure of an asynchronous operation.

    let url = 'stations';
    try {
        let stations = await fetch(url);
        // console.log(stations.status); // 200
        // console.log(stations.statusText); // OK

        // In the following line, the json() method of the Response interface takes
        // a Response stream and reads it to completion. It returns a promise which
        // resolves with the result of parsing the body text as JSON.
        // *** Note that despite the method being named json(), the result is not
        //     JSON but is instead the result of taking JSON as input and parsing
        //     it to produce a JavaScript object!
        if (stations.status == 200) {
            let stationsJson = await stations.json();
            return stationsJson;
        }
        return null // Result undefined
    } catch (error) {
        console.log(error);
    }

    // There's a shorter/neater way to do the above. We're learning. I left it long for now.
    // fetch(url)
    // .then(stations => {
    //     //console.log(stations.json())
    //     return stations.json()
    // })
    // .catch(error => {
    //     // handle the error
    // });
}

async function displayStations() {

    // 'stations' is now a nice javascript object.  We could "for station in stations"
    // over it, or pick it apart by hand, or whatever!!

    // let html = '';
    // stations.forEach(user => {
    //     let htmlSegment = `<div class="user">
    //                         <img src="${stations.bla-bla}" >
    //                         <h2>${stations.bla-bla} ${stations.bla-bla}</h2>
    //                         <div class="bla-bla">${stations.bla-bla}</div>
    //                     </div>`;


    document.getElementById('tempTomShowJson').innerHTML=JSON.stringify(varGlobStations);
}

// Function to dynamically create the dropdown content for station selection
function createStationDropdownContent() {
    // for example: <a href="#" onclick="onUpdateStationInfo(stationId)">SMITHFIELD NORTH</a>
    // where stationId is the index in the station-object

//    console.log(varGlobStations)
    var output = "";
    for (let i = 0; i < varGlobStations.length; i++) {
        output += '<a href="#" ';
        output += 'onclick="onStationSelected(';
        output += "'" + i + "',";  
        output += ')">';
        output += varGlobStations[i].stationName; 
        output += "</a>";
    }
    document.getElementById('dropdownContentStation').innerHTML = output;

}

function onStationSelected(stationId) {
    varGlobStationSelected = varGlobStations[stationId];

    console.log(varGlobStations[stationId].stationName)
    document.getElementById('selectedStation').innerHTML = varGlobStations[stationId].stationName;

}

//##############################################################################
//##############################################################################
//##############################################################################

// SAMPLE CODE FROM COMP30830 LECTURE NOTES / PDF's

// jQuery Heatmap example from Lecture Slides:
// TODO: Rework this using JavaScript 'fetch()'??
// function drawHeatmap(me) {
//     //console.log('toggle heatmap');
//     console.log('clicked checkbox-1', me, me.prop('checked'));
//     checked = me.prop('checked');
//     if(checked) {
//         if(heatmap == null) {
//             var jqxhr = $.getJSON($SCRIPT_ROOT + "/heatmap",
//             function(data) {
//                 console.log('data', data);
//                 var heatmapData = [];
//                 _.forEach(data.data, function(row) {
//                         heatmapData.push(
//                             {
//                             location: new google.maps.LatLng(row.position_lat, row.position_lng),
//                             weight: row.available_bikes});
//                             }
//                         );
//                     heatmap = new google.maps.visualization.HeatmapLayer({
//                         data: heatmapData,
//                         map: map
//                         });
//                     console.log(heatmap);
//                     heatmap.setMap(map);
//                     heatmap.set('radius', 40);
//                     //heatmap.setMap(heatmap.getMap() ? null : map);
//                 }).fail(function() {
//                     console.log('failed');
//                     });
//         }
//         else {
//             heatmap.setMap(map);
//         }
//     }
//     else {
//         heatmap.setMap(null);
//     }
// }

// jQuery Occupancy example from Lecture Slides:
// TODO: Rework this using JavaScript 'fetch()'??
//  var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number,
//         function(data) {
//         data = JSON.parse(data.data);
//         console.log('data', data);
//         var node = document.createElement('div'),
//         infowindow = new google.maps.InfoWindow(),
//         chart = new google.visualization.ColumnChart(node);
//         var chart_data = new google.visualization.DataTable();
//         chart_data.addColumn('datetime', 'Time of Day');
//         chart_data.addColumn('number', '#');
//         _.forEach(data, function(row){
//         chart_data.addRow([new Date(row[0]), row[1]]);
//         })
//         chart.draw(chart_data, options);
//         infowindow.setContent(node);
//         infowindow.open(marker.getMap(), marker);
//         }).fail(function() {
//         console.log( "error" );
//         })