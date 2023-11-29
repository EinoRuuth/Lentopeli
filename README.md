# Lentopeli

Sql koodit
--------------------------------------------------------------------
ALTER TABLE game RENAME COLUMN co2_consumed TO fuel_consumed;

ALTER TABLE game RENAME COLUMN co2_budget TO fuel_budget;

ALTER TABLE game ADD COLUMN fuel_left INT(8) AFTER fuel_budget;

ALTER TABLE game ADD COLUMN treasures VARCHAR(255) AFTER fuel_left;

ALTER TABLE game DROP COLUMN fuel_consumed;

ALTER TABLE game RENAME players;

CREATE TABLE game (
    airport_name VARCHAR(255),
    treasure_chance VARCHAR(255),
    has_visited BIT(1)
);

ALTER TABLE game ADD id INT(11) FIRST; 

ALTER TABLE game MODIFY COLUMN id INT(11) unsigned PRIMARY KEY AUTO_INCREMENT;

ALTER TABLE game CHANGE id id int(11) NOT NULL:

ALTER TABLE players MODIFY COLUMN location VARCHAR(255);

--------------------------------------------------------------------