export async function playerSetup(url, Name, fuel_left, c_airport){
    //Haetaan pelaajan tiedot
    await fetch(url)
    .then((response) => response.json())
    .then((player) => {
      console.log(player[0])
      const current_airport = document.getElementById("Current_Airport");
      if (c_airport == undefined) {
        current_airport.innerHTML = player[0].data.location;
      }
      else {
        current_airport.innerHTML = c_airport;
      }
      const fuel_amount = document.getElementById("Fuel-left");
      if (fuel_left == undefined) {
        fuel_amount.innerHTML = 'Polttoainetta jäljellä: ' + player[0].data.fuel;
      }
      else {
        fuel_amount.innerHTML = 'Polttoainetta jäljellä: ' + fuel_left;

      }
      const player_paragraph = document.getElementById("PlayerName");
      player_paragraph.innerHTML = Name;
  
      let treasure = player[0].data.treasures;
  
      if (treasure !== null){
        const inventory = document.getElementById("Resources");
        inventory.innerHTML = treasure
      }
    });
  }