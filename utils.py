import tempfile
import os
import multiprocessing
import sys

from gtts import gTTS

def sayFunc(phrase, slow=False, audio_options = {}):
    lang = audio_options['language'] or 'es'
    module = audio_options['module']

    tts = gTTS(text=phrase, lang=lang, slow=slow)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name
    tts.save(filename)
    command = "mpg123"
    if module:
        command = f"{command} -o {module}"
    command = f"{command} {filename} > /dev/null 2>&1"
    os.system(command)
    os.unlink(filename)

def say(text, slow=False, audio_options={}):
    process = multiprocessing.Process(target=sayFunc, args=(text, slow, audio_options,))
    process.start()

def signal_handler(_sig, _frame):
    print('\nBye')
    sys.exit(0)
