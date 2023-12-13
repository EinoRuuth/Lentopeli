# Lentopeli

Kuva pelin Menusta
<img width="920" alt="image" src="https://github.com/EinoRuuth/Lentopeli/assets/121025519/5a1b24d3-62bc-4057-989a-17890a7d8f0e">

Kuva pelistä
<img width="921" alt="image" src="https://github.com/EinoRuuth/Lentopeli/assets/121025519/ddf7080d-1050-4f92-81db-d288eac7ede0">


Tietokannan luomis sql koodit
<p>
--------------------------------------------------------------------
ALTER TABLE game RENAME COLUMN co2_consumed TO fuel_consumed;

ALTER TABLE game RENAME COLUMN co2_budget TO fuel_budget;

ALTER TABLE game ADD COLUMN fuel_left INT(8) AFTER fuel_budget;

ALTER TABLE game ADD COLUMN treasures INT(2) AFTER fuel_left;

ALTER TABLE game DROP COLUMN fuel_consumed;

ALTER TABLE game RENAME players;

CREATE TABLE game (
    airport_name VARCHAR(255),
    treasure_chance int(2),
    has_visited BIT(1)
);

ALTER TABLE game ADD id INT(11) FIRST; 

ALTER TABLE game ADD coordinates varchar(255);

ALTER TABLE game MODIFY COLUMN id INT(11) unsigned PRIMARY KEY AUTO_INCREMENT;

ALTER TABLE game CHANGE id id int(11) NOT NULL:

ALTER TABLE players MODIFY COLUMN location VARCHAR(255);

-------------------------------------------------------------------- </p>
