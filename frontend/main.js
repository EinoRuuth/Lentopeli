import { fuel } from './fuel.js';
import { move } from './move.js';

//Loading screen karttaa varten
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

//Cookieiden haku funktio
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const country = getCookie("country");
const playerName = getCookie("playerName");

// Kartta
const map = L.map('map', {tap: false});
  L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    minZoom: 7,
    maxZoom: 7,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
  }).addTo(map);
  map.zoomControl.remove();

// Quit button
const quitbutton = document.getElementById('Quit');
quitbutton.addEventListener('click', async function() {
  const response = await fetch('http://127.0.0.1:3000/cleardata');
  const data = await response.json();
  console.log(data)
})

// Lentokenttien iconit kartalla
const blueIcon = L.divIcon({
  className: ["blue_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34]
  ,
});
const greenIcon = L.divIcon({
  className: ["green_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34]
});

// Pyytää lentokenttien kordinaatit
async function gameSetup(gameurl,playerurl){

  //Haetaan lentokenttien tiedot
  displayLoading();
  await fetch(gameurl)
  .then((response) => response.json())
  .then((location) => {
    hideLoading();
    let player = location[0].data.playerdata
    let airports = location[0].data.gamedata
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
        goButton.setAttribute('id', 'Fly-Button');
        goButton.innerHTML = 'Lennä tänne';

        popupContent.append(goButton);

        const p = document.createElement('p');
        p.innerHTML = `Mahdollisuus: ${airports[i].treasurechance} %`;
        popupContent.append(p);

        marker.bindPopup(popupContent);
        goButton.addEventListener('click', function () {
          let player_location = player.name
          let fuel_url = 'http://127.0.0.1:3000/calculatefuel/' + player_location + '/' + airports[i].name;
          let fuel_url_2 = fuel_url.replaceAll(" ", "_");
          let move_url = 'http://127.0.0.1:3000/moveplayer/' + airports[i].name + '/' + '1';
          let move_url_2 = move_url.replaceAll(" ", "_");
          fuel(fuel_url_2);
          move(move_url_2);
        })
      }
    }
  });

  //Haetaan pelaajan tiedot
  await fetch(playerurl)
  .then((response) => response.json())
  .then((player) => {
    const current_airport = document.getElementById("Current_Airport");
    current_airport.innerHTML = player[0].data.location;

    const fuel_amount = document.getElementById("Fuel-left");
    fuel_amount.innerHTML = 'Polttoainetta jäljellä: ' + player[0].data.fuel;
    
    const player_paragraph = document.getElementById("PlayerName");
    player_paragraph.innerHTML = playerName;

    let treasure = player[0].data.treasures;

    if (treasure !== null){
      const inventory = document.getElementById("Resources");
      inventory.innerHTML = treasure
    }
  });
}

//Kutsutaan gameSetuop funktiota ja katsotaan ettei country ja playerName ole tyhjiä
if (country !== "" && playerName !== "") {
  if (country === "US") {
    gameSetup('http://127.0.0.1:3000/creategame/50/500/' + playerName + "/" + country,'http://127.0.0.1:3000/playerdata');
  }
  else {
    gameSetup('http://127.0.0.1:3000/creategame/20/200/' + playerName + "/" + country,'http://127.0.0.1:3000/playerdata');
  }
}

