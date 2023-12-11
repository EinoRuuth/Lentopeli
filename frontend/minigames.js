import { treasure } from "./main.js";

const grayIcon = L.divIcon({
  className: ["gray_icon"],
  iconSize: [15, 15],
  iconAnchor: [7, 37],
  popupAnchor: [1, -34],
});

export function tic_tac_toe(tchance, current_marker) {
  const dialog = document.getElementById("Game-Dialog");

  const button = document.createElement("button");
  button.setAttribute("id", "close");
  button.innerText = "Sulje minipeli";
  dialog.append(button);

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
          resultContainer.innerText = "X Won the Match.";
          let game_results = "True";
          treasure(
            "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
          );
          current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
          current_marker.setIcon(grayIcon);
          closeBtn.style.display = "flex";
          closeBtn.addEventListener("click", () => {
            dialog.close();
          });
        } else {
          resultContainer.innerText = "O Won the Match.";
          let game_results = "False";
          tchance = "0";
          treasure(
            "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
          );
          current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
          current_marker.setIcon(grayIcon);

          closeBtn.style.display = "flex";
          closeBtn.addEventListener("click", () => {
            dialog.close();
          });
        }
      } else if (len == 8) {
        winStatus = true;
        resultContainer.innerText = "= Match Draw.";
        let game_results = "False";
        tchance = "0";
        treasure(
          "http://127.0.0.1:3000/drawtreasure/" + game_results + "/" + tchance
        );
        current_marker.bindPopup(`Olet käynyt tällä lentokentällä`);
        current_marker.setIcon(grayIcon);

        closeBtn.style.display = "flex";
        closeBtn.addEventListener("click", () => {
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
