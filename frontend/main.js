// Kartta
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 15,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);






const blueIcon = L.divIcon({className: 'blue_icon'});


// Pyytää lentokenttien kordinaatit
async function gameSetup(){
  const response = await fetch('http://127.0.0.1:3000/creategame/20/200/jason')
  .then((response) => response.json())
  .then((location) => {
    let airports = location[0].data.gamedata
    console.log(airports[0])
    for (let i = 0; i < airports.length; i++) {
      const marker = L.marker([airports[i].latitude, airports[i].longitude]).addTo(map);
      marker.bindPopup(`You are here: <b>${airports[i].name}</b>`);
      marker.setIcon(blueIcon);
    }
  });
}

gameSetup();