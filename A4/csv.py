import pandas as pd
from fastavro import reader
import sys

# ----- CONFIG -----
input_avro_path = '1-1-KARTIK_1744014440.avro'  # 🔁 Change to your actual file path
output_dir = './csv_outputs4/'       # Output directory

import os
os.makedirs(output_dir, exist_ok=True)

# ----- READ AVRO FILE -----
def read_avro(file_path):
    with open(file_path, 'rb') as fo:
        return list(reader(fo))

# ----- EXTRACT SENSOR DATA -----
def extract_and_save(data):
    record = data[0]  # assuming single session file

    raw = record['rawData']
    timezone_offset = record.get("timezone", 0)

    def to_df(sensor, keys=['timestampStart', 'samplingFrequency', 'values']):
        if sensor in raw and raw[sensor]:
            obj = raw[sensor]
            sf = obj['samplingFrequency']
            start = obj['timestampStart'] / 1_000_000  # µs to seconds
            values = obj['values']

            timestamps = [start + i / sf for i in range(len(values))]
            df = pd.DataFrame({'timestamp': timestamps, 'value': values})
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') + pd.to_timedelta(timezone_offset, unit='s')
            return df
        return None

    def inertial_to_df(sensor):
        if sensor in raw and raw[sensor]:
            obj = raw[sensor]
            sf = obj['samplingFrequency']
            start = obj['timestampStart'] / 1_000_000
            x, y, z = obj['x'], obj['y'], obj['z']
            timestamps = [start + i / sf for i in range(len(x))]
            df = pd.DataFrame({
                'timestamp': timestamps,
                'x': x,
                'y': y,
                'z': z
            })
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') + pd.to_timedelta(timezone_offset, unit='s')
            return df
        return None

    # Save each sensor stream to a separate CSV
    sensors = {
        'eda': to_df('eda'),
        'temperature': to_df('temperature'),
        'bvp': to_df('bvp'),
        'steps': to_df('steps'),
        'accelerometer': inertial_to_df('accelerometer'),
        'gyroscope': inertial_to_df('gyroscope')
    }

    for name, df in sensors.items():
        if df is not None:
            df.to_csv(f"{output_dir}{name}.csv", index=False)
            print(f"[✓] Saved {name}.csv")

    # Special case for tags and peaks
    if 'tags' in raw and raw['tags']:
        tag_times = raw['tags']['tagsTimeMicros']
        tag_df = pd.DataFrame({
            'timestamp': [pd.to_datetime(t / 1_000_000, unit='s') + pd.to_timedelta(timezone_offset, unit='s') for t in tag_times]
        })
        tag_df.to_csv(f"{output_dir}tags.csv", index=False)
        print("[✓] Saved tags.csv")

    if 'systolicPeaks' in raw and raw['systolicPeaks']:
        peak_times = raw['systolicPeaks']['peaksTimeNanos']
        peak_df = pd.DataFrame({
            'timestamp': [pd.to_datetime(t / 1_000_000_000, unit='s') + pd.to_timedelta(timezone_offset, unit='s') for t in peak_times]
        })
        peak_df.to_csv(f"{output_dir}systolic_peaks.csv", index=False)
        print("[✓] Saved systolic_peaks.csv")


# ----- RUN -----
if __name__ == "__main__":
    try:
        avro_data = read_avro(input_avro_path)
        extract_and_save(avro_data)
        print("\n[✓] All data successfully converted to CSV!")
    except Exception as e:
        print(f"[✗] Error: {e}")
