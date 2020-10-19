# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:40:51 2020

@author: Antiochian

1408484768 lines in main file (140GB, yikes!)

Flow:
    
    Step thru file line by line
    Check if first move of new game (if starts with "1. ")
    
    Compare current eval to previous eval for both sides for all moves
    log eval change, if eval change exceeds a cutoff (-2?) then mark as a blunder
    and note down time at which move occurred
    
    Graph data
    
Data structure:
    Each game should yield two 2XN arrays
    [time, evalchange] - white
    [time, evalchange] - black
    
Intermediate datafiles are exported and saved with the following filename structure:

 "data/1603074502 time180-180_rating2000-4000_raw.txt"
      timestamp     gametime    rating        filetype
      
Each run produces 4 similarly named files:
    ..._raw.txt - all raw blunder times as newline-delineated list
    ..._norm.txt - frequency dict of all move times (needed to normalize data) serialised as dictionary
    ..._info.txt - misc info about when the file was generated, how long it took, etc etc
    ..._graph.png - graph of data
    
Later new graphs/analysis can be built directly from these files without having to endure
the tedius process of stepping through the 140GB raw game datafile again.
"""

import matplotlib.pyplot as plt
import time


def time_to_int(timestring):
    #takes in timestamp of format "00:00:00" etc and converts to seconds int
    timeint = 0 #number of seconds
    t = timestring.split(":")
    t.reverse()
    mult = 1
    for i in t:
        timeint += mult*int(i)
        mult *= 60
    return timeint

def strip_game(line, time_cutoff_min,time_cutoff_max):
    """
    This function removes all metadata and move information from game, leaving only something that looks like:
        [[eval, time], [eval, time], [eval,time],...]
    """  
    if time_cutoff_max == None:
        time_cutoff_max = float("Inf")
    game = line.split("}")[:-1] #gets
    stripped = []
    if game and ("%eval" in game[0]) and ("%clk" in game[0]):
        #valid game
        for line in game:
            res = []
            curr = ""
            read = False
            for char in line:
                if char == "[":
                    read = True
                elif char == "]":
                    res.append(curr.split()[1])
                    curr = ""
                    read = False
                elif read:
                    curr += char
            if len(res) == 2:
                stripped.append(res)
        #final check in case of checkmate (no eval is given)
    if stripped:
        if (time_to_int(stripped[0][1]) >= time_cutoff_min) and (time_to_int(stripped[0][1]) <= time_cutoff_max):
            return stripped
    else:
        return False
            

def extract_blunders(stripped,normalization, cutoff = -2, extremis = 100):
    #cutoff = change in eval to count as a blunder
    #extremis: point at which blunders are no longer recognised
    curr_eval = 0.0
    white = True
    blunder_times = []
    all_times = []
    for move in stripped:
        move[1] = time_to_int(move[1])
        all_times.append(move[1])
        prev_eval = curr_eval
        if move[0][0] == "#":
            if move[0][1] == "-":
                curr_eval = -extremis
            else: 
                curr_eval = extremis
        else:
            curr_eval = float(move[0])
        if white:
            white = False
            eval_change = curr_eval - prev_eval
            if eval_change < cutoff and curr_eval < extremis:
                blunder_times.append(move[1])
        else:
            white = True
            eval_change = prev_eval - curr_eval
            if eval_change < cutoff and curr_eval > -extremis:
                blunder_times.append(move[1])
    for t in all_times:
        if t in normalization:
            normalization[t] += 1
        else:
            normalization[t] = 1
    return blunder_times, normalization

    
def preprocess_PGN(inp, maxlim, blunder_cutoff, min_elo, max_elo, min_time,max_time):    
    print("Starting...")
    id_string = "time"+str(min_time)+"-"+str(max_time)+"_rating"+str(min_elo)+"-"+str(max_elo)
    if not maxlim:
        maxlim = float("Inf")
    start = int(time.time())
    linecount = 0
    validcount = 0
    curr_elo = -1
    normalization = {}
    finished = False
    out = "data/"+str(start)+" "+id_string+"_raw.txt"
    normout = "data/"+str(start)+" "+id_string+"_norm.txt"
    infoout = "data/"+str(start)+" "+id_string+"_info.txt"
    with open(inp,"r") as infile:
        with open(out,"w") as outfile:
            for line in infile:
                if linecount > maxlim:
                    break
                    #return normalization
                if line[:9] == "[WhiteElo":
                    curr_elo = int(line.split()[1][1:-2])
                if (curr_elo < max_elo) and (curr_elo >= min_elo) and (line[:3] == "1. "):
                    #reset for new game!
                    stripped = strip_game(line,min_time,max_time)
                    if stripped:
                        validcount +=1
                        blunder_times, normalization = extract_blunders(stripped,normalization)
                        for t in blunder_times:
                            outfile.write(str(t)+"\n")
                linecount += 1
    time_taken = time.time() - start
    print("Finished creating",out," after ",linecount," lines processed. (", validcount," matching games found)")
    print(round(time_taken,3), " seconds taken.")
    with open(normout,"w") as outfile:
        print(normalization, file=outfile)
    with open(infoout,"w") as outfile:
        print("Created",out,"\n",linecount," lines processed. (", validcount," matching games found)",file=outfile)
        print(str(time_taken)+" seconds taken.", file=outfile)
        print("\nParameters used:", file=outfile)
        print("\n Blunder cutoff: ", blunder_cutoff,"\nMin Elo: ", min_elo, "\nMax Elo: ",max_elo, "\nMin time:", min_time, "\nMax time:", max_time, file=outfile)
    return normalization, out
                 
    
def get_raw(blunderfile="blunders.txt"):
    raw = {}
    with open(blunderfile) as infile:
        for line in infile:
            key = line.replace("\n","")
            if int(key) in raw:
                raw[int(key)] += 1
            else:
                raw[int(key)] = 1
        return raw

def plot_histogram(raw, norm_data, max_time):
    xdata, ydata = [],[]
    for key in raw:
        normed = raw[key]/norm_data[key]
        xdata.append(key)
        ydata.append(normed)
        
    plt.scatter(xdata,ydata, marker="|", s=1)
    plt.xlim(0,max_time)
    plt.ylim(0,0.45)
    plt.xlabel("Time remaining (s)")
    plt.ylabel("Probability of blunder")
    plt.title("Blunder % chance with remaining time")
    return xdata, ydata

def plot_existing_data(identifier=None, max_time=300):
    if not identifier:
        identifier = input("Timestamp & params: ")
    rawfile = "data/"+identifier+"_raw.txt"
    normfile = "data/"+identifier+"_norm.txt"
    print("Extracting raw data...")
    raw = get_raw(rawfile)
    print("Extracting normalization dict...")
    with open(normfile, 'r') as infile: 
        content = infile.read(); 
        norm = eval(content);
    print("Plotting...")
    xdata, ydata = plot_histogram(raw,norm,max_time)
    plt.title(identifier)
    print("Done!")
    return


def driver(maxlim=2**20,  min_elo=0, max_elo=5000,min_time=300, max_time=300, savefig = False):
    blunder_cutoff = -2
    norm, outfile = preprocess_PGN("lichess_db_standard_rated_2020-06.pgn/2020-06.pgn",maxlim,blunder_cutoff, min_elo, max_elo, min_time, max_time)
    print("Data processed.")
    total = 0
    for k in norm:
        total += norm[k]
    print("Total blunders: ",total)
    # plot_histogram_from_blunderfile()
    print("Extracting and plotting data...")
    raw = get_raw(outfile)
    xdata, ydata = plot_histogram(raw,norm, max_time)
    if savefig:
        print("Saving figure...")
        plt.title(str(int(max_time/60))+"min games, ELO: "+str(min_elo)+"-"+str(max_elo))
        plt.savefig(outfile[:-7]+"graph.png", dpi=300)
        plt.clf()
    print("Done!\n")

def overnight_test(ncount = 2**24):
    t0 = time.time()
    print("THREE MINUTES:")
    driver(maxlim=ncount, min_time=180, max_time=180, min_elo=0000, max_elo=1000, savefig = True)
    driver(maxlim=ncount, min_time=180, max_time=180, min_elo=1000, max_elo=2000, savefig = True)
    driver(maxlim=ncount, min_time=180, max_time=180, min_elo=2000, max_elo=4000, savefig = True)
    
    print("FIVE MINUTES:")
    driver(maxlim=ncount, min_time=300, max_time=300, min_elo=0000, max_elo=1000, savefig = True)
    driver(maxlim=ncount, min_time=300, max_time=300, min_elo=1000, max_elo=2000, savefig = True)
    driver(maxlim=ncount, min_time=300, max_time=300, min_elo=2000, max_elo=4000, savefig = True)
    
    print("TEN MINUTES:")
    driver(maxlim=ncount, min_time=600, max_time=600, min_elo=0000, max_elo=1000, savefig = True)
    driver(maxlim=ncount, min_time=600, max_time=600, min_elo=1000, max_elo=2000, savefig = True)
    driver(maxlim=ncount, min_time=600, max_time=600, min_elo=2000, max_elo=4000, savefig = True)
    print("Final runtime: ", round( (time.time()-t0 )/ 60,3),"min")


def comparison_plot():
    #debug code to plot mutliple data series on same graph
    filename1 = "night of 18th/1603071379 time180-180_rating0-1000"
    filename2 = "night of 18th/1603072522 time180-180_rating1000-2000"
    filename3 = "night of 18th/1603074502 time180-180_rating2000-4000"
    plot_existing_data(filename1,180)
    plot_existing_data(filename2,180)
    plot_existing_data(filename3,180)
    plt.title("different ELO band chess blunder % in 3min games")
    plt.legend(["0-1000 ELO", "1000-2000 ELO", "2000-4000 ELO"], markerscale = 4)
    print("Saving figure...")
    plt.savefig(str(time.time())+"_comparison.png", dpi=300)
