-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DELETE DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

USE tournament;

CREATE TABLE players(id SERIAL,
					name TEXT,
					PRIMARY KEY (ID)
);

CREATE TABLE tournaments(tournament_id SERIAL,
						tourney_name TEXT,
						PRIMARY KEY (ID)
);
						   
CREATE TABLE matches(matchid SERIAL,
					tournament_id INTEGER,
					winner INTEGER,
					loser INTEGER,
					draw BOOLEAN,
					PRIMARY KEY (ID),
					FOREIGN KEY (tournament_id)
);

CREATE TABLE scoreboard (tournament_id INTEGER,
						player INTEGER,
						score INTEGER,
						matches INTEGER,
						bye INTEGER
						FOREIGN KEY (tournament_id)
);