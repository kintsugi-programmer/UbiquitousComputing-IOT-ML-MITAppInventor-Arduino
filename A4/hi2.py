import pandas as pd
from fastavro import reader

# Update this path to your actual AVRO file location
file_path = "1-1-KARTIK_1744010889.avro"

# Read the AVRO file
with open(file_path, 'rb') as f:
    avro_reader = reader(f)
    records = list(avro_reader)

# Convert to DataFrame
df = pd.DataFrame(records)

# Save to CSV
df.to_csv("converted_output.csv", index=False)
print("Converted to CSV successfully!")
