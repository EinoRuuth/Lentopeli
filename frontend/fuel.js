export async function fuel(url){
    //Haetaan lentokenttien tiedot
    await fetch(url)
    .then((response) => response.json())
    .then((fuel_data) => {
    console.log(fuel_data)

    document.cookie = 'Fuel_cost=' + fuel_data[0].data.Fuel
    document.cookie = 'Fuel_distance=' + fuel_data[0].data.distance
    });
}