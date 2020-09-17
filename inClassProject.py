import math

def midi_to_hertz(midi):
    return 440 * 2 ** ((midi-69)/12)

def get_letter(pc, offset):
    letters = (("B#", "C", "Dbb"), ("C#", "Db"), ("C##", "D", "Ebb"), ("D#", "Eb"), ("D##", "E", "Fb"), ("E#", "F", "Gbb"), ("F#", "Gb"), ("F##", "G", "Abb"), ("G#", "Ab"), ("G##", "A", "Bbb"), ("A#", "Bb", "Cbb"), ("B", "Cb"))
    try:
        return letters[pc][int(offset + 1)]
    except(IndexError):
        return 0

def pitch_data(knum1, knum2):
    
    out = []
    

    for key in range(knum1, knum2 + 1):
        octave = key // 12
        pc = key % 12
        hertz = midi_to_hertz(key)
        # This iterates the possible accidentals for the note.  If the range
        #   is below 0, then it is enharmonic equivalent below the pc, and a
        #   positive number adds to the pc.  Then, the pc is represented by 
        #   two integers: the actual pitch, and the enharmonic equivalent.  
        #   This allows the octave to change accordingly if the enharmonic 
        #   equivalent belongs to a different octave, and give flexibility 
        #   with different enharmonic equivalents.  If a certain enharmonic 
        #   doesn't exist, then the index error is caught in the get_letter
        #   function, and the loop simply breaks because there are no more
        #   enharmonics to include for the given note.
        for offset in range(-1, 2):
            letter = get_letter(pc, offset)
            if (letter != 0):
                out.append((str(letter + str(int(octave + (pc + offset) // 12))), key, pc, hertz))
            else:
                break
        

    return out


if __name__ == '__main__':
    l = pitch_data(60, 72)
    print("pitch_data: \n\n")
    for tup in l:
        print(tup,"\n")
    