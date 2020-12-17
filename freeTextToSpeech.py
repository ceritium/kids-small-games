#!/usr/bin/env python3

import signal
import sys
import argparse

import urwid
import utils

class Game:
    def __init__(self, opts):
        self.audio_options = {
                'language': opts['audio_language'],
                'module': opts['audio_module']
                }

        self.text = "HOLA!"

        palette = [
            ('titlebar', 'black', 'white'),
            ('enter button', 'dark green,bold', 'black'),
            ('quit button', 'dark red,bold', 'black'),
            ('getting quote', 'dark blue', 'black')]

        header_text = urwid.Text(u'FREE TEXT TO SPEECH')
        header = urwid.AttrMap(header_text, 'titlebar')

        menu = urwid.Text([
            u'Press (', ('enter button', u'ENTER'), u') to speech. ',
            u'Press (', ('quit button', u'CTRL-C'), u') to quit. ',
            ])

        self.txt = urwid.Text(self.text, align='center')
        quote_filler = urwid.Filler(self.txt, valign='middle', top=1, bottom=1)
        v_padding = urwid.Padding(quote_filler, left=1, right=1)
        quote_box = urwid.LineBox(v_padding)

        layout = urwid.Frame(header=header, body=quote_box, footer=menu)

        # Create the event loop
        loop = urwid.MainLoop(
                layout, palette, unhandled_input=self.handle_input)
        loop.run()

    def handle_input(self, key):
        if isinstance(key, str) or type(key) == 'unicode':
            if key == 'enter':
                if len(self.text) > 0:
                    utils.say(self.text, audio_options=self.audio_options)
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

    Game(vars(init_argparse().parse_args()))

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Print or check SHA1 (160-bit) checksums."
    )
    parser.add_argument("-am", "--audio-module")
    parser.add_argument("-al", "--audio-language")
    return parser


if __name__ == "__main__":
    main()
