#!/usr/bin/env python

import urwid
import pyttsx3
import signal
import sys

engine = pyttsx3.init()
engine.setProperty('volume', 1.0)

if sys.platform == 'linux2':
    engine.setProperty('voice', 'english')

text = u"HOLA!"

def signal_handler(_sig, _frame):
    print('Bye')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

def show_or_exit(key):
    global text
    if isinstance(text, str) or type(key) == 'unicode':
        if key == 'enter':
            if len(text) > 0:
                engine.say(text)
                engine.runAndWait()
                text = ""
        elif key == 'backspace':
            text = text[:-1]
        else:
            text = text + key

    txt.set_text(text.upper())

txt = urwid.Text(text, align='center')
fill = urwid.Filler(txt, 'middle')
loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
loop.run()


