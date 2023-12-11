import { fuel } from "./main.js";
export async function playerSetup(url, Name, fuel_left, c_airport, airports_name, chance, marker) {
  //Haetaan pelaajan tiedot
  await fetch(url)
    .then((response) => response.json())
    .then((player) => {
      
      const current_airport = document.getElementById("Current_Airport");
      if (c_airport == undefined) {
        current_airport.innerHTML = player[0].data.location;
      } else {
        current_airport.innerHTML = c_airport;
      }
      const fuel_amount = document.getElementById("Fuel-left");
      if (fuel_left == undefined) {
        fuel_amount.innerHTML =
          "Polttoainetta jäljellä: " + player[0].data.fuel;
      } else {
        fuel_amount.innerHTML = "Polttoainetta jäljellä: " + fuel_left;
      }
      const player_paragraph = document.getElementById("PlayerName");
      player_paragraph.innerHTML = Name;
      if (marker != undefined) {
      let player_location = player[0].data.location;
      let fuel_url =
        "http://127.0.0.1:3000/calculatefuel/" +
        player_location +
        "/" +
        airports_name;
      let fuel_url_2 = fuel_url.replaceAll(" ", "_");
      console.log(fuel_url_2)
      fuel(
        fuel_url_2,
        airports_name,
        marker,
        chance
      );
      }
    });
}
