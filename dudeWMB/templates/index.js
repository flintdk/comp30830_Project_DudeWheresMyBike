// Function to initialize and add the map
function initMap() {
    // Location of Dublin
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // Map, centered at Dublin
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: dublin,
    });
    // Intial marker, positioned at Dublin
    const marker = new google.maps.Marker({
      position: dublin,
      map: map,
      icon: 'bikeIcon.svg'
    });

    // Intial Info
    var infoWindow = new google.maps.InfoWindow({
        content:'<h1>Dublin</h1>'
    });

    // Listener
    marker.addListener('click', function(){
        infoWindow.open(map, marker);
    })
  }