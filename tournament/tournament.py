#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    #Connect to the PostgreSQL database.  Returns a database connection.
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    #Remove all the match records from the database.
	DB=connect()
	c=DB.cursor()
	c.execute("DELETE FROM matches")
	DB.commit()
	DB.close()
	
def deletePlayers():
    #Remove all the player records from the database.
	DB=connect()
	c=DB.cursor()
	c.execute("DELETE FROM players")
	DB.commit()
	DB.close()

def deleteTournaments():
	#Remove all the tournament records from the database.
	DB=connect()
	c=DB.cursor()
	c.execute("DELETE FROM tournaments")
	DB.commit()
	DB.close()
	
def deleteScoreboard():
	#Remove all the scoreboard records from the database.
	DB=connect()
	c=DB.cursor()
	c.execute("DELETE FROM scoreboard")
	DB.commit()
	DB.close()
	
'''def select_tournament_name():
    #Create tournament name.
	print "\n Choose a tournament name:"
	tourney_name = raw_input().lower()  
	return tourney_name'''
	 
def createTournament(tourney_name):
	"""Create a new tournament.  
	
	Arguments: 
		tourney_name = Name of Tournament"""
	DB=connect()
	c=DB.cursor()
	sql="INSERT INTO tournaments (tourney_name) Values (%s) RETURNING id"
	c.execute(sql, (tourney_name,))
	tournament_id=c.fetchall()[0]
	DB.commit()
	DB.close()
	return tournament_id

def countPlayers(tournament_id):
	"""Returns the number of players currently registered.
	
	Arguments: 
		tournament_id = ID of tournament"""
	DB = connect()
	c = DB.cursor()
	sql = """SELECT count(player) AS num
			FROM scoreboard
			WHERE tournament = %s"""
	c.execute(sql,(tournament_id,))
	player = c.fetchone()[0]
	DB.close()
	return player
	
def registerPlayer(name, tournament_id):
	"""Adds a player to the tournament database.
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
	
	Arguments:
		name = the player's full name (need not be unique)."""
	DB = connect()
	c = DB.cursor()
	player = "INSERT INTO players (name) VALUES (%s) RETURNING id"
	scoreboard = """INSERT INTO scoreboard (tournament, player, score, matches, bye)
					VALUES (%s, %s, %s, %s, %s)"""
	param = (name,)
	c.execute(player, param)
	playerid = c.fetchone()[0]
	c.execute(scoreboard, (tournament_id, playerid,0,0,0))
	DB.commit()
	DB.close()
	return playerID
	
def playerStandings(tournament_id):
	"""Returns a list of the players and their win records, sorted by wins.
	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
		A list of tuples, each of which contains (ID, name, wins, matches):
		id: the player's unique ID (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played"""
	DB = connect()
	c = DB.cursor()
	players = """SELECT s.player, p.name, s.score, s.matches, s.bye,
				(SELECT SUM(s2.score)
				FROM scoreboard AS s2
				WHERE s2.player IN (SELECT loser
									FROM matches
									WHERE winner = s.player
									AND tournament = %s)
				OR s2.player IN (SELECT winner
								FROM matches
								WHERE loser = s.player
								AND tournament = %s)) as opponent_strength
				FROM scoreboard AS s
				INNER JOIN players AS p on p.id = s.player
				WHERE tournament = %s
				ORDER BY s.score DESC, opponent_strength DESC, s.matches DESC"""	
	c.execute(players, (tournament_id, tournament_id, tournament_id))
	ranks = []
	for row in c.fetchall():
		ranks.append(row)
	DB.close()
	return ranks

def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.
	
	Arguments:
		winner:  the ID number of the player who won
		loser:  the ID number of the player who lost"""
	if draw == 'TRUE':
		win_points = 1
		loss_points = 1
	else:
		win_points = 3
		loss_points = 0

	DB = connect()
	c = DB.cursor()
	ins = "INSERT INTO matches (tournament, winner, loser, draw) VALUES (%s,%s,%s,%s)"
	win = "UPDATE scoreboard SET score = score+%s, matches = matches+1 WHERE player = %s AND tournament = %s"
	los = "UPDATE scoreboard SET score = score+%s, matches = matches+1 WHERE player = %s AND tournament = %s"
	c.execute(ins, (tournament_id, winner, loser, draw))
	c.execute(win,(win_points, winner, tournament_id))
	c.execute(los, (loss_points, loser, tournament_id))
	DB.commit()
	DB.close()

def hasBye(id, tournament_id):
	"""Checks if player has bye.

	Arguments:
		id = ID of player to check.  Verification returned in boolean form."""
	sql = """SELECT bye
			FROM scoreboard
			WHERE player = %s2
			AND tournament = %s"""
	c.execute(sql, (id, tournament_id))
	bye = c.fetchone()[0]
	DB.close()
	if bye == 0:
		return True
	else:
		return False

def reportBye(player, tournament_id):
	"""Assign points if player has a bye.

	Arguments:
		player = ID of player receiving a bye round.
		tournament_id = ID of the tournament."""
	DB.connect()
	c.DB.cursor()
	bye = "UPDATE scoreboard SET score = score+3, bye = bye+1, WHERE player = %s AND tournament = %s"
	c.execute(bye, (player, tournament_id))
	DB.commit()
	DB.close()	

def checkByes(tournament_id, ranks, index):
	"""Checks if players already have a bye round.

	Arguments:
		tournament_id = ID of the tournament
		ranks = list of current ranks from swissPairings function
		index = index to check
	Returns first ID that is valid or original ID if none are found."""
	if abs(index) > len(ranks):
		return -1
	elif not hasBye(ranks[index][0], tournament_id):
		return index
	else:
		return checkByes(tournament_id,ranks, (index - 1))

def ValidPairs(player1, player2, tournament_id):
	"""Checks if a pair has already played against each other.  

	Arguments:
		player1: the ID # of the first player
		player2: the ID # of the possible opponent
		tournament_id: ID of the tournament
	Verification of valid pair is in Boolean form."""
	DB = connect()
	c = DB.cursor()
	sql = """SELECT winner, loser
			FROM matches
			WHERE ((winner = %s AND loser = %s)
					OR (winner = %s AND loser = %s))
			AND tournament = %s"""
	c.execute(sql, (player1, player2, player2, player1, tournament_id))
	matches = c.rowcount
	DB.close()
	if matches > 0:
		return False
	return True

def checkDuplicatePairs(tournament_id, ranks, id1, id2):
	"""Checks if a pair already played against each other.  If they have,
	loop through possible competitors list until valid opponent is found.

	Arguments:
		tournament_id = ID of tournament
		ranks: list of current ranks from SwissPairing function (below)
		id1: the ID # of the first player; one who needs to be matched
		id2: the ID # of the possible opponent
	Returns final pair, either new match or original match"""
	if id2 >= len(ranks):
		return id1 + 1 
	elif validPair(ranks[id1][0],ranks[id2][0],tournament_id):
		return id2
	else:
		return checkDuplicatePairs(tournament_id, ranks, id1, id2 + 1)

def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.

	Arguments:
		tournament_id = ID of the tournament
	
	Returns:
		A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name"""
	ranks = playerStandings(tournament_id)
	pairs = []

	number_of_Players = countPlayers(tournament_id)
	if number_of_Players % 2 !=0:
		bye = ranks.pop(checkByes(tournament_id, ranks, -1))
		reportBye(tournament_id, bye[0])

	while len(ranks) > 1:
		validMatch = checkPairs(tournament_id, ranks, 0, 1)
		player1 = ranks.pop(0)
		player2 = ranks.pop(validMatch - 1)
		pairs.append((player1[0],player1[1],player2[0],player2[1]))

	return pairs


#def start_tournament():
#	tourney_name = select_tournament_name()
	
#start_tournament()