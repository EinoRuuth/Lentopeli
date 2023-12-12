import { treasure } from "./main.js";

export function tic_tac_toe(tchance, current_marker, current_airport) {
  const dialog = document.getElementById("Game-Dialog");

  const container_div = document.createElement("div");
  container_div.classList.add("container");
  dialog.append(container_div);

  const h1 = document.createElement("h1");
  container_div.append(h1);

  const state = document.createElement("div");
  state.classList.add("state");
  container_div.append(state);

  const p = document.createElement("p");
  p.setAttribute("id", "result");
  container_div.append(p);

  const game_container = document.createElement("div");
  game_container.classList.add("game-container");
  container_div.append(game_container);

  const wrap = document.createElement("div");
  wrap.classList.add("wrap");
  game_container.append(wrap);

  const button_div = document.createElement("div");
  button_div.classList.add("Button-div");
  container_div.append(button_div);

  const button = document.createElement("button");
  button.setAttribute("id", "close");
  button.innerText = "Sulje minipeli";
  button_div.append(button);

  let i = 0;
  while (i < 9) {
    const section = document.createElement("section");
    section.classList.add("box");
    section.setAttribute("data-box-num", i);
    wrap.append(section);
    i++;
  }

  const allBox = document.querySelectorAll(".box");
  const resultContainer = document.getElementById("result");
  const closeBtn = document.getElementById("close");

  const checkList = [];
  let currentPlayer = "CROSS";
  let winStatus = false;

  function areEqual(one, two) {
    if (one === two) return one;
    return false;
  }

  function checkEquality(currentPlayer, array) {
    for (const item of array) {
      const a = checkList[item[0]];
      const b = checkList[item[1]];
      if (areEqual(a, b) == currentPlayer) {
        return [item[0], item[1]];
      }
    }
    return false;
  }

  function blinkTheBox(val) {
    if (val) {
      for (const i of val) {
        const box = document.querySelector(`[data-box-num="${i}"]`);
        box.classList.add("blink");
      }
      return true;
    }
    return false;
  }

  function isWin() {
    let val = false;
    if (checkList[0] == currentPlayer) {
      val = checkEquality(currentPlayer, [
        [1, 2],
        [3, 6],
        [4, 8],
      ]);
      if (val && blinkTheBox([0, ...val])) return true;
    }

    if (checkList[8] == currentPlayer) {
      val = checkEquality(currentPlayer, [
        [2, 5],
        [6, 7],
      ]);
      if (val && blinkTheBox([8, ...val])) return true;
    }

    if (checkList[4] == currentPlayer) {
      val = checkEquality(currentPlayer, [
        [1, 7],
        [3, 5],
        [2, 6],
      ]);
      if (val && blinkTheBox([4, ...val])) return true;
    }

    return val;
  }

  function checkWin(len) {
    if (len >= 3 && isWin()) {
      winStatus = true;
      if (currentPlayer == "CROSS") {
        resultContainer.innerText = "Voitit minipelin.";
        let game_results = "True";
        treasure(
          "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
        );
        closeBtn.style.display = "block";
        closeBtn.addEventListener("click", () => {
          current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
          dialog.close();
        });
      } else {
        resultContainer.innerText = "Hävisit minipelin.";
        let game_results = "False";
        tchance = "0";
        treasure(
          "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
        );

        closeBtn.style.display = "block";
        closeBtn.addEventListener("click", () => {
          current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
          dialog.close();
        });
      }
    } else if (len == 8) {
      winStatus = true;
      resultContainer.innerText = "Tasapeli";
      let game_results = "False";
      tchance = "0";
      treasure(
        "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
      );

      closeBtn.style.display = "block";
      closeBtn.addEventListener("click", () => {
        current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
        dialog.close();
      });
    }
    return winStatus;
  }

  function boxClick(targetBox, player, boxNum) {
    checkList[boxNum] = player;
    targetBox.classList.add(player.toLowerCase());
  }

  function handleBoxClick(e) {
    let len = checkList.filter(Boolean).length;
    const boxNum = parseInt(e.target.getAttribute("data-box-num"));
    let boxNumForBot;

    if (!winStatus && !checkList[boxNum]) {
      currentPlayer = "CROSS";
      boxClick(e.target, "CROSS", boxNum);

      if (checkWin(len) === false) {
        len = checkList.filter(Boolean).length;
        currentPlayer = "ZERO";
        while (len < 9) {
          boxNumForBot = Math.floor(Math.random() * 9);
          if (!checkList[boxNumForBot]) {
            boxClick(allBox[boxNumForBot], "ZERO", boxNumForBot);
            checkWin(len);
            break;
          }
        }
      }
    }
  }

  allBox.forEach((item) => {
    item.addEventListener("click", (e) => handleBoxClick(e));
  });
}

export function rock_paper(tchance, current_marker, current_airport) {
  const dialog = document.getElementById("Game-Dialog");

  const selections = document.createElement("div");
  selections.classList.add("selections");
  dialog.append(selections);

  const button1 = document.createElement("button");
  button1.classList.add("selection");
  button1.setAttribute("data-selection", "rock");
  button1.innerText = "✊";
  selections.append(button1);

  const button2 = document.createElement("button");
  button2.classList.add("selection");
  button2.setAttribute("data-selection", "paper");
  button2.innerText = "✋";
  selections.append(button2);

  const button3 = document.createElement("button");
  button3.classList.add("selection");
  button3.setAttribute("data-selection", "scissors");
  button3.innerText = "✌";
  selections.append(button3);

  const results = document.createElement("div");
  results.classList.add("results");
  dialog.append(results);

  const random_div = document.createElement("div");
  results.append(random_div);

  const span = document.createElement("span");
  span.classList.add("result-score");
  span.setAttribute("data-your-score", "");
  span.innerHTML = 0;
  random_div.append(span);

  const random_div2 = document.createElement("div");
  random_div2.setAttribute("data-final-column", "");
  results.append(random_div2);

  const span2 = document.createElement("span");
  span2.classList.add("result-score");
  span2.setAttribute("data-computer-score", "");
  span2.innerHTML = 0;
  random_div2.append(span2);

  const selectionButtons = document.querySelectorAll("[data-selection]");
  const finalColumn = document.querySelector("[data-final-column]");
  const computerScoreSpan = document.querySelector("[data-computer-score]");
  const yourScoreSpan = document.querySelector("[data-your-score]");
  const SELECTIONS = [
    {
      name: "rock",
      emoji: "✊",
      beats: "scissors",
    },
    {
      name: "paper",
      emoji: "✋",
      beats: "rock",
    },
    {
      name: "scissors",
      emoji: "✌",
      beats: "paper",
    },
  ];

  selectionButtons.forEach((selectionButton) => {
    selectionButton.addEventListener("click", (e) => {
      const selectionName = selectionButton.dataset.selection;
      const selection = SELECTIONS.find(
        (selection) => selection.name === selectionName
      );
      makeSelection(selection);
    });
  });

  function makeSelection(selection) {
    const computerSelection = randomSelection();
    const yourWinner = isWinner(selection, computerSelection);
    const computerWinner = isWinner(computerSelection, selection);
    let player_game_score = yourScoreSpan.innerText
    let computer_game_score = computerScoreSpan.innerText

    if (computer_game_score === "2") {
      console.log("Hävisit pelin minipelin.")
      dialog.innerHTML = "";
      dialog.style.width = "400px";
      dialog.style.height = "200px";

      const h1 = document.createElement("h1");
      h1.innerHTML = "Hävisit minipelin"
      h1.style.textAlign = "center";
      dialog.append(h1);

      const button_div = document.createElement("div");
      button_div.classList.add("Button-div");
      dialog.append(button_div);
    
      const button = document.createElement("button");
      button.setAttribute("id", "close");
      button.innerText = "Sulje minipeli";
      button_div.append(button);



      const closeBtn = document.getElementById("close");

      let game_results = "False";
      tchance = "0";
      treasure(
        "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
      );
      closeBtn.style.display = "block";
      closeBtn.addEventListener("click", () => {
        current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
        dialog.close();
      });
    }
    else if (player_game_score === "2") {
      console.log("Voitit minipelin.")
      dialog.innerHTML = "";
      dialog.style.width = "400px";
      dialog.style.height = "200px";

      const h1 = document.createElement("h1");
      h1.innerHTML = "Voitit minipelin"
      h1.style.textAlign = "center";
      dialog.append(h1);

      const button_div = document.createElement("div");
      button_div.classList.add("Button-div");
      dialog.append(button_div);
    
      const button = document.createElement("button");
      button.setAttribute("id", "close");
      button.innerText = "Sulje minipeli";
      button_div.append(button);
      let game_results = "True";

      const closeBtn = document.getElementById("close");

      treasure(
        "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
      );
      closeBtn.style.display = "block";
      closeBtn.addEventListener("click", () => {
        current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
        dialog.close();
      });
    }
    addSelectionResult(computerSelection, computerWinner);
    addSelectionResult(selection, yourWinner);
    if (yourWinner) incrementScore(yourScoreSpan);
    if (computerWinner) incrementScore(computerScoreSpan);
  }

  function incrementScore(scoreSpan) {
    scoreSpan.innerText = parseInt(scoreSpan.innerText) + 1;
  }

  function addSelectionResult(selection, winner) {
    const div = document.createElement("div");
    div.innerText = selection.emoji;
    div.classList.add("result-selection");
    if (winner) div.classList.add("winner");
    finalColumn.after(div);
  }

  function isWinner(selection, opponentSelection) {
    return selection.beats === opponentSelection.name;
  }

  function randomSelection() {
    const randomIndex = Math.floor(Math.random() * SELECTIONS.length);
    return SELECTIONS[randomIndex];
  }
}

export function guess_number(tchance, current_marker, current_airport) {
  const dialog = document.getElementById("Game-Dialog");

  const wrappaaja = document.createElement("div");
  wrappaaja.classList.add("wrappaaja");
  dialog.append(wrappaaja);


  const wrapper = document.createElement("div");
  wrapper.classList.add("wrapper");
  wrappaaja.append(wrapper);

  const h1 = document.createElement("h1");
  h1.innerText = "Arvaa numero 1 ja 20 välillä";
  wrapper.append(h1);

  const p = document.createElement("p");
  p.classList.add("guess");
  wrapper.append(p);

  const input_field = document.createElement("div");
  input_field.classList.add("input-field");
  wrapper.append(input_field);

  const input2 = document.createElement("input");
  input2.setAttribute("type", "number");
  input_field.append(input2);

  const button = document.createElement("button");
  button.classList.add("number-button");
  button.innerText = "Kokeile";
  input_field.append(button);

  const span = document.createElement("span");
  span.innerText = 5;
  span.classList.add("chances");

  const p2 = document.createElement("p");
  p2.innerText = "Arvauksia jäljellä ";
  p2.append(span)
  wrapper.append(p2);
  const input = document.querySelector("input"),
  guess = document.querySelector(".guess"),
  checkButton = document.querySelector("button"),
  remainChances = document.querySelector(".chances");

// Set the focus on input field
input.focus();

let randomNum = Math.floor(Math.random() * 20);
let chance = 5;

// Listen for the click event on the check button
checkButton.addEventListener("click", () => {
  // Decrement the chance variable on every click
  chance--;
  // Get the value from the input field
  let inputValue = input.value;
  // Check if the input value is equal to the random number
  if (inputValue == randomNum) {
    // Update guessed number, disable input, check button text and color.
    console.log("Voitit minipelin.")
      dialog.innerHTML = "";
      dialog.style.width = "400px";
      dialog.style.height = "200px";

      const h1 = document.createElement("h1");
      h1.innerHTML = "Voitit minipelin"
      h1.style.textAlign = "center";
      dialog.append(h1);

      const button_div = document.createElement("div");
      button_div.classList.add("Button-div");
      dialog.append(button_div);
    
      const button = document.createElement("button");
      button.setAttribute("id", "close");
      button.innerText = "Sulje minipeli";
      button_div.append(button);
      let game_results = "True";

      const closeBtn = document.getElementById("close");

      treasure(
        "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
      );
      closeBtn.style.display = "block";
      closeBtn.addEventListener("click", () => {
        current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
        dialog.close();
      });
    //Check if input value is > random number and within 1-99 range.
  } else if (inputValue > randomNum && inputValue < 100) {
    // Update the guess text and remaining chances
    [guess.textContent, remainChances.textContent] = ["Arvauksesi on liian korkea", chance];
    guess.style.color = "#333";
    //Check if input value is < random number and within 1-99 range.
  } else if (inputValue < randomNum && inputValue > 0) {
    // Update the guessed number text and remaining chances
    [guess.textContent, remainChances.textContent] = ["Arvauksesi on liian matala", chance];
    guess.style.color = "#333";
    // If the input value is not within the range of 1 to 99
  } else {
    // Update the guessed number text, color and remaining chances
    [guess.textContent, remainChances.textContent] = ["Syötä ainoastaan numero", chance];
    guess.style.color = "#DE0611";
  }
  // Check if the chance is zero
  if (chance == 0) {
    //Update check button, disable input, and clear input value.
    // Update guessed number text and color to indicate user loss.
    console.log("Hävisit pelin minipelin.")
    dialog.innerHTML = "";
    dialog.style.width = "400px";
    dialog.style.height = "200px";

    const h1 = document.createElement("h1");
    h1.innerHTML = "Hävisit minipelin"
    h1.style.textAlign = "center";
    dialog.append(h1);

    const button_div = document.createElement("div");
    button_div.classList.add("Button-div");
    dialog.append(button_div);
  
    const button = document.createElement("button");
    button.setAttribute("id", "close");
    button.innerText = "Sulje minipeli";
    button_div.append(button);

    const closeBtn = document.getElementById("close");

    let game_results = "False";
    tchance = "0";
    treasure(
      "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
    );
    closeBtn.style.display = "block";
    closeBtn.addEventListener("click", () => {
      current_marker.bindPopup(`Olet täällä <b>${current_airport}</b>`);
      dialog.close();
    });
  }
  if (chance < 0) {
    window.location.reload();
  }
});
}