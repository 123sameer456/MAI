# pyaudioop.py - Compatibility shim
import audioop
import sys

# Make audioop available as pyaudioop
sys.modules['pyaudioop'] = audioop


# At the top of your files that use pydub
import pyaudioop  # This loads our compatibility shim
from pydub import AudioSegment

# Test to verify audioop works
try:
    test_data = b'\x00\x01\x02\x03'  # dummy audio bytes
    rms_value = audioop.rms(test_data, 1)  # width=1 byte
    print(f"[TEST] audioop is working. RMS value: {rms_value}")
except Exception as e:
    print(f"[TEST] audioop failed: {e}")

print("sheke")