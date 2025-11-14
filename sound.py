import RPi.GPIO as GPIO
import time

# --------------------------
# Configuration
# --------------------------
SOUND_PIN = 17  # Connect KY-038 DO pin to GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # try PUD_UP if always 0

# --------------------------
# Main loop
# --------------------------
print(f"Listening for sound on GPIO{SOUND_PIN} (press Ctrl+C to exit)...")
last_state = None

try:
    while True:
        state = GPIO.input(SOUND_PIN)
        if state != last_state:
            if state:
                print("🔊 Sound detected! (HIGH)")
            else:
                print("🔈 Sound ended (LOW)")
            last_state = state
        time.sleep(0.05)  # poll every 50ms

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
