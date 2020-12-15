#!/usr/bin/env python3

import signal
import sys
import multiprocessing

import urwid
import utils

class Game:
    def __init__(self):
        self.text = "HOLA!"
        self.txt = urwid.Text(self.text, align='center')
        fill = urwid.Filler(self.txt, 'middle')
        loop = urwid.MainLoop(fill, unhandled_input=self.handle_input)
        loop.run()

    def handle_input(self, key):
        if isinstance(key, str) or type(key) == 'unicode':
            if key == 'enter':
                if len(self.text) > 0:
                    utils.say(self.text)
                    self.text = ""
            elif key == 'backspace':
                self.text = self.text[:-1]
            else:
                self.text = self.text + key

        self.txt.set_text(self.text.upper())

def signal_handler(_sig, _frame):
    print('\nBye')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    Game()

if __name__=="__main__":
    main()
