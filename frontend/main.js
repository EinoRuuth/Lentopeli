import { playerSetup } from './player.js';
import { tic_tac_toe } from './minigames.js';


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

var startTime; // to keep track of the start time
var stopwatchInterval; // to keep track of the interval
var elapsedPausedTime = 0; // to keep track of the elapsed time while stopped

function startStopwatch() {
  if (!stopwatchInterval) {
    startTime = new Date().getTime() - elapsedPausedTime; // get the starting time by subtracting the elapsed paused time from the current time
    stopwatchInterval = setInterval(updateStopwatch, 1000); // update every second
  }
}

function stopStopwatch() {
  clearInterval(stopwatchInterval); // stop the interval
  elapsedPausedTime = new Date().getTime() - startTime; // calculate elapsed paused time
  stopwatchInterval = null; // reset the interval variable
}

function updateStopwatch() {
  var currentTime = new Date().getTime(); // get current time in milliseconds
  var elapsedTime = currentTime - startTime; // calculate elapsed time in milliseconds
  var seconds = Math.floor(elapsedTime / 1000) % 60; // calculate seconds
  var minutes = Math.floor(elapsedTime / 1000 / 60) % 60; // calculate minutes
  var hours = Math.floor(elapsedTime / 1000 / 60 / 60); // calculate hours
  var displayTime = pad(hours) + ":" + pad(minutes) + ":" + pad(seconds); // format display time
  document.getElementById("stopwatch").innerHTML = displayTime; // update the display
}

function pad(number) {
  // add a leading zero if the number is less than 10
  return (number < 10 ? "0" : "") + number;
}

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
const grayIcon = L.divIcon({
  className: ["gray_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34]
});
//minigame
function minigame() {
  const dialog = document.getElementById("Game-Dialog");
  dialog.showModal(); 
  let random_number = 1;
  if (random_number = 1) {
    tic_tac_toe()
    const game = {
      xTurn: true,
      xState: [],
      oState: [],
      winningStates: [
          // Rows
          ['0', '1', '2'],
          ['3', '4', '5'],
          ['6', '7', '8'],
  
          // Columns
          ['0', '3', '6'],
          ['1', '4', '7'],
          ['2', '5', '8'],
  
          // Diagonal
          ['0', '4', '8'],
          ['2', '4', '6']
      ]
      }
      document.addEventListener('click', event => {
        const target = event.target
        const isCell = target.classList.contains('grid-cell')
        const isDisabled = target.classList.contains('disabled')
    
        if (isCell && !isDisabled) {
            // The player clicked on a cell that is still empty
            const cellValue = target.dataset.value
            game.xTurn === true
                ? game.xState.push(cellValue)
                : game.oState.push(cellValue)

            target.classList.add('disabled')
            target.classList.add(game.xTurn ? 'x' : 'o')

            
            game.xTurn = !game.xTurn
            if (!document.querySelectorAll('.grid-cell:not(.disabled)').length) {
              document.querySelector('.game-over').classList.add('visible')
              document.querySelector('.game-over-text').textContent = 'Draw!'
            }
            game.winningStates.forEach(winningState => {
              const xWins = winningState.every(state => game.xState.includes(state))
              const oWins = winningState.every(state => game.oState.includes(state))
            
              if (xWins || oWins) {
                  document.querySelectorAll('.grid-cell').forEach(cell => cell.classList.add('disabled'))
                  document.querySelector('.game-over').classList.add('visible')
                  document.querySelector('.game-over-text').textContent = xWins
                      ? 'X wins!'
                      : 'O wins!'
              }
          }) 

        }
    })

}
}

//Liikkumis funktio toiselle kentälle
async function move(move_url, current_marker, player_longitude, player_latitude){
  //Haetaan lentokenttien tiedot
  await fetch(move_url)
  .then((response) => response.json())
  .then((move_data) => {


      //Moven datasta laitetaan muuttujiin mitä polttoaineesta on jäljellä,
      //Lentokentän nimi mihin mennään ja moved arvo.
      let fuel_left = move_data[0].data.data.fuel;
      let current_airport = move_data[0].data.data.name;
      let moved = move_data[0].data.moved;

      //Katsotaan onko moved true eli onko lentokentälle liikkuminen onnistunut
      //Ja muutetaan nappuloiden popup tekstiä ja väriä.
      if (moved === true) {
        const player_marker = L.marker([player_latitude, player_longitude]);
        player_marker.setIcon(grayIcon);
        player_marker.bindPopup(`Olet jo käynyt täällä`);
        playerSetup('http://127.0.0.1:3000/playerdata', playerName, fuel_left, current_airport)
        current_marker.setIcon(greenIcon);
        minigame();

        //Kutsuun playersetup funktiota päivitetyillä tidoilla tietokannassa
    }
  });
}


//Polttoaineen laskenta funktio
async function fuel(fuel_url, current_airport, marker, longitude, latitude){
  //Haetaan lentokenttien tiedot
  await fetch(fuel_url)
  .then((response) => response.json())
  .then((fuel_data) => {
    //Fuel datasta laitetaan muuttujiin polttoaineen hinta, marker muuttuja gamesetup funktiosta
    //Ja pelaajan edelliset kordinaatit.
    let fuel_cost = fuel_data[0].data.Fuel;
    let current_marker = marker
    let player_longitude = longitude
    let player_latitude = latitude

    //Kutsutaan move funktiota
    let move_url = 'http://127.0.0.1:3000/moveplayer/' + current_airport + '/' + fuel_cost;
    let move_url_2 = move_url.replaceAll(" ", "_");
    move(move_url_2, current_marker, player_longitude, player_latitude);
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
    const longitude = location[0].data.playerdata.longitude
    const latitude = location[0].data.playerdata.latitude

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
          fuel(fuel_url_2, airports[i].name, marker, longitude, latitude);


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
startStopwatch();
