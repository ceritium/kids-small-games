#!/usr/bin/env python3

import multiprocessing
import random
import signal
import sys
import urwid
import pyttsx3

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    if sys.platform == 'linux':
        engine.setProperty('voice', 'spanish')
    engine.say(phrase)
    engine.runAndWait()

def signal_handler(_sig, _frame):
    print('\nBye')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    Game()

class Game:
    DICT = [
            'VERONICA',
            'GATO',
            'PATO',
            'PERRO',
            'DEDO',
            'PELOTA',
            'MOCO',
            'PEDO',
            'DADO',
            'CAMINO',
            'PAPA',
            'MAMA',
            'CAMISA',
            'VASO',
            'ROJO',
            'ROSA',
            'GATA',
            'PERRA',
            'PATA',
            'CAMA',
            'MESA',
            'PESA',
            'OJO',
            'AJO',
            'HOJA',
            'PERA',
            ]

    MISSING_LETTER = '_'
    VOWELS = 'AEIOU'

    def __init__(self):
        self.text = None
        self.pair = None
        self.txt = urwid.Text("", align='center')
        fill = urwid.Filler(self.txt, 'middle')
        self.loop = urwid.MainLoop(fill, unhandled_input=self.handle_input)

        self.new_round()
        self.loop.run()

    @classmethod
    def text_decorator(cls, string, kind):
        if(kind == 'success'):
            color_bg = urwid.AttrSpec('default', 'dark green')
        else:
            color_bg = urwid.AttrSpec('default', 'dark red')

        return [(color_bg, f" {string} ")]

    @classmethod
    def say(cls, text):
        if __name__ == "__main__":
            process = multiprocessing.Process(target=sayFunc, args=(text,))
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
        self.text = self.pair[1]
        self.txt.set_text(self.text)

    def alarm_new_round(self, _loop=None, _data=None):
        self.new_round()

    def new_challenge(self):
        word = random.choice(Game.DICT)
        challenge = Game.replace_word(word)
        while challenge == word:
            challenge = Game.replace_word(word)

        self.pair = (word, challenge)

    def new_round(self):
        self.new_challenge()
        self.text = self.pair[1]
        self.txt.set_text(self.text)
        Game.say(self.pair[0])

    def handle_input(self, key):
        if isinstance(key, str) and len(key) == 1:
            self.text = self.text.replace(Game.MISSING_LETTER, key.upper(), 1)
            self.txt.set_text(self.text)
            if(not(Game.MISSING_LETTER in self.text)):
                if self.pair[0] == self.text:
                    self.txt.set_text(self.text_decorator(self.text, "success"))
                    self.loop.set_alarm_in(1, self.alarm_new_round)
                else:
                    self.txt.set_text(self.text_decorator(self.text, "error"))
                    self.loop.set_alarm_in(2, self.alarm_reset_text)
                    Game.say(self.pair[0])

if __name__=="__main__":
    main()
