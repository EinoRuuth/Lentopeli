export async function fuel(url){
    //Haetaan lentokenttien tiedot
    await fetch(url)
    .then((response) => response.json())
    .then((data) => {
    console.log(url)
    console.log(data)
    
    });
}