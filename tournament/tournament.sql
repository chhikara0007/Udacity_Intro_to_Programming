-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP TABLE IF EXISTS players;
CREATE TABLE players ( id SERIAL,
                       name TEXT );

DROP TABLE IF EXISTS tournaments;
CREATE TABLE tournaments ( tournament_id SERIAL,
                           tourney_name TEXT );

DROP TABLE IF EXISTS matches;
CREATE TABLE matches ( matchid SERIAL,
                       tournament INTEGER,
                       winner INTEGER,
                       loser INTEGER,
                       draw BOOLEAN );

DROP TABLE IF EXISTS scoreboard;					   
CREATE TABLE scoreboard ( tournament INTEGER,
                          player INTEGER,
                          score INTEGER,
                          matches INTEGER,
                          bye INTEGER );