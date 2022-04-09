"use strict";

google.load("visualization", 'current', {packages:["corechart"]});

// Define modes as kind of enumerations in javascript
const MODE_AVAILABLE_BIKES = "ModeAvailableBikes";
const MODE_AVAILABLE_SPACES = "ModeAvailabeSpaces";

// varGlobStations is a array that contains the json objects for each station
var varGlobStations;
// varGlobStationSelected contains station data for the selected station
var varGlobStationSelectedIndex;
// varGlobMap allows to access the created map globally
var varGlobMap;
// varGlobActiveMode represents the active user mode (avalailable bikes, available spaces)
var varGlobActiveMode = MODE_AVAILABLE_BIKES;
// varGlobPredictionInHours indicates the data prediction we want to get in x hours time, where hours == 0 stands for current time 
var varGlobPredictionInHours = 0;

//-----------------------------------------------------------------------------
// Function onLoad is invoked when the website (DOM) is loaded the first time
//-----------------------------------------------------------------------------
// This function is called onload.  It's the 'parent process' if you like that
// kicks off all the work...
async function onLoad() {

    let url = 'stations'
    varGlobStations = await getStationsJson(url);

    // Add event listener to mode buttons 
    document.getElementById("button_available_bikes").addEventListener("click", function() {
        onSetMode(MODE_AVAILABLE_BIKES);
      });
    document.getElementById("button_available_spaces").addEventListener("click", function() {
        onSetMode(MODE_AVAILABLE_SPACES);
    });

    // set default mode
    onSetMode(MODE_AVAILABLE_BIKES);

    displayOccupancyChart(16);
}

//-----------------------------------------------------------------------------
// Function to initialize and add the map
//-----------------------------------------------------------------------------
async function initMap() {
    // We load the stations on page load as well as here in initMap - whatever event occurs first 
    let url = 'stations'
    varGlobStations = await getStationsJson(url);

    // Location of Dublin
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // Create new map, centered at Dublin
    varGlobMap = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: dublin,
    });

    createMarkers(varGlobMap);
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
    // Also update station details
//    displayStationDetails(varGlobStationSelectedIndex);
}

//-----------------------------------------------------------------------------
// Bike icon selection according to occupancy and user mode 
//-----------------------------------------------------------------------------
function getBikeIconUrl(mode, station) {

    // Threshold values defined in percentage to select coloured bike icons accordingly
    const THRESHOLD_GREEN = 70.0;
    const THRESHOLD_ORANGE = 40.0;
    const THRESHOLD_RED = 10.0;

    // Relative paths to bike icons
    const PATH_BIKE_ICON = "img/bikeIcon.svg";
    const PATH_BIKE_ICON_GREEN = "img/bikeIconGreen.png";
    const PATH_BIKE_ICON_ORANGE = "img/bikeIconOrange.png";
    const PATH_BIKE_ICON_RED = "img/bikeIconRed.png";
 
    let iconPathSelected = PATH_BIKE_ICON;
    //console.log("In getbikeIcon : " + JSON.stringify(station));
    // If station is closed then show default icon
    if (!(station.occupancy.status == 'OPEN')) {
        iconPathSelected = PATH_BIKE_ICON;
    } 
    // Select bike icons to user mode and occupancy accordingly
    // If user mode is 'available bikes' then... 
    else if (mode === MODE_AVAILABLE_BIKES) {
        if (getPercentage(station.occupancy.available_bikes, station.bike_stands) >= THRESHOLD_GREEN) {
            iconPathSelected = PATH_BIKE_ICON_GREEN;
        } 
        else if (getPercentage(station.occupancy.available_bikes, station.bike_stands) >= THRESHOLD_ORANGE) {
            iconPathSelected = PATH_BIKE_ICON_ORANGE;
        } 
        else if (getPercentage(station.occupancy.available_bikes, station.bike_stands) <= THRESHOLD_RED) {
            iconPathSelected = PATH_BIKE_ICON_RED;
        } 
    } 
    // If user mode is 'available bikes' then... 
    else if (mode === MODE_AVAILABLE_SPACES) {
        if (getPercentage(station.occupancy.available_bike_stands, station.bike_stands) >= THRESHOLD_GREEN) {
            iconPathSelected = PATH_BIKE_ICON_GREEN;
        } 
        else if (getPercentage(station.occupancy.available_bike_stands, station.bike_stands) >= THRESHOLD_ORANGE) {
            iconPathSelected = PATH_BIKE_ICON_ORANGE;
        } 
        else if (getPercentage(station.occupancy.available_bike_stands, station.bike_stands) <= THRESHOLD_RED) {
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

//-----------------------------------------------------------------------------
// Create markers that are displayed on the map
//-----------------------------------------------------------------------------
// Note: The coloured bike icon (black, green, orange, red) may change when the user mode is changed,
// depending on the availability of available bikes, spaces
// That's why this function is also called if the user mode changes
function createMarkers(map) {

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
            displayStationDetails(marker.station_index);
          });
    }
}

//-----------------------------------------------------------------------------
// Display station details such as weather info and occupancy 
//-----------------------------------------------------------------------------
async function displayStationDetails(stationIndex) {

    // Store the index of the selected station within the station array
    varGlobStationSelectedIndex = stationIndex;

    // Create URL to fetch data for stations at a specific time in the future
    let url = 'stations?hours_in_future=';
    url += varGlobPredictionInHours.toString();
    // After the following code line, our function will wait for the getStationJson to return a result.
    // This website describes how promises using async/await works: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises 
    // Quoting from the website:
    // "Inside an async function you can use the await keyword before a call to a function that returns a promise. 
    // This makes the code wait at that point until the promise is settled, 
    // at which point the fulfilled value of the promise is treated as a return value, or the rejected value is thrown.
    // This enables you to write code that uses asynchronous functions but looks like synchronous code.
    let StationDataPredicted = await getStationsJson(url);

    // Update station name headline
    //console.log("stationIndex: " + stationIndex.toString());
    //console.log(StationDataPredicted);
    //console.log(url);
    document.getElementById('selectedStation').innerHTML = StationDataPredicted[stationIndex].stationName;

    displayOccupancyChart(stationIndex);
    displayWeatherIcon(stationIndex);
    
}

//-----------------------------------------------------------------------------
// Display station weather detials such as weather icon, temperature, etc. 
//-----------------------------------------------------------------------------
function displayWeatherIcon(stationIndex) {
    /* Function to display weather icon for current/future weather description
    as slider is moved
    */
    // Relative paths to weather category icons
    // Default Image for any errors etc.
    const PATH_TEMP_ICON = "img/weather_forecast_icon.png";
    // Icon paths for different weather categories
    const PATH_ICON_BROKEN_CLOUDS = "img/broken_clouds.svg";
    const PATH_ICON_CLEAR_SKY = "img/clear_sky.svg";
    const PATH_ICON_FEW_CLOUDS = "img/few_clouds.svg";
    const PATH_ICON_FOG = "img/fog.svg";
    const PATH_ICON_HAZE = "img/haze.svg";
    const PATH_ICON_HVY_INT_RAIN = "img/heavy_intensity_rain.svg";
    const PATH_ICON_LIGHT_INT_DRIZ = "img/light_intensity_drizzle.svg";
    const PATH_ICON_LIGHT_INT_DRIZ_RAIN = "img/light_intensity_drizzle_rain.svg";
    const PATH_ICON_LIGHT_INT_SHOW_RAIN = "img/light_intensity_shower_rain.svg";
    const PATH_ICON_LIGHT_RAIN = "img/light_rain.svg";
    const PATH_ICON_MIST = "img/mist.svg";
    const PATH_ICON_MODERATE_RAIN = "img/moderate_rain.svg";
    const PATH_ICON_OVERCAST_CLOUDS = "img/overcast_clouds.svg";
    const PATH_ICON_SCATTERED_CLOUDS = "img/scattered_clouds.svg";
 
    let weatherIconPath = PATH_TEMP_ICON;

    let station = varGlobStations[stationIndex];

    // Checking current and future weather description to update path to weather icon
    if (station.weather.description == 'broken clouds') {
        weatherIconPath = PATH_ICON_BROKEN_CLOUDS;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'clear sky') {
        weatherIconPath = PATH_ICON_CLEAR_SKY;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'few clouds') {
        weatherIconPath = PATH_ICON_FEW_CLOUDS;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'fog') {
        weatherIconPath = PATH_ICON_FOG;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'haze') {
        weatherIconPath = PATH_ICON_HAZE;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'heavy intensity rain') {
        weatherIconPath = PATH_ICON_HVY_INT_RAIN;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'light intensity drizzle') {
        weatherIconPath = PATH_ICON_LIGHT_INT_DRIZ;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'light intensity drizzle rain') {
        weatherIconPath = PATH_ICON_LIGHT_INT_DRIZ_RAIN;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'light intensity shower rain') {
        weatherIconPath = PATH_ICON_LIGHT_INT_SHOW_RAIN;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'light rain') {
        weatherIconPath = PATH_ICON_LIGHT_RAIN;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'mist') {
        weatherIconPath = PATH_ICON_MIST;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'moderate rain') {
        weatherIconPath = PATH_ICON_MODERATE_RAIN;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'overcast clouds') {
        weatherIconPath = PATH_ICON_OVERCAST_CLOUDS;
        document.getElementById("img-weather").src=weatherIconPath;
    } else if(station.weather.description == 'scattered clouds') {
        weatherIconPath = PATH_ICON_SCATTERED_CLOUDS;
        document.getElementById("img-weather").src=weatherIconPath;
    } else {
        weatherIconPath = PATH_TEMP_ICON;
        document.getElementById("img-weather").src=weatherIconPath;
    }
    document.getElementById("sliderTemp").innerHTML=station.weather.temp;
    console.log(station.weather.description);

    return;
}

// document.getElementById("img-weather").src

//-----------------------------------------------------------------------------
// Display station occupancy chart 
//-----------------------------------------------------------------------------
async function displayOccupancyChart(stationIndex) {

    let station = varGlobStations[stationIndex];

    let occupancyFetchPromise = fetch('/occupancy/' + station.id);
    // Define our event handler for what to do when the promise is fulfilled...
    occupancyFetchPromise.then(
        response => {
            //console.log(`Received response: ${response.status}`);

            let responseTextPromise = response.text();
            responseTextPromise.then (
                responseText => {
                    let occupancyData = JSON.parse(responseText)
                    //console.log("occupancyData: " + JSON.stringify(occupancyData));

                    // Google Visualisation API Reference:
                    //   https://developers.google.com/chart/interactive/docs/reference#dataparam

                    // Google Chart Tools charts require data to be wrapped in a
                    // JavaScript class called google. visualization. DataTable

                    // Can we load the json data directly into a Data Table??
                    //let dataTableData = google.visualization.arrayToDataTable(occupancyData);
                    var dataTable = new google.visualization.DataTable(occupancyData);

                    google.charts.load("current", {packages:["corechart"]});

                    // var options = {'title':'My Average Day'};
                    var options = {
                        title: 'Occupancy for ' + station.stationName + ', Last Seven Days',
                        legend: { position: 'none' },
                        width: 400,
                        height:300,
                        hAxis: {
                            format: 'yy/MM/dd',
                            gridlines: {count: 7}
                        },
                        vAxis: {
                            gridlines: {color: 'none'},
                            minValue: 0
                        }
                    };
                
                    //var chart = new google.visualization.Histogram(document.getElementById('occupancy_histogram'));
                    //var chart = new google.visualization.PieChart(document.getElementById('occupancy_histogram'));
                    //var chart = new google.visualization.BarChart(document.getElementById('occupancy_histogram'));
                    var chart = new google.visualization.ColumnChart(document.getElementById('occupancy_histogram'));
                    chart.draw(dataTable, options);
                    
                }
            )
        }
    );

//     fetch("URL")
//    .then(response => response.text())
//    .then((response) => {
//        console.log(response)
//    })
//    .catch(err => console.log(err))

    // var data = google.visualization.arrayToDataTable([
    // ['Dinosaur', 'Length'],
    // ['Acrocanthosaurus (top-spined lizard)', 12.2],
    // ['Albertosaurus (Alberta lizard)', 9.1],
    // ['Allosaurus (other lizard)', 12.2],
    // ['Apatosaurus (deceptive lizard)', 22.9],
    // ['Archaeopteryx (ancient wing)', 0.9],
    // ['Argentinosaurus (Argentina lizard)', 36.6],
    // ['Baryonyx (heavy claws)', 9.1],
    // ['Brachiosaurus (arm lizard)', 30.5],
    // ['Microvenator (small hunter)', 1.2],
    // ['Ornithomimus (bird mimic)', 4.6],
    // ['Oviraptor (egg robber)', 1.5],
    // ['Plateosaurus (flat lizard)', 7.9],
    // ['Sauronithoides (narrow-clawed lizard)', 2.0],
    // ['Seismosaurus (tremor lizard)', 45.7],
    // ['Spinosaurus (spiny lizard)', 12.2],
    // ['Supersaurus (super lizard)', 30.5],
    // ['Tyrannosaurus (tyrant lizard)', 15.2],
    // ['Ultrasaurus (ultra lizard)', 30.5],
    // ['Velociraptor (swift robber)', 1.8]]);
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
async function getStationsJson(url) {
    // There is a good example on using JavaScript fetch here:
    //      https://www.javascripttutorial.net/javascript-fetch-api/
    // I chose not to reproduce that content here (because it's much easier to
    // read on the web with pictures etc.).  If you want to explore JavaScript
    // fetch, please start there.

    // Key concept: A Promise is an object representing the eventual completion or failure of an asynchronous operation.

 //   let url = 'stations?hours_in_future=3';
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

//-----------------------------------------------------------------------------
// Function to dynamically create the dropdown content for station selection
//-----------------------------------------------------------------------------
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
    // Store the index of the selected station within the station array
    varGlobStationSelectedIndex = stationId;

    // Also update station details
    displayStationDetails(varGlobStationSelectedIndex);

}

//-----------------------------------------------------------------------------
// Range slider for time prediction
//-----------------------------------------------------------------------------

var slider = document.getElementById("sliderTimePrediction");
var output = document.getElementById("futureTime");

const CURRENT_DATETIME = new Date();
let predictedDateTime = new Date(CURRENT_DATETIME);

// Intialise display element with current time
output.innerHTML = CURRENT_DATETIME.toLocaleString();

// On event call which is invoked each time you drag the slider handle
slider.onchange = function() {
    // Write time prediction in hours to a global variable
    varGlobPredictionInHours =  this.value;
    // Add these hours to the current date & time and convert it into a string
    predictedDateTime = new Date(new Date().getTime() + this.value*60*60*1000).toLocaleString();
    // Update display element
    output.innerHTML = predictedDateTime;

    // Also update station details
    displayStationDetails(varGlobStationSelectedIndex);

    // debugging only!
    // console.log("slider value:" + slider.value.toString());
    // console.log(predictedDateTime);
}
