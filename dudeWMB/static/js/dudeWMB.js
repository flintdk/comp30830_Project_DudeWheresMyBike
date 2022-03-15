"use strict";

// This function is called onload.  It's the 'parent process' if you like that
// kicks off all the work...
function onLoad() {
 
}

// draw markers
_.forEach(stations, function(station) {
    // console.log(station.name, station.number);
    var marker = new google.maps.Marker({
    position : {
    lat : station.position_lat,
    lng : station.position_lng
    },
    map : map,
    title : station.name,
    station_number : station.number
    });
    })



    _.forEach(stations, function(station) {
        // console.log(station.name, station.number);
        var marker = new google.maps.Marker(...);
        contentString = '<div id="content"><h1>' + station.name + '</h1></div>'
        + '<div id="station_availability"></div>';
        google.maps.event.addListener(marker, 'click', function() {
        drawInfoWindowChart(this);
        });
        })

 var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number,
        function(data) {
        data = JSON.parse(data.data);
        console.log('data', data);
        var node = document.createElement('div'),
        infowindow = new google.maps.InfoWindow(),
        chart = new google.visualization.ColumnChart(node);
        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', 'Time of Day');
        chart_data.addColumn('number', '#');
        _.forEach(data, function(row){
        chart_data.addRow([new Date(row[0]), row[1]]);
        })
        chart.draw(chart_data, options);
        infowindow.setContent(node);
        infowindow.open(marker.getMap(), marker);
        }).fail(function() {
        console.log( "error" );
        })

        36
        function drawHeatmap(me) {
        //console.log('toggle heatmap');
        console.log('clicked checkbox-1', me, me.prop('checked'));
        checked = me.prop('checked');
        if(checked) {
        if(heatmap == null) {
        var jqxhr = $.getJSON($SCRIPT_ROOT + "/heatmap",
        function(data) {
        console.log('data', data);
        var heatmapData = [];
        _.forEach(data.data, function(row) {
        heatmapData.push(
        {location: new google.maps.LatLng(row.position_lat, row.position_lng),
        weight: row.available_bikes});
        });
        heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: map
        });
        console.log(heatmap);
        heatmap.setMap(map);
        heatmap.set('radius', 40);
        //heatmap.setMap(heatmap.getMap() ? null : map);
        }).fail(function() {
        console.log('failed');
        });
        } else {
        heatmap.setMap(map);
        }
        } else {
        heatmap.setMap(null);
        }
        }