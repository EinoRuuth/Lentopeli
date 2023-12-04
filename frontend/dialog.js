//Dialog
function dialog() {
    const dialog = document.getElementById("Menu-Dialog");
    const suomiBtn = document.getElementById("Suomi");
    const usaBtn = document.getElementById("Usa");
    const closeBtn = document.getElementById("Close");
    let dialog_value = ""
    
    dialog.showModal();
    
    usaBtn.addEventListener("click", () => {
      const x = document.getElementById('Player-Name').value;
      if (x == "" || x == null) {
        alert("Kirjoita nimi!");
        return false;
      }
      else {
        dialog_value = usaBtn.value
        document.cookie = 'country=' + dialog_value
        document.cookie = 'playerName=' + x
        location.href = "game.html";
      }
    });
    
    
    suomiBtn.addEventListener("click", () => {
      const x = document.getElementById('Player-Name').value;
      if (x == "" || x == null) {
        alert("Kirjoita nimi!");
        return false;
      }
      else {
        dialog_value = suomiBtn.value
        document.cookie = 'country=' + dialog_value
        document.cookie = 'playerName=' + x
        location.href = "game.html";
      }
    });
    
    closeBtn.addEventListener("click", () => {
      dialog_value = ""
      dialog.close();
    });


}