# pyaudioop.py - Compatibility shim
import audioop
import sys

# Make audioop available as pyaudioop
sys.modules['pyaudioop'] = audioop


# At the top of your files that use pydub
import pyaudioop  # This loads our compatibility shim
from pydub import AudioSegment