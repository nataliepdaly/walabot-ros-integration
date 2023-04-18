import WalabotAPI as wbt
import time
import numpy as np

# Walabot settings
PROF_SENSOR_NARROW = wbt.PROF_SENSOR_NARROW
FILTER_TYPE_DERIVATIVE = wbt.FILTER_TYPE_DERIVATIVE

# Parameters
PEAK_THRESHOLD = 0.4  # Adjust this value to fine-tune peak detection
TIME_WINDOW = 7  # Number of recent peaks to consider for breaths per minute calculation

# Variables
prev_energy = 0
peak_timestamps = []

Rmin, Rmax, RRes = 10, 100, 2
Tmin, Tmax, TRes = -15, 15, 2
Pmin, Pmax, PRes = -45, 45, 2

# Initialize and connect to the Walabot
wbt.Init()
wbt.SetSettingsFolder()
wbt.ConnectAny()

# Set Walabot parameters
wbt.SetProfile(PROF_SENSOR_NARROW)
wbt.SetArenaR(Rmin, Rmax, RRes)
wbt.SetArenaTheta(Tmin, Tmax, TRes)
wbt.SetArenaPhi(Pmin, Pmax, PRes)
wbt.SetDynamicImageFilter(FILTER_TYPE_DERIVATIVE)

# Start Walabot
wbt.Start()

try:
    while True:
        # Get status and trigger Walabot
        lastStatus = wbt.GetStatus()
        wbt.Trigger()

        # Get image energy and process collected data
        energy = wbt.GetImageEnergy()
        # Detect peaks in breathing energy
        if energy > PEAK_THRESHOLD and prev_energy <= PEAK_THRESHOLD:
            current_time = time.time()
            peak_timestamps.append(current_time)

            # Remove old peaks
            while len(peak_timestamps) > 0 and peak_timestamps[0] < current_time - 60:
                peak_timestamps.pop(0)

            # Calculate breaths per minute
            if len(peak_timestamps) > 1:
                intervals = np.diff(peak_timestamps)
                avg_interval = np.mean(intervals)
                breaths_per_minute = 60 / avg_interval
                print("Breaths per minute:", breaths_per_minute)

        prev_energy = energy

        # Sleep for a short period to reduce the data collection rate
        time.sleep(0.1)

except KeyboardInterrupt:
    # Stop and disconnect the Walabot
    wbt.Stop()
    wbt.Disconnect()
    print("Walabot disconnected")
