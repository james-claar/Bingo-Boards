"""
Plays notes in a song.
"""

import time
import winsound

NOTE_KEY = {
    "Cb":-1,
    "C":0,
    "C#":1,
    "Db":1,
    "D":2,
    "D#":3,
    "Eb":3,
    "E":4,
    "Fb":4,
    "E#":5,
    "F":5,
    "F#":6,
    "Gb":6,
    "G":7,
    "G#":8,
    "Ab":8,
    "A":9,
    "A#":10,
    "Bb":10,
    "B":11,
    "B#":12
}


songs = [
    {
        #In the mountain king's chamber or something
        "tempo":180,
        "octaves":[ 4,   4,    4,   4,   4,   4,   4,   4,   4,    4,    4,    4,   4,   4,   4,   4,   4,   4,    4,   4,   4,   4,   4,   5,   5,   4,   4,   4,   5,   5,   5,   5],
        "notes":  ["E", "F#", "G", "A", "B", "G", "B", " ", "A#", "F#", "A#", " ", "A", "F", "A", " ", "E", "F#", "G", "A", "B", "G", "B", "E", "D", "B", "G", "B", "D", " ", " ", " "]
    },
    {
        #Nutcracker thing
        "tempo":300,
        "octaves":[ 4,   4,   4,   4,    4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,    4,    4,    4,    4,   5,    5,    5,    5,   5,   5,   5,   4,   4,   4,   4,    4,    4,    4,    4,   5,   5,   5,   5],
        "notes":  ["G", "G", "G", "Eb", " ", " ", " ", "F", "F", "F", "D", " ", " ", " ", "G", "G", "G", "Eb", "Ab", "Ab", "Ab", "G", "Eb", "Eb", "Eb", "C", " ", " ", " ", "G", "G", "G", "Eb", "Ab", "Ab", "Ab", "G", "F", "F", "F", "D"]
    },
    {
        #Song James made up
        "tempo":150,
        "octaves":[ 4,    4,    4,   4,   4,   4,   4,   4,   3,    3,   3,   3,    3,    4,   4,    4,   4,   4,   4,   4,    5,   5],
        "notes":  ["G#", "A#", "G", "E", "G", "C", "F", "C", "G#", "F", "G", "G#", "A#", "C", "C#", "C", "D", "E", "F", "G#", "C", "F"]
    }
]


picked_song = int(input("Which song would you like? (1 - %s) >>> " % len(songs)))


picked_song = songs[picked_song - 1]
tempo   = picked_song["tempo"]
octaves = picked_song["octaves"]
notes   = picked_song["notes"]


def playnote(note, octave):
    note_to_play = NOTE_KEY[note] + octave * 12 + 3
    winsound.Beep(int(round(27.5*1.059463**note_to_play)), int(round(60 / tempo * 1000)))


for i in range(len(notes)):
    if notes[i] == " ":
        time.sleep(60 / tempo)
    else:
        playnote(notes[i], octaves[i])