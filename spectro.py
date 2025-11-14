import RPi.GPIO as GPIO
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import time

# --------------------------
# GPIO Setup
# --------------------------
SOUND_PIN = 17  # KY-038 DO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Change to PUD_UP if needed

# --------------------------
# Audio Config
# --------------------------
FS = 44100           # Sampling frequency
DURATION = 2         # Seconds to record per detection

# --------------------------
# Callback function
# --------------------------
def sound_detected(channel):
    if GPIO.input(channel):
        print("🔊 Sound detected! Recording audio...")
        audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float32')
        sd.wait()
        audio = audio.flatten()
        
        # Generate spectrogram
        f, t, Sxx = spectrogram(audio, fs=FS, nperseg=1024)
        plt.figure(figsize=(8, 4))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='inferno')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.title('Sound Spectrogram')
        plt.colorbar(label='Intensity [dB]')
        plt.ylim(0, 8000)  # optional
        plt.show()

# --------------------------
# Set up event detection
# --------------------------
GPIO.add_event_detect(SOUND_PIN, GPIO.RISING, callback=sound_detected, bouncetime=300)

print(f"Waiting for sound on GPIO{SOUND_PIN} (press Ctrl+C to exit)...")

# --------------------------
# Main loop (idle)
# --------------------------
try:
    while True:
        time.sleep(1)  # just wait for KY-038 events

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
