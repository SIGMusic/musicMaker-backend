import os
import pychord

# Create McGillChord class
class McGillChord:
    def __init__(self, chord, duration = 1, key_irrespective = False):
        self.chord = chord
        self.duration = duration
        self.key_irrespective = key_irrespective
    def __repr__(self):
        return self.chord + " x" + str(self.duration)
    def toPychord(self):
        chord_root = self.chord[:self.chord.find(":")]
        find_bass = self.chord.find("/")
        if find_bass == -1:
            chord_quality = self.chord[self.chord.find(":") + 1:]
            chord_bass = ''
        else:
            chord_quality = self.chord[self.chord.find(":") + 1:self.chord.find("/")]
            chord_bass = self.chord[self.chord.find("/") + 1:]

        # Create notes list to reference later. Only sharps are used. Any flats can look to one index before their base.
        notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        # Record intervals for a generic scale (2 = whole step, 1 = half step)
        intervals = [2, 2, 1, 2, 2, 2, 1]

        # If key_irrespective, convert to key of C
        if self.key_irrespective:
            # Check for 'x:__' chords and return None
            if chord_root == 'x':
                return None

            # Check for 'b' in chord_root
            offset = 0
            if chord_root.find('b') != -1:
                offset = -1
                chord_root = chord_root[0]
            
            chord_root = int(chord_root) - 1 # index from 0 instead of 1
            chord_index = 3 # Begin at C
            for i in range(chord_root):
                chord_index += intervals[i]
            chord_index += offset
            chord_index %= len(notes)
            
            chord_root = notes[chord_index]
            
        # Definining quality conversions based on http://ismir2005.ismir.net/proceedings/1080.pdf
        #  and https://github.com/yuma-m/pychord/blob/master/pychord/constants/qualities.py
        #  reveals that 'maj' => 'M' if not alone and 'min' => 'm' if not alone are the only
        #  required conversions
        new_quality = chord_quality
        if chord_quality.find('maj') != -1 and chord_quality != 'maj':
            new_quality = new_quality.replace('maj', 'M')
        if chord_quality.find('min') != -1 and chord_quality != 'min':
            new_quality = new_quality.replace('min', 'm')

        # Create pychord.Chord with converted values (excluding bass)
        result_chord = pychord.Chord(chord_root + new_quality)
        
        # If no bass or unreadable bass, return un-inverted chord
        try:
            int(chord_bass)
        except:
            return result_chord

        # Configure bass
        chord_notes = list(result_chord.components)
        result_chord = pychord.Chord(chord_root + new_quality + "/" + chord_notes[int(chord_bass) - 1])
        
        return result_chord

# Fill in list of chord names/durations for each musical section
#  return (tonic, chordlist)
def get_chord_list (filepath, pychord_chord = False):    
    # Iterate over lines in file
    chord_file = open(filepath)
    tonic = []
    song_chord_list = []
    section_chord_list = []
    for line in chord_file:
        section_chord_list_beginning_index = len(section_chord_list)
        # Read meta-data
        if line[0] == "#":
            if line.find("# tonic: ") != -1:
                # cut off '# tonic: ' from beginning and '\n' from end
                tonic.append(line[9:-1])
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
                previous_N = False
                while remaining_measure.find(" ") != -1:
                    #print("Remaining Measure: " + remaining_beat)
                    next_space = remaining_measure.find(" ")
                    # McGillChord is in between spaces, if it contains a colon
                    chord_name = remaining_measure[:next_space]
                    repeat = False
                    if(chord_name.find(".")==-1):
                        if(chord_name.find(":")==-1):
                            remaining_measure = remaining_measure[next_space + 1:]
                            previous_N = True
                            continue
                    else:
                        repeat = True
                    #print("McGillChord: " + chord_name)
                    if len(measure_chord_list) != 0 and repeat and not previous_N:
                        measure_chord_list[-1].duration += 1
                    elif repeat and previous_N:
                        # If a . comes after an N, also ignore the . and record previous_N as true still
                        #  in case of "N . . . ."
                        remaining_measure = remaining_measure[next_space + 1:]
                        continue
                    else:
                        to_append = McGillChord(chord_name, 1)
                        if pychord_chord:
                            to_append = to_append.toPychord()
                        measure_chord_list.append(to_append)
                    previous_N = False
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

# Call get_chord_list for each file inside parent folder and organize based on tonic
# parent_folder should be set to "../data/McGill-Billboard"
# return dictionary (key, value) = (tonic, a list of arrays where each array is the chord list of a song)
def get_all_data (parent_folder, pychord_chord = False):
    # Create dictionary to store chordLists by tonic
    data = dict()
    # Call getChordList on every file in the dataset
    for folder in os.listdir(parent_folder):
        tonic, chord_list = get_chord_list(parent_folder + "/" + folder + "/salami_chords.txt", pychord_chord)
        # Add each song's chordList to the dictionary by first tonic
        if tonic[0] in data:
            data[tonic[0]].append(chord_list)
        else:
            data[tonic[0]] = [chord_list]
    return data

# Convert a McGillChord object into key irrespective notation for a given tonic
#  Exs: 1:maj, 2:min, 3:min, 4:maj, 5:maj, 6:min, 7:dim
#  For minor chords, you may see 3:maj for a III or 7b:maj for a VII in natural minor
#
#  Note: chord types (':maj' or ':min') are not converted AT ALL. This function only converts the root name,
#   hence the use of '7b:maj' for VII, which uses a different 7th than a vii0 would.
#   Also, "x:__" represents a non-diatonic chord or other error
def key_irrespective_chord (tonic, chord, pychord_chord = False):
    # Create notes list to reference later. Only sharps are used. Any flats can look to one index before their base.
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    # Record intervals for a generic scale (2 = whole step, 1 = half step)
    intervals = [2, 2, 1, 2, 2, 2, 1]

    # Find tonic within the notes list
    try:
        tonic_index = notes.index(tonic)
    except:
        # If tonic has a flat in it, use the index before the base note
        tonic_index = notes.index(tonic[:1]) - 1

    error = False
    chord_root = chord.chord[:chord.chord.find(":")]
    chord_type = chord.chord[chord.chord.find(":"):]
    
    try:
        chord_index = notes.index(chord_root)
    except:
        try:
            # If chord name has a flat in it, use the index before the base note
            chord_index = notes.index(chord_root[:1]) - 1
        except:
            # McGillChord name not properly formatted
            error = True
    
    if not error:
        # Find now much forward the chord_index is compared to the tonic
        index_difference = (chord_index - tonic_index + len(notes)) % len(notes)
        interval_sum = 0
        interval_index_counter = 0
        diatonic = True
        minor = False
        #print("Difference between", tonic, "and", chord_root, ":", index_difference)
        while diatonic and interval_sum != index_difference:
            #print("Counter:", interval_index_counter)
            # If the chord can't be found within our intervals, it is non-diatonic
            try:
                # Check for lowered 3rds 6ths and 7ths to check for minor mode
                #  indexes are subtracted by 2 because we index from 0 and because the interval for a 1 chord is 0 and thus ommitted
                if interval_index_counter in [1, 4, 5] and interval_sum + intervals[interval_index_counter] - 1 == index_difference:
                    minor = True
                    break
                interval_sum += intervals[interval_index_counter]
            except:
                diatonic = False
            interval_index_counter += 1

        if minor:
            # Since a 1 chord is tonic, add 1 to the interval_index_counter
            #  And, to record the chord as a flat instead of a sharp, add an extra 1
            #  Note: I chose to have all chords default to a flattened 3, 6, or 7 because I want to keep chord names unique!
            chord_root_num = str(interval_index_counter + 2) + "b"
        elif diatonic:
            # Since a 1 chord is tonic, add 1 to the interval_index_counter
            chord_root_num = interval_index_counter + 1 
        else:
            chord_root_num = "x"
            #print(chord_root, chord_type, "in key", tonic, "labeled as x")

        to_return =  McGillChord(str(chord_root_num) + chord_type, chord.duration, True)
        if pychord_chord:
            return to_return.toPychord()
        else:
            return to_return
    else:
        # If something goes wrong, don't add the chord to the new list.
        #  Seems like I've gotten rid of all errors, but I'm keeping this in here just in case.
        print("There was an error with chord:", chord)

# Convert a given (tonic, chordList) into key-irrespective form
#  returns a new chord_list if applicable
#  return empty list if there are key changes or any errors in tonic
def key_irrespective_list (tonic_list, chord_list, pychord_chord = False):
    new_chord_list = []
    # Ignore lists where there are key changes
    if len(tonic_list) == 1:
        tonic = tonic_list[0]
        # If tonic has double sharps or flats, ignore the list
        if len(tonic) <=2:
            for section_chord_list in chord_list:
                new_section_chord_list = []
                for chord in section_chord_list:
                    new_section_chord_list.append(key_irrespective_chord(tonic, chord, pychord_chord))
                new_chord_list.append(new_section_chord_list)
                new_section_chord_list = []
            
    return new_chord_list

# Call get_chord_list for each file inside parent folder and convert it to key irrespective
# parent_folder should be set to "../data/McGill-Billboard"
# return list of lists where each inner list is the key irrespective chord list of a song
def get_all_data_key_irrespective (parent_folder, pychord_chord = False):
    # Create list to store chordLists
    data = []
    # Call get_chord_list on every file in the dataset
    for folder in os.listdir(parent_folder):
        tonic, chord_list = get_chord_list(parent_folder + "/" + folder + "/salami_chords.txt")
        # Add each song's chord_list to the list
        data.append(key_irrespective_list(tonic, chord_list, pychord_chord))
    return data

## Tests ##

#print(get_chord_list("../data/McGill-Billboard/0089/salami_chords.txt"))
#print(get_all_data_key_irrespective("../data/McGill-Billboard"))
#get_all_data_key_irrespective("../data/McGill-Billboard")
#print(get_all_data("../data/McGill-Billboard"))
#get_all_data("../data/McGill-Billboard")
#notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
#for note in notes:
#    print(note, "with tonic C:", key_irrespective_chord("C", McGillChord(note + ":maj"), True))
#print(key_irrespective_chord("C", McGillChord("Bb:min"), True))
#print(key_irrespective_chord("A", McGillChord("G:min")))

# Test
#print(get_chord_list("McGill-Billboard/0089/salami_chords.txt"))
#data = get_all_data_key_irrespective("../data/McGill-Billboard")
#noneCount = 0
#for song in data:
#    for section in song:
#        for chord in section:
#            if chord == None:
#                noneCount += 1
#print(noneCount)