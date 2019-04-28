# Music Maker (Backend)

2019 EoH SIGMusic Project   
[Frontend Repo](https://github.com/SIGMusic/musicMaker-frontend)

The Music Maker Backend is a rest API made using Flask. At the moment, it has two main services: getting the name of the chord from the notes, then getting the next chord from a list of previous chords.

## Getting Started

Clone the repository onto your local machine by running `git clone https://github.com/SIGMusic/musicMaker-backend.git`

### Prerequisites

To install the dependencies for the repository, run -r `pip install requirements.txt` in your virtualenv.

## How to use the API

###### Chord name from notes

```
http://127.0.0.1:5000/chordname?notes=arg1,arg2,...,arg7
```

In which the args are the midi numbers for each of the notes, up to 7 different notes. It will return a JSON with the name of the chord.

###### Next chord from previous chords

```
http://127.0.0.1:5000/nextchord?chords=arg1,arg2,...,argn
```

In which the args are the chord names for each of the previosu chords, with an arbitrary number of previous chords. It will return a JSON of next chord names mapped to probabilities of each chord happening.
