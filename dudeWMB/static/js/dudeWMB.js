"use strict";

// Define modes as kind of enumerations in javascript
const MODE_AVAILABLE_BIKES = "ModeAvailableBikes";
const MODE_AVAILABLE_SPACES = "ModeAvailabeSpaces";

// varGlobStations is a array that contains the json objects for each station
var varGlobStations;
// varGlobStationSelected contains station data for the selected station
var varGlobStationSelected;
// varGlobMap allows to access the created map globally
var varGlobMap;
// varGlobActiveMode represents the active user mode (avalailable bikes, available spaces)
var varGlobActiveMode = MODE_AVAILABLE_BIKES;


//-----------------------------------------------------------------------------
// Function onLoad is invoked when the website (DOM) is loaded the first time
//-----------------------------------------------------------------------------
// This function is called onload.  It's the 'parent process' if you like that
// kicks off all the work...
async function onLoad() {
    // get station data in json format
    varGlobStations = await getStationsJson();

    // Add event listener to mode buttons 
    document.getElementById("button_available_bikes").addEventListener("click", function() {
        onSetMode(MODE_AVAILABLE_BIKES);
      });
    document.getElementById("button_available_spaces").addEventListener("click", function() {
        onSetMode(MODE_AVAILABLE_SPACES);
    });

    // set default mode
    onSetMode(MODE_AVAILABLE_BIKES);
}

//-----------------------------------------------------------------------------
// Mode control - 'available bikes' OR 'available spaces' 
//-----------------------------------------------------------------------------
function onSetMode(mode) {
    if (mode === MODE_AVAILABLE_BIKES) {
        varGlobActiveMode = MODE_AVAILABLE_BIKES;
        document.getElementById("button_available_bikes").style.backgroundColor = "green"
        document.getElementById("button_available_spaces").style.backgroundColor = "lightgreen"
    } else if (mode === MODE_AVAILABLE_SPACES) {
        varGlobActiveMode = MODE_AVAILABLE_SPACES;
        document.getElementById("button_available_bikes").style.backgroundColor = "lightgreen"
        document.getElementById("button_available_spaces").style.backgroundColor = "green"
    }
    // Init map and coloured icons when user mode is changing
    initMap();
}

//-----------------------------------------------------------------------------
// Bike icon selection according to occupancy and user mode 
//-----------------------------------------------------------------------------
function getBikeIconUrl(mode, stationState) {

    // Threshold values defined in percentage to select coloured bike icons accordingly
    const THRESHOLD_GREEN = 70.0;
    const THRESHOLD_ORANGE = 40.0;
    const THRESHOLD_RED = 10.0;

    // Relative paths to bike icons
    const PATH_BIKE_ICON = "/img/bikeIcon.svg";
    const PATH_BIKE_ICON_GREEN = "/img/bikeIconGreen.png";
    const PATH_BIKE_ICON_ORANGE = "/img/bikeIconOrange.png";
    const PATH_BIKE_ICON_RED = "/img/bikeIconRed.png";
 
    let iconPathSelected = PATH_BIKE_ICON;

    // If station is closed then show default icon
    if (!(stationState.status == 'OPEN')) {
        iconPathSelected = PATH_BIKE_ICON;
    } 
    // Select bike icons to user mode and occupancy accordingly
    // If user mode is 'available bikes' then... 
    else if (mode === MODE_AVAILABLE_BIKES) {
        if (getPercentage(stationState.available_bikes, stationState.bike_stands) >= THRESHOLD_GREEN) {
            iconPathSelected = PATH_BIKE_ICON_GREEN;
        } 
        else if (getPercentage(stationState.available_bikes, stationState.bike_stands) >= THRESHOLD_ORANGE) {
            iconPathSelected = PATH_BIKE_ICON_ORANGE;
        } 
        else if (getPercentage(stationState.available_bikes, stationState.bike_stands) <= THRESHOLD_RED) {
            iconPathSelected = PATH_BIKE_ICON_RED;
        } 
    } 
    // If user mode is 'available bikes' then... 
    else if (mode === MODE_AVAILABLE_SPACES) {
        if (getPercentage(stationState.available_bike_stands, stationState.bike_stands) >= THRESHOLD_GREEN) {
            iconPathSelected = PATH_BIKE_ICON_GREEN;
        } 
        else if (getPercentage(stationState.available_bike_stands, stationState.bike_stands) >= THRESHOLD_ORANGE) {
            iconPathSelected = PATH_BIKE_ICON_ORANGE;
        } 
        else if (getPercentage(stationState.available_bike_stands, stationState.bike_stands) <= THRESHOLD_RED) {
            iconPathSelected = PATH_BIKE_ICON_RED;
        } 
    }
    // console.log("available bikes: " + stationState.available_bikes);
    // console.log("available bike stands: " + stationState.available_bike_stands);
    // console.log("stands bikes: " + stationState.bike_stands);
    // console.log("stands status: " + stationState.status);
    // console.log(iconPathSelected);
    return iconPathSelected;

}

function getPercentage(value, max) {
        
        let percentage = 0.0;
        if (max != 0) {
            percentage = (value / max) * 100;
        } else {
            console.log("Error: Zero Division in getPercentage()");
        }

    return percentage;
}

function getPercentage(value, max) {
        
        let percentage = 0.0;
        if (max != 0) {
            percentage = (value / max) * 100;
        } else {
            console.log("Error: Zero Division in getPercentage()");
        }

    return percentage;
}
// status = db.Column(db.String(45), nullable=True)
// bike_stands = db.Column(db.Integer, nullable=True)
// available_bike_stands = db.Column(db.Integer, nullable=True)
// available_bikes = db.Column(db.Integer, nullable=True)

//-----------------------------------------------------------------------------
// Function to initialize and add the map
//-----------------------------------------------------------------------------
async function initMap() {
    // We load the stations on page load as well as here in initMap - whatever event occurs first 
    varGlobStations = await getStationsJson();

    // Location of Dublin
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // Create new map, centered at Dublin
    varGlobMap = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: dublin,
    });

    createMarkers(varGlobMap, varGlobStations);
}

//-----------------------------------------------------------------------------
// Create markers that are displayed on the map
//-----------------------------------------------------------------------------
// Note: The coloured bike icon (black, green, orange, red) may change when the user mode is changed,
// depending on the availability of available bikes, spaces
// That's why this function is also called if the user mode changes
function createMarkers(map, stationData) {

    for (let key in varGlobStations) {
        let station = varGlobStations[key];

        //console.log(station.stationName, station.number);
        var marker = new google.maps.Marker({
            position: {
                lat: station.latitude,
                lng: station.longitude
            },
            map: map,
            icon: {
                url: getBikeIconUrl(varGlobActiveMode, station),
                scaledSize: new google.maps.Size(42, 42)
            },
            title: station.stationName,
            station_number: station.number,
            station_index: key, // add key as index so that marker correlates with the array index in station data
            
        });
        
        // Create table containing information about the station
        let contentString = '<div id="content"><span id="markerStationName">' + station.stationName + '</span></div>' +
            '<div id="station_details"><table>' +
            '<tr><td>Station name:</td><td>' + station.stationName + '</td></tr>' +
            '<tr><td>Address:</td><td>' + station.address + '</td></tr>' +
            '<tr><td>Latitude:</td><td>' + station.latitude + '</td></tr>' +
            '<tr><td>Longitude:</td><td>' + station.longitude + '</td></tr>' +
            '<tr><td>Banking:</td><td>' + station.banking + '</td></tr>' +
            '<tr><td>Total bike stands:</td><td>' + station.bike_stands + '</td></tr>' +
            '<tr><td>Available bike stands:</td><td>' + station.occupancy.available_bike_stands + '</td></tr>' +
            '<tr><td>Available bikes:</td><td>' + station.occupancy.available_bikes + '</td></tr>' +
            '</div>';
        
        let infoWindow = new google.maps.InfoWindow({ content: contentString });
        // Add listener so that we can add actions that will be performed when clicking on a marker
        marker.addListener("click", () => {
            map.setZoom(16);
            map.setCenter(marker.getPosition());
            infoWindow.open(map, marker);
            displayDetails(marker.station_index);
          });
    }
}

//-----------------------------------------------------------------------------
// Display station details such as weather info and occupancy 
//-----------------------------------------------------------------------------
async function displayDetails (stationIndex) {
    
}

//-----------------------------------------------------------------------------
// Display station weather detials such as weather icon, temperature, etc. 
//-----------------------------------------------------------------------------
function displayWeatherIcon (stationIndex) {
    // TODO @ Will
    ;
}

//-----------------------------------------------------------------------------
// Display station occupancy chart 
//-----------------------------------------------------------------------------
function displayOccupancyChart (stationIndex) {
    ;
}

//-----------------------------------------------------------------------------
// Get station data
//-----------------------------------------------------------------------------
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
}

// async function displayStations() {

//     // 'stations' is now a nice javascript object.  We could "for station in stations"
//     // over it, or pick it apart by hand, or whatever!!

//     // let html = '';
//     // stations.forEach(user => {
//     //     let htmlSegment = `<div class="user">
//     //                         <img src="${stations.bla-bla}" >
//     //                         <h2>${stations.bla-bla} ${stations.bla-bla}</h2>
//     //                         <div class="bla-bla">${stations.bla-bla}</div>
//     //                     </div>`;


//     document.getElementById('tempTomShowJson').innerHTML=JSON.stringify(varGlobStations);
// }

function drawOccupancyHistogram(stationId) {

    const occupancyFetchPromise = fetch('/occupancy/' + stationId);
    // Define our event handler for what to do when the promise is fulfilled...
    occupancyFetchPromise.then(
        response => {
            //console.log(`Received response: ${response.status}`);
            var occupancyData = JSON.parse(response.text());
            console.log(occupancyData);
            var dataTableData = google.visualization.arrayToDataTable(occupancyData);
        }
    );

    fetch("URL")
   .then(response => response.text())
   .then((response) => {
       console.log(response)
   })
   .catch(err => console.log(err))




    // var data = new google.visualization.DataTable(dataTableData);
    // var options = {'title':'My Average Day', 'width':550, 'height':400};
    // var chart =
    //     new google.visualization.PieChart(document.getElementById('occupancy_histogram'));
    // chart.draw(data, options);
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

// SLIDER - IN PROGRESS
// Credit http://jsfiddle.net/meghap/9pz5grru/5/

// function toTimestamp(strDate){
//     // The Date.parse() method parses a string representation of a date, and
//     // returns the number of milliseconds since January 1, 1970, 00:00:00 UTC
//     var datum = Date.parse(strDate);
//     // We divide by 1000, just to use seconds.
//     return datum/1000;
//  }

//  var currentDateTime = new Date();
//  currentDateTime.setMinutes(0, 0, 0);  // Resets also seconds and milliseconds

//  var dt_to = "01/13/2016 16:37:43";
 
//  var sel_dt_from = "01/13/2016 00:34:44";
//  var sel_dt_to = "01/14/2016 16:37:43";
 
//  $('.slider-time').html(dt_from);
//  $('.slider-time2').html(dt_to);
//  var min_val = toTimestamp(sel_dt_from);
//  var max_val = toTimestamp(sel_dt_to);
 
//  function zeroPad(num, places) {
//    var zero = places - num.toString().length + 1;
//    return Array(+(zero > 0 && zero)).join("0") + num;
//  }
//  function formatDT(__dt) {
//      var year = __dt.getFullYear();
//      var month = zeroPad(__dt.getMonth()+1, 2);
//      var date = zeroPad(__dt.getDate(), 2);
//      var hours = zeroPad(__dt.getHours(), 2);
//      var minutes = zeroPad(__dt.getMinutes(), 2);
//      var seconds = zeroPad(__dt.getSeconds(), 2);
//      return year + '-' + month + '-' + date + ' ' + hours + ':' + minutes + ':' + seconds;
//  };
 
 
//  $("#slider-range").slider({
//      range: true,
//      min: min_val,
//      max: max_val,
//      step: 10,
//      values: [min_val, max_val],
//      slide: function (e, ui) {
//          var dt_cur_from = new Date(ui.values[0]*1000); //.format("yyyy-mm-dd hh:ii:ss");
//          $('.slider-time').html(formatDT(dt_cur_from));
 
//          var dt_cur_to = new Date(ui.values[1]*1000); //.format("yyyy-mm-dd hh:ii:ss");                
//          $('.slider-time2').html(formatDT(dt_cur_to));
//      }
//  });

//##############################################################################
//##############################################################################
//##############################################################################


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