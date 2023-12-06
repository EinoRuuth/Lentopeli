export async function move(url){
    //Haetaan lentokenttien tiedot
    await fetch(url)
    .then((response) => response.json())
    .then((move_data) => {
    console.log(move_data)

    document.cookie = 'current_airport=' + move_data[0].data.data.name
    document.cookie = 'Fuel_left=' + move_data[0].data.data.fuel
    document.cookie = 'Moved=' + move_data[0].data.moved

    });
}
  

  