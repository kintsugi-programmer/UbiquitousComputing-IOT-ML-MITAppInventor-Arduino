import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# ---- Step 1: Load the CSV file ----
CSV_PATH = "1-1-KARTIK_1744014440.csv"  # 🔁 Change this to your actual CSV file path
df = pd.read_csv(CSV_PATH)

# ---- Step 2: Parse the rawData column ----
raw_data_str = df['rawData'][0]  # Assuming 1 row
raw_data = ast.literal_eval(raw_data_str)
accel_data = raw_data['accelerometer']

x_vals = accel_data['x']
y_vals = accel_data.get('y', [0] * len(x_vals))  # Safe fallback
z_vals = accel_data.get('z', [0] * len(x_vals))
sampling_rate = accel_data['samplingFrequency']  # Hz

# ---- Step 3: Create time axis ----
time = np.arange(0, len(x_vals)) / sampling_rate

# ---- Step 4: Apply smoothing (optional but helps) ----
x_smooth = gaussian_filter1d(x_vals, sigma=2)
y_smooth = gaussian_filter1d(y_vals, sigma=2)
z_smooth = gaussian_filter1d(z_vals, sigma=2)

# ---- Step 5: Plot all axes ----
plt.figure(figsize=(15, 6))
plt.plot(time, x_smooth, label="Accel-X", color='r', linewidth=1)
plt.plot(time, y_smooth, label="Accel-Y", color='g', linewidth=1)
plt.plot(time, z_smooth, label="Accel-Z", color='b', linewidth=1)

plt.xlabel("Time (s)")
plt.ylabel("Acceleration")
plt.title("Empatica Accelerometer Data (Smoothed)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# ---- Step 6: Show and Save ----
plt.savefig("eda_accelerometer_plot_1-1-KARTIK_1744014440.png", dpi=300)
plt.show()


