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
    # Iterate over lines in file
    chord_file = open(filepath)
    song_chord_list = []
    section_chord_list = []
    for line in chord_file:
        section_chord_list_beginning_index = len(section_chord_list)
        # Read meta-data
        if line[0] == "#":
            if line.find("# tonic: ") != -1:
                # cut off '# tonic: ' from beginning and '\n' from end
                tonic = line[9:-1]
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
                    section_label = line[first_comma + 2: second_comma]
            
            # Slowly append each chord and cut it off from remaining_line 
            remaining_line = line[line.find("|") + 1:]
            while remaining_line.find("|") != -1:
                next_bar = remaining_line.find("|")
                # Beat is in between bars ("|"), can contain multiple chords
                measure = remaining_line[:next_bar]

                # Chop up measure by chord, identified by spaces
                measure_chord_list = []
                remaining_measure = measure[measure.find(" ") + 1:]
                while remaining_measure.find(" ") != -1:
                    #print("Remaining Measure: " + remaining_beat)
                    next_space = remaining_measure.find(" ")
                    # Chord is in between spaces, if it contains a colon
                    chord_name = remaining_measure[:next_space]
                    repeat = False
                    if(chord_name.find(".")==-1):
                        if(chord_name.find(":")==-1):
                            remaining_measure = remaining_measure[next_space + 1:]
                            continue
                    else:
                        repeat = True
                    #print("Chord: " + chord_name)
                    if len(measure_chord_list) != 0 and repeat:
                        measure_chord_list[-1].duration += 1
                    else:
                        measure_chord_list.append(Chord(chord_name, 1))
                    remaining_measure = remaining_measure[next_space + 1:]

                # Convert duration measurements into units of measures
                #  First, find total length of chords in measure_chord_list
                chord_duration_sum = 0
                for chord in measure_chord_list:
                    chord_duration_sum += chord.duration
                # Next divide by that sum
                for chord in measure_chord_list:
                    chord.duration/=chord_duration_sum

                # Check for repeats between measures
                if len(section_chord_list) != 0 and len(measure_chord_list) != 0 and section_chord_list[-1].chord == measure_chord_list[0].chord:
                    section_chord_list[-1].duration += measure_chord_list[0].duration
                    measure_chord_list.pop(0)

                # Concatenate the measure's chords to section_chord_list
                section_chord_list += measure_chord_list
                remaining_line = remaining_line[next_bar + 1:]

            # account for "xN" multipliers
            multiplier_index = remaining_line.find("x")
            if multiplier_index == 1:
                next_space = remaining_line[multiplier_index:].find(" ")
                multiplier = int(remaining_line[multiplier_index + 1:next_space])

                # Iterate through chords from this line
                for chord in section_chord_list[section_chord_list_beginning_index:]:
                    chord.duration *= multiplier

            
    return tonic, song_chord_list

# Call getChordList for each file inside parent folder and organize based on tonic
# return dictionary (key, value) = (tonic, a list of arrays where each array is the chord list of a song)
def get_all_data (parent_folder):
    # Create dictionary to store chordLists by tonic
    data = dict()
    # Call getChordList on every file in the dataset
    for folder in os.listdir(parent_folder):
        tonic, chordList = get_chord_list(parent_folder + "/" + folder + "/salami_chords.txt")
        # Add each song's chordList to the dictionary by tonic
        if tonic in data:
            data[tonic].append(chordList)
        else:
            data[tonic] = [chordList]
    return data

# Test
#print(get_chord_list("McGill-Billboard/0089/salami_chords.txt"))
print(get_all_data("McGill-Billboard"))