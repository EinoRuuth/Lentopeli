export function tic_tac_toe() {
    const dialog = document.getElementById("Game-Dialog");

    const h2 = document.getElementById("Game-Dialog");
    h2.innerHTML = "❌⭕ Ristinolla"
    const game_div = document.createElement('div');
    game_div.classList.add('tic_tac_toe');
    dialog.append(game_div);
    let i = 0
    while (i < 9) {
        const grid_div = document.createElement('div');
        grid_div.classList.add('grid-cell');
        grid_div.setAttribute('data-value', i)
        game_div.append(grid_div);
        i++;
    }

    const game_over = document.createElement('div');
    game_over.classList.add('game-over');
    dialog.append(game_over);

    const span = document.createElement('span');
    span.classList.add('game-over-text');
    game_over.append(span);
}