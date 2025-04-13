import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Config ---
folders = ['csv_outputs1', 'csv_outputs2', 'csv_outputs3', 'csv_outputs4']
plt.ioff()

# --- Loop through all specified folders ---
for folder in folders:
    outfolder = os.path.join(folder, folder.replace("csv_outputs", "plot"))
    os.makedirs(outfolder, exist_ok=True)

    for file in os.listdir(folder):
        if file.endswith('.csv'):
            path = os.path.join(folder, file)
            name = file.replace('.csv', '')

            df = pd.read_csv(path)

            if 'timestamp' not in df.columns:
                print(f"[!] Skipping {file} in {folder} (no timestamp)")
                continue

            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # --- Plot ---
            plt.figure(figsize=(12, 4))
            for col in df.columns:
                if col != 'timestamp':
                    plt.plot(df['timestamp'], df[col], label=col)

            plt.xlabel('Time (HH:MM:SS)')
            plt.ylabel('Value')
            plt.title(f"{name} ({folder})")
            plt.legend()

            # ✅ Set exactly 20 ticks with HH:MM:SS format
            total_len = len(df)
            step = max(1, total_len // 20)
            tick_locs = df['timestamp'][::step]

            ax = plt.gca()
            ax.set_xticks(tick_locs)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

            plt.xticks(rotation=45)
            plt.tight_layout()

            # --- Save ---
            outfile = os.path.join(outfolder, f"{name}.png")
            plt.savefig(outfile)
            plt.close()
            print(f"[✓] Saved: {outfile}")
