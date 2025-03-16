import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Define file mappings and labels
file_labels = {
    "1.txt": "Too_Close_Alert",
    "2.txt": "Move_Right",
    "3.txt": "Move_Left",
    "4.txt": "Grey_Object"
}

# Function to parse data from the given format
def parse_file(filename, label):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):  # Every 2 lines make one record
            distance_light = lines[i].strip().split(', ')
            motion_data = lines[i+1].strip().split(', ')
            
            distance = float(distance_light[0].split(': ')[1])
            light = float(distance_light[1].split(': ')[1])
            ax = float(motion_data[1].split(': ')[1])
            ay = float(motion_data[2].split(': ')[1])
            az = float(motion_data[3].split(': ')[1])
            
            data.append([distance, light, ax, ay, az, label])
    
    return data

# Load and parse all files
dataset = []
for file, label in file_labels.items():
    dataset.extend(parse_file(file, label))

# Convert to DataFrame
df = pd.DataFrame(dataset, columns=["Distance", "Light", "AX", "AY", "AZ", "Label"])

# Encode labels
label_mapping = {label: idx for idx, label in enumerate(file_labels.values())}
df['Label'] = df['Label'].map(label_mapping)

# Split data
X = df.drop("Label", axis=1)
y = df["Label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and scaler using joblib
joblib.dump(model, "final_model.joblib")
joblib.dump(scaler, "scaler.joblib")
joblib.dump(label_mapping, "label_mapping.joblib")

print("Model trained and saved as final_model.joblib")