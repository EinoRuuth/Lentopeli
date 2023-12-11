import { fuel } from "./main.js";
export async function playerSetup(url, Name, fuel_left, c_airport, airports_name, chance, marker) {
  //Haetaan pelaajan tiedot
  await fetch(url)
    .then((response) => response.json())
    .then((player) => {
      console.log(player)
      let earlier_latitude = player[0].data.latitude
      let earlier_longitude = player[0].data.longitude
      const old_marker = L.marker([
        earlier_latitude,
        earlier_longitude,
      ])
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
      fuel(
        fuel_url_2,
        airports_name,
        marker,
        chance,
        player_location,
        old_marker,
        earlier_latitude,
        earlier_longitude
      );
      }
    });
}
