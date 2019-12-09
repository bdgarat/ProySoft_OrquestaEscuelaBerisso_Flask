var mymap = L.map('mapid').setView([-34.8799,-57.8826], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 30,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);


// ICONOS
var home = L.AwesomeMarkers.icon({
    icon: 'home',
    iconSize:     [38, 95], // size of the icon
    shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
  });

// CONTROL
var routerControl = L.Routing.control({
    language: 'es',
		formatter:  new L.Routing.Formatter({
			language: 'es' 
        }),
    routeWhileDragging: true,
    showAlternatives: true
  }).addTo(mymap);


// RUTAS  
function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}

mymap.on('click', function(e) {
    
    var container = L.DomUtil.create('div'),
    startBtn = createButton('Iniciar recorrido aquí', container),
    destBtn = createButton('Finalizar recorrido aquí', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(mymap);
    
    L.DomEvent.on(startBtn, 'click', function() {
        routerControl.spliceWaypoints(0, 1, e.latlng);
        mymap.closePopup();
    });

    L.DomEvent.on(destBtn, 'click', function() {
        routerControl.spliceWaypoints(routerControl.getWaypoints().length - 1, 1, e.latlng);
        mymap.closePopup();
    });
});


// VOLAR (SELECCIONAR UN NUCLEO)
document.getElementById('select-location')
    .addEventListener('change', function(e) {
        let coords = e.target.value.split(",");
        L.marker(coords, {icon: home }).addTo(mymap);
        mymap.flyTo(coords, 16);
    })
