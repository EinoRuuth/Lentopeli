const loader = document.getElementById("loader");
const loader_text = document.getElementById("loader_text");

function displayLoading() {
  loader.classList.add("display");
  loader_text.classList.add("display");

}

function hideLoading() {
  loader.classList.remove("display");
  loader_text.classList.remove("display");

}

//Dialog
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const country = getCookie("country");
const playerName = getCookie("playerName");

console.log(country)
console.log(playerName)

// Kartta
const map = L.map('map', {tap: false});
  L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 10,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
  }).addTo(map);

// Onnin tehtävä
// Tee tähän funktio joka ottaa Pelaajan tiedot backendistä lähetetystä jsonista
// Laita tiedot kartan vieressä oleviin laatikoihin nätin näköisesti











// Quit button
const quitbutton = document.getElementById('Quit');
quitbutton.addEventListener('click', async function() {
  const response = await fetch('http://127.0.0.1:3000/cleardata');
  const data = await response.json();
  console.log(data)
})

// Lentokenttien iconit kartalla
const blueIcon = L.divIcon({className: 'blue_icon'});
const greenIcon = L.divIcon({className: 'green_icon'});




// Pyytää lentokenttien kordinaatit
async function gameSetup(url){
  displayLoading();
  fetch(url)
  .then((response) => response.json())
  .then((location) => {
    hideLoading();
    console.log(url)
    let player = location[0].data.playerdata
    let airports = location[0].data.gamedata
    console.log(player)
    console.log(airports)
    let longitude = location[0].data.playerdata.longitude
    let latitude = location[0].data.playerdata.latitude
    map.setView([latitude, longitude], 7);
    // Laittaa lentokenttien sijainnit kartalle
    for (let i = 0; i < airports.length; i++) {
      const marker = L.marker([airports[i].latitude, airports[i].longitude]).addTo(map);

      // Kenttä missä pelaajan on
      if (player.longitude === airports[i].longitude && player.latitude === airports[i].latitude) {
        marker.bindPopup(`Olet täällä: <b>${airports[i].name}</b>`);
        marker.openPopup();
        marker.setIcon(greenIcon);
      }

      // Muut kentät
      else {
        marker.setIcon(blueIcon);
        const popupContent = document.createElement('div');
        const h4 = document.createElement('h4');
        h4.innerHTML = airports[i].name;
        popupContent.append(h4);

        const goButton = document.createElement('button');
        goButton.classList.add('Fly-Button');
        goButton.innerHTML = 'Lennä tänne';

        popupContent.append(goButton);

        const p = document.createElement('p');
        p.innerHTML = `Mahdollisuus: ${airports[i].treasurechance} %`;
        popupContent.append(p);

        marker.bindPopup(popupContent);
      }
    }
  });

}

if (country !== "" && playerName !== "") {
  gameSetup('http://127.0.0.1:3000/creategame/20/200/' + playerName + "/" + country);
}

