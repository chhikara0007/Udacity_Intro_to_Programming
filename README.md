# Udacity_Intro_to_Programming
Tournament Final Project

Project was designed for multiple concurrent tournaments allowed per player.

<b>Primer Functions</b>: 

-Delete matches, players, tournaments and scoreboard functions are the starting point for a clean slate tournament test.


<b>Tournament Functions</b>:

-<i>Create Tournament</i>: This is for the extra credit and allows for players to be participants in multiple tournaments concurrently.

-<i>Count Players</i> and <i>Register Player</i>: Functions that deal with player onboarding and maintenance.

-<i>Players Standings</i>: Function that displays current scoreboard

-<i>Report Match</i>: Function that updates SQL tables on tournament results

-<i>hasBye</i>, <i>checkByes</i> and <i>reportBye</i>: Functions that deal with Byes in a tournament round if there are odd players.  A bye is when a player gets a free pass during a round because they are unable to be matched up with another opponent.

-<i>validPairs</i> and <i>checkDuplicatePairs</i>: Functions that deal with player and opponent matchups.  ValidPair() simply verifies whether the pair has played against each other while checkDuplicatePairs() loops through ValidPairs() to make sure this check has been completed against all possible opponents if the first suggested pair has failed the check.

-<i>SwissPairing</i>: Main Tournament Function
