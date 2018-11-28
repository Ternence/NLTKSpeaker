import os

import nltk

import audio
import argparse
from nltk.corpus import cmudict
import re

import numpy as np

parser = argparse.ArgumentParser(
    description='A basic text-to-speech app that synthesises an input phrase using diphone unit selection.')
parser.add_argument('--diphones', default="./diphones", help="Folder containing diphone wavs")
parser.add_argument('--play', '-p', action="store_true", default=False, help="Play the output audio")
parser.add_argument('--outfile', '-o', action="store", dest="outfile", type=str, help="Save the output audio to a file",
                    default=None)
parser.add_argument('phrase', nargs=1, help="The phrase to be synthesised")

# Arguments for extensions
parser.add_argument('--spell', '-s', action="store_true", default=False,
                    help="Spell the phrase instead of pronouncing it")
parser.add_argument('--crossfade', '-c', action="store_true", default=False,
                    help="Enable slightly smoother concatenation by cross-fading between diphone units")
parser.add_argument('--volume', '-v', default=None, type=int,
                    help="An int between 0 and 100 representing the desired volume")

args = parser.parse_args()

print(args.diphones)


class Synth:
    def __init__(self, wav_folder):
        self.diphones = {}
        self.diphones_wavs = self.get_wavs(wav_folder)

    def get_wavs(self, wav_folder):
        '''
        The output of get_wavs is self.diphones which is a dict of the data corresponding to all the .wav files in wav_folder (which will be a slow process).
        It can also be a dict of tmpaudio.Audio objects, e.g. self.diphones[diphone] = tmpaudio
        '''
        tmpaudio = audio.Audio(rate=16000)  # Audio_obj
        for root, dirs, files in os.walk(wav_folder, topdown=False):
            for file in files:
                try:
                    diphone = file[:-4]
                    tmpaudio.load(wav_folder + '/' + file)
                    self.diphones[diphone] = tmpaudio.data
                except:
                    print("error load " + file)
                    pass
        length = 16000 * 0.1  # sample rate = 16000, 100ms = 0.1s
        self.diphones[' '] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.2
        self.diphones[','] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.4
        self.diphones[':'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['!'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['?'] = np.zeros(int(length), tmpaudio.nptype)
        return self.diphones


class Utterance:
    def __init__(self, phrase):
        print(phrase)
        # self.phrase = re.sub("[^a-zA-Z\\s\,:?!]", "", phrase.strip()).lower()
        # Do not remove symbols
        self.phrase = phrase.lower()
        if args.spell is False:
            self.phrase = re.split(r"([.,:?!\s+])", self.phrase)
        print(str(self.phrase))

    def get_phone_seq(self):
        # entries = cmudict.entries()
        word_dict = cmudict.dict()
        phone_seq = []
        for word in self.phrase:
            if len(word) < 1:
                continue
            if word in ' ,.:?!':
                phone_seq.append([word])
            else:
                if word in word_dict:
                    phone = word_dict[word][0]
                    for i in range(len(phone)):
                        phone[i] = re.sub("[^a-zA-Z\\s\-]", "", phone[i]).lower()
                    phone_seq.append(phone)
                # else:
                #     exit('"' + word + '" not found in cmudict, exit!\n')
        return phone_seq

    def get_phone_seq_spell(self):
        try:
            self.arpabet = nltk.corpus.cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            self.arpabet = nltk.corpus.cmudict.dict()

        phone_seq = []
        for word in self.phrase:
            wordbreak = self.word_break(word)
            # print(wordbreak)
            phone_seq.append(wordbreak)

        print("phone_seq " + str(phone_seq).lower())
        return phone_seq

    def word_break(self, s):
        s = s.lower()
        if s in self.arpabet:
            return self.arpabet[s]
        return []


def build_normal_diphones():
    global phone_seq, diphone, array
    phone_seq = utt.get_phone_seq()
    is_space_before = False
    is_first_sentence = False
    first_sentence_index = 0
    index = 0
    for seq in phone_seq:
        # print("seq"  + str(seq))
        if (len(seq) == 1) & (seq[0] in ' ,.:?!'):
            if seq[0] is " ":
                is_space_before = True
            elif '.' in seq or "?" in seq or "!" in seq:
                is_first_sentence = True
                first_sentence_index = index + 1
                diphones.insert(len(diphones), diphones[len(diphones) - 1].split("-")[1] + "-pau")
            else:
                diphones.append(seq[0])
        else:
            if is_first_sentence and index is first_sentence_index:
                diphones.insert(len(diphones), "pau-" + seq[0])

            for j in range(1, len(seq)):
                # print(seq[j-1]+'-'+seq[j])
                diphones.append(seq[j - 1] + '-' + seq[j])
            if is_space_before:
                diphones.insert(len(diphones) - j, phone_seq[index - 2][-1] + "-" + phone_seq[index][0])
                # print("space insert: " + space_)
                is_space_before = False
        if index is 0:
            diphones.insert(0, "pau-" + seq[0])
        elif index is len(phone_seq) - 1:
            diphones.insert(len(diphones), seq[len(seq) - 1] + "-pau")

        index = index + 1
    print(diphones)
    # concate the data
    for diphone in diphones:
        try:
            array = np.append(array, (diphone_synth.diphones[diphone]))
        except:
            pass


def build_spell_diphones():
    global phone_seq, diphone, array
    phone_seq = utt.get_phone_seq_spell()
    for diphone in phone_seq:
        if len(diphone) <= 0:
            continue

        if len(diphone[0]) is 1:
            diphone[0].insert(1, 'pau')

        try:
            phone_name = (diphone[0][0] + "-" + diphone[0][1]).replace("0", "").replace("1", "").lower()
            print(diphone)
            print(phone_name)
            array = np.append(array, diphone_synth.diphones[phone_name])
            array = np.append(array, diphone_synth.diphones['pau-pau'])
        except:
            pass


if __name__ == "__main__":
    utt = Utterance(args.phrase[0])

    diphone_synth = Synth(wav_folder=args.diphones)
    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    out = audio.Audio(rate=16000)
    # generate diphones
    diphones = []
    array = []

    if args.spell is False:
        build_normal_diphones()
    else:
        build_spell_diphones()

    print(array)
    out.data = array.astype(np.int16)

    if args.volume and 100 >= int(args.volume) >= 0:
        out.rescale(args.volume / 100.)
    print(out.data, type(out.data))

    if args.play is True:
        out.play()

    out.save("test.wav")
    if args.outfile:
        out.save(args.outfile)
