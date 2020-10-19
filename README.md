# chess-blunders
Examining blunder rates in 68 million games of online chess

What is it?
----
This is a series of graphs that illustrate the incidence of blunders (major unforced errors) in games of online chess for different ELO ratings and time controls.
A blunder is defined as it is on lichess - a move resulting 200 centipawn eval loss (more on that later).

The y axis is the normalised blunder chance - the total number of blunders over the total number of all moves, and the x-axis is the time remaining (in seconds)

Results
---
(Still need to add some more results for 5min and 10min time controls)
![3min result]('3min_game_comparison.png')

Some interesting things to discuss here:
 - There is a noticeable "bump" at the 20s mark for 3min games and the 40s mark for 5min games - this is the exact same time the lichess website plays a loud alarm beeping sound and flashes the clock read to warn you you are low on time. I hypothesise this interupption can panic players and cause them to play knee-jerk, illconsidered moves, resulting in a bump in the blunder rates.
 - As expected, generally speaking, the blunder rate increases with time, with very few players blundering in the opening stages and the most blunders occuring in the last few seconds of a game as the time situation becomes desperate.
 - It is interesting to note the blunder rate plateaus for <1k and 1-2k elo players, but in fact does not plateau for expert players (>2k elo, top 10% of userbase). My hypothesis for this is that beginner players generally gain little advantage from extra time - if they havent found the best move in 20 seconds, they probably wont find it in 20 minutes either. However, expert players probably could play an (almost) blunder-free game if they spent an hour carefully considering any move - they are the only demographic which is actually suffering from time pressure throughout the entire match, not just in the final stages. An alternate hypothesis could be that expert players ration there time more ruthlessly and strategically.
 - There is a strange dip in blunder rates at the "50% of time remaining mark" for all ELOs. I do not know from whence this came, and determining (a) whether its some program error or (b) some natural phenomena is currently my main priority.
 
How does it work?
----
