const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);


async function gameSetup(){
  const response = await fetch('http://127.0.0.1:3000/creategame/20/200');
  const jsondata = response.json();

  console.log(jsondata);
}

gameSetup();