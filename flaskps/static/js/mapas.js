var mymap = L.map('mapid').setView([-34.8799,-57.8826], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 30,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var marker = L.marker([-34.8799,-57.8826]).addTo(mymap);
var marker = L.marker([-34.8748,-57.8715]).addTo(mymap);
var marker = L.marker([-34.8783,-57.8907]).addTo(mymap);
var marker = L.marker([-34.9157,-57.9482]).addTo(mymap);



document.getElementById('select-location')
    .addEventListener('change', function(e) {
        let coords = e.target.value.split(",");
        mymap.flyTo(coords, 18);
    })



// var popup = L.popup();

// function onMapClick(e) {
//     popup
//         .setLatLng(e.latlng)
//         .setContent("You clicked the map at " + e.latlng.toString())
//         .openOn(mymap);
// }

// mymap.on('click', onMapClick);