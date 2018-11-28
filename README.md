# NLTKSpeaker

Speech Synthesiser

This Speaker takes text input from a user and convert it to a sound waveform containing intelligible speech.
This will be a basic waveform concatenation system, whereby the acoustic units are recordings of diphones.

# Modules
audio.py
This is a version of the audio.py module that the Audio class contained therein will allow you to save, load and play .wav files as well as perform some simple audio processing functions

speaker.py
This is a skeleton structure for your program,

diphones/ 
A folder containing .wav files for the diphone sounds. A diphone is a voice recording lasting from the middle of one speech sound to the middle of a second speech sound (i.e. the transition between two speech sounds). 

examples/
A folder containing example .wav files of how the synthesiser should sound.

# NLTK Parts
this speaker using nltk.corpus.cmudict, the part of NLTK.

• expand the phone sequence to the corresponding diphone sequence
• concatenate the necessary diphone wav files together in the right order to produce the required synthesised audio in an instance of the Audio class. 

you should be able to execute your program by running the synth.py script from the command line with arguments, e.g. the following should play “hello”:-

python speaker.py -p "hello"

python synth.py -o rose.wav "A rose by any other name would smell as sweet"

# TODO 

TODO – Emphasis markup
One way emphasis can be indicated on a word is by increased loudness, duration and some pitch (f0) accent. Implement a simplified version of this in your synthesiser. Allow the user to put curly braces around any 1 word in the input text, and increase the loudness (don’t worry about duration or pitch) of that word noticeably compared to the rest of the utterance. So, for example:
     "The {cat} sat on the mat."
     -> the word ‘cat’ should sound louder than the rest of the utterance.

TODO – Smoother Concatenation
Simply pasting together diphone audio waveforms one after the other can lead to audible glitches where the waveform “jumps” at join points. Implement a simple way to alleviate this by “cross-fading” between adjacent diphones using a 10 msec overlap. (To achieve a cross-fade, you need to lower the amplitude at the end of one diphone down to 0.0 over 10msec and then add in the signal from the start of the next diphone which is similarly tapered from 0.0 to normal amplitude over the same 10msec period). Note this will only mitigate one cause of “choppiness” in the synthetic speech and so can only do so much! Audio examples are provided for you to compare cross-faded concatenation with simple concatenation. 

TODO  – Text Normalisation for Dates
If the string contains dates in the form DD/MM, DD/MM/YY or DD/MM/YYYY, then convert them to word sequences, e.g. –
     "John Lennon died on 8/12/80"
     -> "john lennon died on december eighth nineteen eighty"


