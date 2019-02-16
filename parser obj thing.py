import numpy as np
import pandas as pd
import re
import os

#Fill in array with the chord names/durations
#return (tonic, chordlist)
def getChordList(filepath):
    pass

# Call getChorList for each file inside parent folder and organize based on tonic
# return dictionary (key, value) = (tonic, 2d array where each row is the chord list of a song)
def getAllData(location_of_parent_folder):
    pass

filepathnum = 3 # points to the file number in the name (ie. 0003, 0006, etc.)
i = 0 # counts how many iterations of the loop
namecounter = 0 # variable that counts how many times a non existent file was opened
check = 0 # variable to check if the Song Number text should be printed (depends on if the file being opened exits)

#get chord list
#basically for each file make list sort of thing with tonic and chords in the song

#loop through getting info from each file
while (i < 1298):
    label = "Song Number " + str(i-namecounter) + ": \n"
    if check == 0:
        label = "Song Number " + str(i-namecounter) + ": \n"
        print(label)
    check = 0
    filepathname = str(filepathnum).zfill(4)
    path = os.path.abspath('./billboard_data_new/McGill-Billboard/' + filepathname + '/salami_chords.txt')
    fout = open('database_new.txt', 'a+')
    try:
        with open(path) as file:
            file_contents = file.read()
            print(file_contents)
            fout.write(label)
            fout.write(file_contents)
    except IOError:
        namecounter = namecounter + 1
        check = 1
    i = i + 1
    filepathnum = filepathnum + 1
    
