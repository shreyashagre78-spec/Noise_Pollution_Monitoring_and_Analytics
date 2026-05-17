import sounddevice as sd
import numpy as np
import time

# Constants
FS = 44100  # Sample rate
DURATION = 1  # Seconds per sample
REF_PRESSURE = 0.00002  # Reference pressure for dB calculation

def calculate_db(indata):
    # Calculate Root Mean Square (RMS) of the audio signal
    rms = np.sqrt(np.mean(indata**2))
    if rms > 0:
        # Convert RMS to Decibels
        db = 20 * np.log10(rms / REF_PRESSURE)
        return round(db, 2)
    return 0

print("Monitoring Noise Levels... Press Ctrl+C to stop.")

try:
    with open("noise_log.csv", "w") as f:
        f.write("Timestamp,Decibel_Level\n")
        while True:
            # Record a short burst of audio
            recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
            sd.wait()
            
            level = calculate_db(recording)
            timestamp = time.strftime('%H:%M:%S')
            
            print(f"[{timestamp}] Current Noise: {level} dB")
            f.write(f"{timestamp},{level}\n")
            f.flush() # Ensure data is saved immediately
            
except KeyboardInterrupt:
    print("\nMonitoring stopped. Data saved to noise_log.csv")