"use strict";

// This function is called onload.  It's the 'parent process' if you like that
// kicks off all the work...
function onLoad() {
    displayStations()
}

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
        return null  // Result undefined
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
    let stations = await getStationsJson();
    // 'stations' is now a nice javascript object.  We could "for station in stations"
    // over it, or pick it apart by hand, or whatever!!

    // let html = '';
    // stations.forEach(user => {
    //     let htmlSegment = `<div class="user">
    //                         <img src="${stations.bla-bla}" >
    //                         <h2>${stations.bla-bla} ${stations.bla-bla}</h2>
    //                         <div class="bla-bla">${stations.bla-bla}</div>
    //                     </div>`;


    document.getElementById('tempTomShowJson').innerHTML=JSON.stringify(stations);
}

//##############################################################################
//##############################################################################
//##############################################################################

// SAMPLE CODE FROM COMP30830 LECTURE NOTES / PDF's

// // draw markers
// _.forEach(stations, function(station) {
//     // console.log(station.name, station.number);
//     var marker = new google.maps.Marker({
//         position : {
//             lat : station.position_lat,
//             lng : station.position_lng
//         },
//         map : map,
//         title : station.name,
//         station_number : station.number
//     });
//     contentString = '<div id="content"><h1>' + station.name + '</h1></div>'
//         + '<div id="station_availability"></div>';
//     google.maps.event.addListener(marker, 'click', function() { drawInfoWindowChart(this); } );
// })

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