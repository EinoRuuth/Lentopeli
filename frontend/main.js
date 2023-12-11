import { tic_tac_toe } from "./minigames.js";
import { playerSetup } from "./player.js";
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
  if (parts.length === 2) return parts.pop().split(";").shift();
}
const country = getCookie("country");
const playerName = getCookie("playerName");

// Kartta
const map = L.map("map", { tap: false });
L.tileLayer("https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", {
  minZoom: 7,
  maxZoom: 7,
  subdomains: ["mt0", "mt1", "mt2", "mt3"],
}).addTo(map);
map.zoomControl.remove();

// Quit button
const quitbutton = document.getElementById("Quit");
quitbutton.addEventListener("click", async function () {
  const response = await fetch("http://127.0.0.1:3000/cleardata");
  const data = await response.json();
});

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
  popupAnchor: [1, -34],
});
const greenIcon = L.divIcon({
  className: ["green_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34],
});

export async function treasure(url) {
  //Haetaan pelaajan tiedot
  await fetch(url)
    .then((response) => response.json())
    .then((treasure_Data) => {
      console.log(treasure_Data);
      let found = treasure_Data[0].data.found;
      let win = treasure_Data[0].data.won;
      let loss = treasure_Data[0].data.loss;
      let reason = treasure_Data[0].data.data;

      console.log(found)
      console.log(win)
      console.log(loss)

      if(found != undefined) {
        if (found = true) {
          const inventory = document.getElementById("Resources");
          const p = document.createElement("p");
          p.innerText = treasure_Data[0].data.item;
          inventory.append(p);
        }
      }
      playerSetup("http://127.0.0.1:3000/playerdata", playerName);
      if (loss === "true") {
        const dialog = document.getElementById("Game-Dialog");
        dialog.innerHTML = "";

        const p1 = document.createElement("p");
        p1.classList.add("Reason");
        p1.innerText = reason;
        dialog.append(p1);

        const p2 = document.createElement("p");
        p2.classList.add("Move-Fuelcost");
        p2.innerText = "Hävisit pelin";
        dialog.append(p2);
  
        const button1 = document.createElement("button");
        button1.setAttribute("id", "Game-end");
        button1.innerText = "Lopeta peli";
        dialog.append(button1);  
        
        const button2 = document.createElement("button");
        button2.setAttribute("id", "Game-again");
        button2.innerText = "Pelaa uudelleen";
        dialog.append(button2);
  
        //Kutsutaan move funktiota
        button1.style.display = "block";
        button1.addEventListener("click", () => {
          dialog.close();
          location.href = "menu.html";
        });
      }
      if(win === true) {
        const dialog = document.getElementById("Game-Dialog");
        dialog.innerHTML = "";

        const p1 = document.createElement("p");
        p1.classList.add("Reason");
        p1.innerText = reason;
        dialog.append(p1);

        const p2 = document.createElement("p");
        p2.classList.add("Move-Fuelcost");
        p2.innerText = "Voitit pelin";
        dialog.append(p2);
  
        const button1 = document.createElement("button");
        button1.setAttribute("id", "Game-end");
        button1.innerText = "Lopeta peli";
        dialog.append(button1);  
        
        const button2 = document.createElement("button");
        button2.setAttribute("id", "Game-again");
        button2.innerText = "Pelaa uudelleen";
        dialog.append(button2);
  
        //Kutsutaan move funktiota
        button1.style.display = "block";
        button1.addEventListener("click", () => {
          dialog.close();
          location.href = "menu.html";
        });
      }
    });
}

//minigame
function minigame(tchance, current_marker) {
  const dialog = document.getElementById("Game-Dialog");
  dialog.innerHTML = "";
  dialog.showModal();
  let random_number = 1;
  if ((random_number = 1)) {
    tic_tac_toe(tchance, current_marker);
  }
}

//Liikkumis funktio toiselle kentälle
async function move(move_url, current_marker, tchance) {
  //Haetaan lentokenttien tiedot
  await fetch(move_url)
    .then((response) => response.json())
    .then((move_data) => {
      console.log(move_data);

      //Moven datasta laitetaan muuttujiin mitä polttoaineesta on jäljellä,
      //Lentokentän nimi mihin mennään ja moved arvo.
      let fuel_left = move_data[0].data.data.fuel;
      let current_airport = move_data[0].data.data.name;
      let moved = move_data[0].data.moved;
      //Katsotaan onko moved true eli onko lentokentälle liikkuminen onnistunut
      //Ja muutetaan nappuloiden popup tekstiä ja väriä.
      if (moved === true) {
        playerSetup(
          "http://127.0.0.1:3000/playerdata",
          playerName,
          fuel_left,
          current_airport
        );
        current_marker.setIcon(greenIcon);
        minigame(tchance, current_marker);

        //Kutsuun playersetup funktiota päivitetyillä tidoilla tietokannassa
      }
    });
}

//Polttoaineen laskenta funktio
export async function fuel(fuel_url, current_airport, marker, tchance) {
  //Haetaan lentokenttien tiedot
  await fetch(fuel_url)
    .then((response) => response.json())
    .then((fuel_data) => {
      //Fuel datasta laitetaan muuttujiin polttoaineen hinta, marker muuttuja gamesetup funktiosta
      //Ja pelaajan edelliset kordinaatit.
      let fuel_cost = fuel_data[0].data.fuel;
      let fuel_distance = fuel_data[0].data.pituus;
      let current_marker = marker;
      const dialog = document.getElementById("Game-Dialog");
      dialog.innerHTML = "";
      dialog.showModal();

      const h2 = document.createElement("h2");
      h2.classList.add("Move-Header");
      h2.innerText = current_airport;

      dialog.append(h2);
    
      const p1 = document.createElement("p");
      p1.classList.add("Move-Fuelcost");
      p1.innerText = "Matkan hinta on " + fuel_cost + " Polttoainetta";

      dialog.append(p1);

      const p2 = document.createElement("p");
      p2.classList.add("Move-Distance");
      p2.innerText = "Matkan pituus on " + fuel_distance + " Kilometriä";

      dialog.append(p2);

      const button1 = document.createElement("button");
      button1.setAttribute("id", "Move-Dontfly");
      button1.innerText = "Älä lennä";
      dialog.append(button1);  
      
      const button2 = document.createElement("button");
      button2.setAttribute("id", "Move-Fly");
      button2.innerText = "Lennä " + current_airport;
      dialog.append(button2);

      //Kutsutaan move funktiota
      button1.style.display = "block";
      button1.addEventListener("click", () => {
        dialog.close();
      });

      button2.style.display = "block";
      button2.addEventListener("click", () => {
        let move_url =
        "http://127.0.0.1:3000/moveplayer/" + current_airport + "/" + fuel_cost;
        let move_url_2 = move_url.replaceAll(" ", "_");
        move(move_url_2, current_marker, tchance);

      });

    });
}
// Pyytää lentokenttien kordinaatit
async function gameSetup(url) {
  //Haetaan lentokenttien tiedot
  displayLoading();
  await fetch(url)
    .then((response) => response.json())
    .then((location) => {
      hideLoading();
      playerSetup("http://127.0.0.1:3000/playerdata", playerName);
      startStopwatch();
      let player = location[0].data.playerdata;
      let airports = location[0].data.gamedata;
      const longitude = location[0].data.playerdata.longitude;
      const latitude = location[0].data.playerdata.latitude;

      map.setView([latitude, longitude], 7);
      // Laittaa lentokenttien sijainnit kartalle
      for (let i = 0; i < airports.length; i++) {
        const marker = L.marker([
          airports[i].latitude,
          airports[i].longitude,
        ]).addTo(map);

        // Kenttä missä pelaajan on
        if (
          player.longitude === airports[i].longitude &&
          player.latitude === airports[i].latitude
        ) {
          marker.bindPopup(`Olet täällä: <b>${airports[i].name}</b>`);
          marker.openPopup();
          marker.setIcon(greenIcon);
        }

        // Muut kentät
        else {
          marker.setIcon(blueIcon);
          const popupContent = document.createElement("div");
          const h4 = document.createElement("h4");
          h4.innerHTML = airports[i].name;
          popupContent.append(h4);

          const goButton = document.createElement("button");
          goButton.setAttribute("id", "Fly-Button");
          goButton.innerHTML = "Lennä tänne";

          popupContent.append(goButton);

          const p = document.createElement("p");
          p.innerHTML = `Mahdollisuus: ${airports[i].treasurechance} %`;
          popupContent.append(p);

          marker.bindPopup(popupContent);
          goButton.addEventListener("click", function () {
            playerSetup("http://127.0.0.1:3000/playerdata", playerName, undefined, undefined, airports[i].name, airports[i].treasurechance, marker);

          });
        }
      }
    });
}

//Kutsutaan gameSetup funktiota ja katsotaan ettei country ja playerName ole tyhjiä
if (country !== "" && playerName !== "") {
  if (country === "US") {
    gameSetup(
      "http://127.0.0.1:3000/creategame/50/500/" + playerName + "/" + country
    );
  } else {
    gameSetup(
      "http://127.0.0.1:3000/creategame/20/200/" + playerName + "/" + country
    );
  }
}
