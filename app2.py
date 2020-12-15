#!/usr/bin/env python3

import multiprocessing
import random
import signal
import sys
import unicodedata
import tempfile
import os

import urwid

from gtts import gTTS

def sayFunc(phrase, slow):
    tts = gTTS(text=phrase, lang='es', slow=slow)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name
    tts.save(filename)
    os.system("mpg123 " + filename + " > /dev/null 2>&1")
    os.unlink(filename)

def signal_handler(_sig, _frame):
    print('\nBye')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    Game()

class Game:
    DICT = list(map(lambda x: x.strip().upper(), open('simple_words.txt').readlines()))
    MISSING_LETTER = '_'
    VOWELS = 'AEIOU'

    def __init__(self):
        self.text = None
        self.word = None
        self.slow = False
        self.txt = urwid.Text("", align='center')
        fill = urwid.Filler(self.txt, 'middle')
        self.loop = urwid.MainLoop(fill, unhandled_input=self.handle_input)

        self.new_round()
        self.loop.run()

    @classmethod
    def strip_accents(cls, text):
        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")
        return str(text)

    @classmethod
    def text_decorator(cls, string, kind):
        if(kind == 'success'):
            color_bg = urwid.AttrSpec('default', 'dark green')
        else:
            color_bg = urwid.AttrSpec('default', 'dark red')

        return [(color_bg, f" {string} ")]

    @classmethod
    def say(cls, text, slow):
        if __name__ == "__main__":
            process = multiprocessing.Process(target=sayFunc, args=(text, slow,))
            process.start()

    @classmethod
    def replace_letter(cls, letter):
        if letter in Game.VOWELS and bool(random.getrandbits(1)):
            return Game.MISSING_LETTER
        else:
            return letter

    @classmethod
    def replace_word(cls, word):
        return "".join(list(map(Game.replace_letter, word)))

    def alarm_reset_text(self, _loop=None, _data=None):
        self.text = self.word['challenge']
        self.txt.set_text(self.text)

    def alarm_new_round(self, _loop=None, _data=None):
        self.new_round()

    def new_challenge(self):
        word = random.choice(Game.DICT)
        screen = Game.strip_accents(word)

        challenge = Game.replace_word(screen)
        while challenge == screen:
            challenge = Game.replace_word(screen)

        self.word = {'speak': word, 'screen': screen, 'challenge': challenge}

    def new_round(self):
        self.slow = False
        self.new_challenge()
        self.text = self.word['challenge']
        self.txt.set_text(self.text)
        Game.say(self.word['speak'], self.slow)

    def toggle_slow(self):
        self.slow = not self.slow
        return self.slow

    def handle_input(self, key):
        if isinstance(key, str) and len(key) == 1:
            self.text = self.text.replace(Game.MISSING_LETTER, key.upper(), 1)
            self.txt.set_text(self.text)
            if(not(Game.MISSING_LETTER in self.text)):
                if self.word['screen'] == self.text:
                    self.txt.set_text(self.text_decorator(self.text, "success"))
                    self.loop.set_alarm_in(1, self.alarm_new_round)
                else:
                    self.txt.set_text(self.text_decorator(self.text, "error"))
                    self.loop.set_alarm_in(2, self.alarm_reset_text)
                    Game.say(self.word['speak'], self.toggle_slow())

if __name__=="__main__":
    main()
