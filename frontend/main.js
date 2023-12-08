import { playerSetup } from './player.js';

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
  document.cookie = 'current_airport=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
  document.cookie = 'Fuel_left=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
  document.cookie = 'Moved=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
  document.cookie = 'Fuel_cost=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
  document.cookie = 'Fuel_distance=; expires=Thu, 01-Jan-70 00:00:01 GMT;';

  
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
async function move(move_url){
  //Haetaan lentokenttien tiedot
  await fetch(move_url)
  .then((response) => response.json())
  .then((move_data) => {
      console.log(move_data)
      let fuel_left = move_data[0].data.Fuel;
      let current_airport = move_data[0].data.Fuel;

      playerSetup('http://127.0.0.1:3000/playerdata', playerName, fuel_left, current_airport)
  });
}
async function fuel(fuel_url, current_airport){
  //Haetaan lentokenttien tiedot
  await fetch(fuel_url)
  .then((response) => response.json())
  .then((fuel_data) => {
    let fuel_cost = fuel_data[0].data.Fuel;

    let move_url = 'http://127.0.0.1:3000/moveplayer/' + current_airport + '/' + fuel_cost;
    let move_url_2 = move_url.replaceAll(" ", "_");
    move(move_url_2);
  });
}

// Pyytää lentokenttien kordinaatit
async function gameSetup(url){
  //Haetaan lentokenttien tiedot
  displayLoading();
  await fetch(url)
  .then((response) => response.json())
  .then((location) => {
    hideLoading();
    playerSetup('http://127.0.0.1:3000/playerdata', playerName)
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
          fuel(fuel_url_2, airports[i].name);

        })
      }
    }
  });
}

//Kutsutaan gameSetup funktiota ja katsotaan ettei country ja playerName ole tyhjiä
if (country !== "" && playerName !== "") {
  if (country === "US") {
    gameSetup('http://127.0.0.1:3000/creategame/50/500/' + playerName + "/" + country);
  }
  else {
    gameSetup('http://127.0.0.1:3000/creategame/20/200/' + playerName + "/" + country);
  }
}

