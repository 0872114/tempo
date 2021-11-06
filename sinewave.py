import time

from pysinewave import SineWave

# Create a sine wave, with a starting pitch of 12, and a pitch change speed of 10/second.
sinewave = SineWave(pitch=24, pitch_per_second=10)
sinewave.output_stream
