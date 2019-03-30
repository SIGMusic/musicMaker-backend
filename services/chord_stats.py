class chord_stats:
    def __init__(self, depth, debug = False):
        self.debug = debug
        self.depth = depth
        self.songs = []
        self.chord_data = {}

    def analyse_song(self, song):
        '''
        Analyses the chords of a song and adds that data to the chord data
        params:
            song: a list of chords that appear in a song (in the order they occur)
        returns:
            None
        '''
        self.songs.append(song)
        for d in range(1,self.depth+1):
            self.analyse_song_helper(song, d)

    def analyse_songs(self, songs):
        for i in range(len(songs)):
            songs[i] = [item for sublist in songs[i] for item in sublist]

        for song in songs:
            self.analyse_song(song)

    def analyse_song_helper(self, song, depth):
        '''
        Helper function for analysing songs, which analyses at a the given depth only
        params:
            song: a list of chords that appear in a song (in the order they occur)
            depth: the number of preceding chords to consider
        returns:
            None
        '''
        for i in range(len(song)-depth):
            sample = song[i:i+depth+1]
            samX = tuple(sample[:-1])
            samY = sample[-1]
            if samX not in self.chord_data:
                self.chord_data[samX] = {}
            self.chord_data[samX][samY] = 1+self.chord_data.get(samX, {}).get(samY, 0)

    def increase_depth(self, new_depth):
        '''
        Increases the number of preceding chords that this object analyses and analyses currently
        held songs to that depth
        params:
            new_depths: an integer which is greater than the previous depth representing the
                        maximum number of preceding chords to analyse in this object
        returns:
            None
        '''
        if new_depth > self.depth:
            for i in range(self.depth+1, new_depth+1):
                for song in self.songs:
                    self.analyse_song_helper(song, i)

    def get_next_chord(self, past_chords, depth = None):
        '''
        Gets the probabilities of particular chords following the given set of past chords
        By default, uses as much depth as the object analyses
        params:
            past_chords: a list or numpy array of chords that precede the one being asked about
            depth: if set, forces the search to be for the preceding 'depth' chords only
        returns:
            A dictionary of chords that might follow the past_chords, followed by the fraction
            of the time this has occured in the current data set
        '''
        # Do extra analysis if necessary
        if depth == None:
            depth = self.depth
        if depth > self.depth:
            self.increase_depth(depth)

        # Find the chord data
        retVal = {}
        while len(retVal) == 0 and depth > 0:
            retVal = self.chord_data.get(tuple(past_chords[-depth:]), {})
            if(self.debug):
                print("Depth:", depth, "Key:", tuple(past_chords[-depth:]), "Value:", retVal)
            depth -= 1
        # Divide to get probability
        retVal = retVal.copy()
        instanceCount = sum(retVal.values())
        for key in retVal.keys():
            retVal[key] /= instanceCount
        return retVal


class chord_stats_tester:
    def __init__(self):
        self.testAnalyseSong()
        self.testIncreaseDepth()
    def testAnalyseSong(self):
        print("Testing analyse_song()")
        testStats = chord_stats(3, debug=True)
        a, b, c = "a", "b", "c"
        testSong = [a, a, b, b, c, c]
        testStats.analyse_song(testSong)
        print(testStats.chord_data)
        print(testStats.get_next_chord([a]))
    def testIncreaseDepth(self):
        print("Test Missing: increase_depth()")

#chord_stats_tester()
