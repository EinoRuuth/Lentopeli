//Dialog
function dialog() {
    const dialog = document.getElementById("Menu-Dialog");
    const suomiBtn = document.getElementById("Suomi");
    const usaBtn = document.getElementById("Usa");
    const closeBtn = document.getElementById("Close");
    let dialog_value = ""
    
    dialog.showModal();
    
    usaBtn.addEventListener("click", () => {
      dialog_value = usaBtn.value
      document.cookie = 'country=' + dialog_value
      console.log(dialog_value)
    });
    
    
    suomiBtn.addEventListener("click", () => {
      dialog_value = suomiBtn.value
      document.cookie = 'country=' + dialog_value
      console.log(dialog_value)
    });
    
    closeBtn.addEventListener("click", () => {
      dialog_value = ""
      dialog.close();
    });


}