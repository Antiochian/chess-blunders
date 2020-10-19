# chess-blunders
Examining blunder rates in 68 million games of online chess

What is it?
----
This is a series of graphs that illustrate the incidence of blunders (major unforced errors) in games of online chess for different ELO ratings and time controls.
The y axis is the normalised blunder chance - the total number of blunders over the total number of all moves, and the x-axis is the time remaining (in seconds)

Results
---
(Still need to add some more results for 5min and 10min time controls, and more precise documentation and graph-labelling)
![3min result](3min_game_comparison.png)

|Legend | Matching games analysed (3min)| Matching games analysed (5min)| Matching games analysed (10min)|
|:---:|:---:|:---:|:---:|
|<1k ELO|21,762| tbc | tbc |
|1-2k ELO |704,164| tbc | tbc |
|>2k ELO |230,211| tbc | tbc |

Some interesting things to discuss here:
 - There is a noticeable "bump" at the 20s mark for 3min games and the 40s mark for 5min games - this is the exact same time the lichess website plays a loud alarm beeping sound and flashes the clock red to warn you you are low on time. I hypothesise this interuption can panic players and cause them to play knee-jerk, illconsidered moves, resulting in a bump in the blunder rates (since I know that I do the same!).
 - As expected, generally speaking, the blunder rate increases with time, with very few players blundering in the opening stages and most blunders occuring in the last few seconds of a game as the time situation becomes desperate.
 - It is interesting to note the blunder rate plateaus for <1k and 1-2k elo players, but in fact does not plateau for expert players (>2k elo, top 10% of userbase). My hypothesis for this is that beginner players generally gain little advantage from extra time - if they havent found the best move in 20 seconds, they probably wont find it in 20 minutes either. However, expert players probably could play an (almost) blunder-free game if they spent an hour carefully considering any move - they are the only demographic which is actually suffering from time pressure throughout the entire match, not just in the final stages. An alternate hypothesis could be that expert players ration their time more ruthlessly and strategically.
 - There is a strange dip in blunder rates at the "50% of time remaining mark" for all ELOs. I do not know from whence this came, and determining (a) whether its some program error or (b) some natural phenomena is currently my main priority.
 
How does it work?
----

I downloaded 68 million games of online chess from the lichess database: [https://database.lichess.org/](https://database.lichess.org/)
I wrote a program to go through these games and filter them for various parameters (ELO, time controls, etc) and also only select those games with clock and eval data (about 25% of them). From these I analysed the change in eval with every move, and the time at which that move was taken.

I defined a blunder the same way the lichess.org website does - a blunder is a move that results in a 200 [centipawn eval loss](https://en.wikipedia.org/wiki/Chess_piece_relative_value) according to the computer. There is a slight complication, which is that if you were already winning the game before your blunder, and you are still winning the game after your blunder, then the blunder doesnt count. This is the same method lichess uses.

The main interesting challenge here was handling such enormous volumes of data. A naive readlines() approach to reading in the raw data would require 140GB of text to be stored in memory - not exactly feasible! So instead I wrote a preprocessing step whereby all unnessary information is stripped out (metadata, actual moves, etc), reducing the initial 140GB datafile by a proportion of about 0.0000093, resulting in much more manageable 1.3KB datafiles that could be used. Another advantage of this is speed - it takes 40 minutes just to read every line of the initial file, so by preprocessing it into a new file, I only ever have to do that costly initial read step once, and in future can plot/analyse data instead from the 1.3KB reduced file.

Matplotlib is used for plotting.
