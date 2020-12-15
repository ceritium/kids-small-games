import tempfile
import os
import multiprocessing

from gtts import gTTS

def sayFunc(phrase, slow=False):
    tts = gTTS(text=phrase, lang='es', slow=slow)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name
    tts.save(filename)
    os.system("mpg123 " + filename + " > /dev/null 2>&1")
    os.unlink(filename)

def say(text, slow=False):
    process = multiprocessing.Process(target=sayFunc, args=(text, slow,))
    process.start()
