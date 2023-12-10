export function tic_tac_toe() {
    const dialog = document.getElementById("Game-Dialog");

    const button = document.createElement('button');
    button.setAttribute('id', 'close')
    button.innerText = "Sulje minipeli";
    dialog.append(button);

    const container_div = document.createElement('div');
    container_div.classList.add('container');
    dialog.append(container_div);

    const h1 = document.createElement('h1');
    container_div.append(h1);

    const state = document.createElement('div');
    state.classList.add('state');
    container_div.append(state);

    const p = document.createElement('p');
    p.setAttribute('id', 'result')
    container_div.append(p);

    const game_container = document.createElement('div');
    game_container.classList.add('game-container');
    container_div.append(game_container);

    const wrap = document.createElement('div');
    wrap.classList.add('wrap');
    game_container.append(wrap);


    let i = 0
    while (i < 9) {
        const section = document.createElement('section');
        section.classList.add('box');
        section.setAttribute('data-box-num', i)
        wrap.append(section);
        i++;
    }
}
