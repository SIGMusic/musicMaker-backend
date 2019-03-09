import numpy as np

class chord_stats():
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
        pass

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
