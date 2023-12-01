// Kartta
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 15,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

// Onnin tehtävä
// Tee tähän funktio joka ottaa Pelaajan tiedot backendistä lähetetystä jsonista
// Laita tiedot kartan vieressä oleviin laatikoihin nätin näköisesti











//


// Lentokenttien iconit kartalla
const blueIcon = L.divIcon({className: 'blue_icon'});
const greenIcon = L.divIcon({className: 'green_icon'});


// Pyytää lentokenttien kordinaatit
async function gameSetup(url){
  fetch(url)
  .then((response) => response.json())
  .then((location) => {
    let player = location[0].data.playerdata
    let airports = location[0].data.gamedata
    console.log(player)
    console.log(airports)

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
        goButton.classList.add('Fly-Button');
        goButton.innerHTML = 'Lennä tänne';

        const quitbutton = document.createElement('button');
        quitbutton.classList.add('Fly-Button');
        quitbutton.innerHTML = 'Quit';

        popupContent.append(goButton);
        popupContent.append(quitbutton);

        const p = document.createElement('p');
        p.innerHTML = `Mahdollisuus: ${airports[i].treasurechance} %`;
        popupContent.append(p);

        marker.bindPopup(popupContent);
        quitbutton.addEventListener('click', async function() {
          const response = await fetch('http://127.0.0.1:3000/cleardata');
          const data = await response.json();
          console.log(data)
        })
      }
    }
  });
}

gameSetup('http://127.0.0.1:3000/creategame/20/200/jason');