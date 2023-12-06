export async function playerSetup(url, Name){
    //Haetaan pelaajan tiedot
    await fetch(url)
    .then((response) => response.json())
    .then((player) => {
      console.log(player)
      const current_airport = document.getElementById("Current_Airport");
      current_airport.innerHTML = player[0].data.location;
  
      const fuel_amount = document.getElementById("Fuel-left");
      fuel_amount.innerHTML = 'Polttoainetta jäljellä: ' + player[0].data.fuel;

      const player_paragraph = document.getElementById("PlayerName");
      player_paragraph.innerHTML = Name;
  
      let treasure = player[0].data.treasures;
  
      if (treasure !== null){
        const inventory = document.getElementById("Resources");
        inventory.innerHTML = treasure
      }
    });
  }