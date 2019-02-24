import numpy as np
#import pandas as pd
import re
import os

# Create Chord class
class Chord:
    def __init__(self, chord, duration):
        self.chord = chord
        self.duration = duration
    def __repr__(self):
        return self.chord + " x" + str(self.duration)

# Fill in list of chord names/durations for each musical section
#  return (tonic, chordlist)
def get_chord_list (filepath):
    # Sample return so that getAllData runs correctly
    #return 'A:min', ['A:min', 'D:maj', 'A:min']
    
    # Iterate over lines in file
    chord_file = open(filepath)
    song_chord_list = []
    section_chord_list = []
    for line in chord_file:
        # Read meta-data
        if line[0] == "#":
            if line.find("# tonic: ") != -1:
                tonic = line[9:]
        else:
            # Read chord data
            first_comma = line.find(',')
            if first_comma != -1: # line has organizational data
                # Musical section is over, create new chordList for new section
                if(len(section_chord_list) != 0):
                    song_chord_list.append(section_chord_list)
                section_chord_list = []

                # Store the section label -- not used now, but stored in case we want it
                second_comma = line.find(',', first_comma)
                if second_comma != -1:
                    label = line[first_comma + 2: second_comma]
            
            # Slowly append each chord and cut it off from remaining_line 
            remaining_line = line[line.find("|") + 1:]
            while remaining_line.find("|") != -1:
                next_bar = remaining_line.find("|")
                # Chord is in between bars ("|") and spaces
                chord_name = remaining_line[1:next_bar - 1]
                if len(section_chord_list) != 0 and section_chord_list[-1].chord == chord_name:
                    section_chord_list[-1].duration += 1
                else:
                    section_chord_list.append(Chord(chord_name, 1))
                remaining_line = remaining_line[next_bar + 1:]
    
    return tonic, song_chord_list

# Call getChordList for each file inside parent folder and organize based on tonic
# return dictionary (key, value) = (tonic, a list of arrays where each array is the chord list of a song)
def get_all_data (parent_folder):
    # Create dictionary to store chordLists by tonic
    data = dict()
    # Call getChordList on every file in the dataset
    for folder in os.listdir(parent_folder):
        tonic, chordList = get_chord_list(parent_folder + "/" + folder + "/salami-chords.txt")
        # Add each song's chordList to the dictionary by tonic
        if tonic in data:
            data[tonic].append(chordList)
        else:
            data[tonic] = [chordList]
    return data