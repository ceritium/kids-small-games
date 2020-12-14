#!/usr/bin/env python3

import urwid
import pyttsx3
import signal
import sys
import multiprocessing

class Game:
    def __init__(self):
        self.text = "HOLA!"
        self.txt = urwid.Text(self.text, align='center')
        fill = urwid.Filler(self.txt, 'middle')
        loop = urwid.MainLoop(fill, unhandled_input=self.handle_input)
        loop.run()

    def say(self, text):
        if __name__ == "__main__":
            p = multiprocessing.Process(target=sayFunc, args=(text,))
            p.start()

    def handle_input(self, key):
        if isinstance(key, str) or type(key) == 'unicode':
            if key == 'enter':
                if len(self.text) > 0:
                    self.say(self.text)
                    self.text = ""
            elif key == 'backspace':
                self.text = self.text[:-1]
            else:
                self.text = self.text + key

        self.txt.set_text(self.text.upper())

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
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

if __name__=="__main__":
    main()
