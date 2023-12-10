import { playerSetup } from "./player.js";
import { tic_tac_toe } from "./minigames.js";

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
  console.log(data);
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
const grayIcon = L.divIcon({
  className: ["gray_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34],
});

async function treasure(url) {
  //Haetaan pelaajan tiedot
  await fetch(url)
    .then((response) => response.json())
    .then((treasure_Data) => {
      console.log(treasure_Data);
      playerSetup("http://127.0.0.1:3000/playerdata", playerName);
    });
}

//minigame
function minigame(tchance, current_marker) {
  const dialog = document.getElementById("Game-Dialog");
  dialog.innerHTML = "";
  dialog.showModal();
  let random_number = 1;
  if ((random_number = 1)) {
    tic_tac_toe();
    const allBox = document.querySelectorAll(".box");
    const resultContainer = document.getElementById("result");
    const closeBtn = document.getElementById("close");

    const checkList = [];
    let currentPlayer = "CROSS";
    let winStatus = false;

    function areEqual(one, two) {
      if (one === two) return one;
      return false;
    }

    function checkEquality(currentPlayer, array) {
      for (const item of array) {
        const a = checkList[item[0]];
        const b = checkList[item[1]];
        if (areEqual(a, b) == currentPlayer) {
          return [item[0], item[1]];
        }
      }
      return false;
    }

    function blinkTheBox(val) {
      if (val) {
        for (const i of val) {
          const box = document.querySelector(`[data-box-num="${i}"]`);
          box.classList.add("blink");
        }
        return true;
      }
      return false;
    }

    function isWin() {
      let val = false;
      if (checkList[0] == currentPlayer) {
        val = checkEquality(currentPlayer, [
          [1, 2],
          [3, 6],
          [4, 8],
        ]);
        if (val && blinkTheBox([0, ...val])) return true;
      }

      if (checkList[8] == currentPlayer) {
        val = checkEquality(currentPlayer, [
          [2, 5],
          [6, 7],
        ]);
        if (val && blinkTheBox([8, ...val])) return true;
      }

      if (checkList[4] == currentPlayer) {
        val = checkEquality(currentPlayer, [
          [1, 7],
          [3, 5],
          [2, 6],
        ]);
        if (val && blinkTheBox([4, ...val])) return true;
      }

      return val;
    }

    function checkWin(len) {
      if (len >= 3 && isWin()) {
        winStatus = true;
        if (currentPlayer == "CROSS") {
          resultContainer.innerText = "X Won the Match.";
          let game_results = "True";
          treasure(
            "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
          );
          current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
          current_marker.setIcon(grayIcon);
          closeBtn.style.display = "flex";
          closeBtn.addEventListener("click", () => {
            dialog.close();
          });
        } else {
          resultContainer.innerText = "O Won the Match.";
          let game_results = "False";
          tchance = "0";
          treasure(
            "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
          );
          current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
          current_marker.setIcon(grayIcon);

          closeBtn.style.display = "flex";
          closeBtn.addEventListener("click", () => {
            dialog.close();
          });
        }
      } else if (len == 8) {
        winStatus = true;
        resultContainer.innerText = "= Match Draw.";
        let game_results = "False";
        tchance = "0";
        treasure(
          "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
        );
        current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
        current_marker.setIcon(grayIcon);

        closeBtn.style.display = "flex";
        closeBtn.addEventListener("click", () => {
          dialog.close();
        });
      }
      return winStatus;
    }

    function boxClick(targetBox, player, boxNum) {
      checkList[boxNum] = player;
      targetBox.classList.add(player.toLowerCase());
    }

    function handleBoxClick(e) {
      let len = checkList.filter(Boolean).length;
      const boxNum = parseInt(e.target.getAttribute("data-box-num"));
      let boxNumForBot;

      if (!winStatus && !checkList[boxNum]) {
        currentPlayer = "CROSS";
        boxClick(e.target, "CROSS", boxNum);

        if (checkWin(len) === false) {
          len = checkList.filter(Boolean).length;
          currentPlayer = "ZERO";
          while (len < 9) {
            boxNumForBot = Math.floor(Math.random() * 9);
            if (!checkList[boxNumForBot]) {
              boxClick(allBox[boxNumForBot], "ZERO", boxNumForBot);
              checkWin(len);
              break;
            }
          }
        }
      }
    }

    allBox.forEach((item) => {
      item.addEventListener("click", (e) => handleBoxClick(e));
    });
  }
}

//Liikkumis funktio toiselle kentälle
async function move(move_url, current_marker, tchance) {
  //Haetaan lentokenttien tiedot
  await fetch(move_url)
    .then((response) => response.json())
    .then((move_data) => {
      console.log(move_data)
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
async function fuel(fuel_url, current_airport, marker, tchance) {
  //Haetaan lentokenttien tiedot
  await fetch(fuel_url)
    .then((response) => response.json())
    .then((fuel_data) => {
      console.log(fuel_data);
      //Fuel datasta laitetaan muuttujiin polttoaineen hinta, marker muuttuja gamesetup funktiosta
      //Ja pelaajan edelliset kordinaatit.
      let fuel_cost = fuel_data[0].data.fuel;
      let fuel_distance = fuel_data[0].data.pituus;
      let current_marker = marker;
      console.log(tchance);
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
            let player_location = player.name;

            let fuel_url =
              "http://127.0.0.1:3000/calculatefuel/" +
              player_location +
              "/" +
              airports[i].name;
            let fuel_url_2 = fuel_url.replaceAll(" ", "_");
            fuel(
              fuel_url_2,
              airports[i].name,
              marker,
              airports[i].treasurechance
            );
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
startStopwatch();
