import numpy as np

class chord_stats:
    def __init__(self, depth):
        self.depth = depth
        self.songs = []
        self.chord_data = {}

    # Analyses a song and adds it to the chord data
    # song: a list of chords in a song (in order of occurance)
    def analyse_song(self, song):
        self.songs.append(song)
        for d in range(1,self.depth+1):
            analyse_song_helper(self, song, d)

    def analyse_song_helper(self, song, depth):
        #Do something
        for i in range(len(song)-depth):
            sample = song[i:i+depth+1]
            samX = tup(sample[:-1])
            samY = sample[-1]
            self.chord_data[samX][samY] = 1+self.chord_data.get(samX, {}).get(samY, 0)

    def increase_depth(new_depth):
        if new_depth > depth:
            for i in range(depth+1, new_depth+1):
                for song in self.songs:
                    analyse_song_helper(self, song, i)

    def get_next_chord(self, past_chords, depth = None):
        if depth == None:
            depth = self.depth
        if depth > self.depth:
            raise Exception("No data for depth "+str(depth))
        return self.chord_data[tuple(past_chords[:-depth])]

class chord_stats_tester:
    def __init__(self):
        self.testAnalyseSong()
        self.testIncreaseDepth()
    def testAnalyseSong():
        print("Test Missing")
    def testIncreaseDepth():
        print("Test Missing")
