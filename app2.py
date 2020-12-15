#!/usr/bin/env python3

import urwid
import pyttsx3
import signal
import sys
import random
import multiprocessing

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    if sys.platform == 'linux':
        engine.setProperty('voice', 'spanish')
    engine.say(phrase)
    engine.runAndWait()

class Game:
    DICT = [
            ('VERONICA', 'VER_NICA'),
            ('VERONICA', 'V_R_N_C_'),
            ('PAPA', 'PAP_'),
            ('MAMA', 'M_MA'),
            ('VERO', 'VER_'),
            ('VERO', 'V_RO'),
            ('VERO', 'V_R_'),
            ('GATO', 'G_TO'),
            ('GATO', 'GAT_'),
            ('GATO', 'G_T_'),
            ('PATO', 'P_T_'),
            ('PATO', 'PAT_'),
            ('PATO', 'P_TO'),
            ('DEDO', 'D_DO'),
            ('DEDO', 'DED_'),
            ('DEDO', 'D_D_'),
            ('DADO', 'D_D_'),
            ('DADO', 'DAD_'),
            ('DADO', 'D_DO'),
            ('LORO', 'L_RO'),
            ('LORO', 'LOR_'),
            ('LORO', 'L_R_'),
            ('MOCO', 'M_CO'),
            ('MOCO', 'MOC_'),
            ('MOCO', 'M_C_'),
        ]

    def __init__(self):
        self.text = None
        self.txt = urwid.Text("", align='center')
        fill = urwid.Filler(self.txt, 'middle')
        self.loop = urwid.MainLoop(fill, unhandled_input=self.handle_input)

        self.new_round()
        self.loop.run()

    @classmethod
    def text_decorator(cls, string, kind):
        if (kind == 'success'):
            color_bg = urwid.AttrSpec('default', 'dark green')
        else:
            color_bg = urwid.AttrSpec('default', 'dark red')
        return [(color_bg, f" {string} ")]


    def say(self, text):
        if __name__ == "__main__":
            process = multiprocessing.Process(target=sayFunc, args=(text,))
            process.start()


    def alarm_reset_text(self, _loop=None, _data=None):
        self.text = self.pair[1]
        self.txt.set_text(self.text)

    def alarm_new_round(self, _loop=None, _data=None):
        self.new_round()

    def new_round(self):
        self.pair = random.choice(Game.DICT)
        self.text = self.pair[1]
        self.txt.set_text(self.text)
        self.say(self.pair[0])

    def handle_input(self, key):
        if isinstance(key, str) or type(key) == 'unicode':
            self.text = self.text.replace('_', key.upper(), 1)
            self.txt.set_text(self.text)
            if(not("_" in self.text)):
                if self.pair[0] == self.text:
                    self.txt.set_text(self.text_decorator(self.text, "success"))
                    self.loop.set_alarm_in(1, self.alarm_new_round)
                else:
                    self.txt.set_text(self.text_decorator(self.text, "error"))
                    self.loop.set_alarm_in(2, self.alarm_reset_text)
                    self.say(self.pair[0])

def signal_handler(_sig, _frame):
    print('\nBye')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    Game()

if __name__=="__main__":
    main()
