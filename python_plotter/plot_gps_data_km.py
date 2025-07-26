import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define data structure for parsing lines
data = []

# Read the file line by line
with open("gps_data.txt", "r") as f:
    for line in f:
        # Split the line by spaces and convert to floats
        time_str, latitude, longitude = map(float, line.strip().split(" "))
        data.append({"utc_time": time_str, "latitude": latitude, "longitude": longitude})

# Create a DataFrame from the data list
df = pd.DataFrame(data)

# Remove entries where latitude or longitude is 0.0
df = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]

# Calculate the relative coordinates
first_latitude = df['latitude'].iloc[0]
first_longitude = df['longitude'].iloc[0]
df['x'] = -((df['longitude'] - first_longitude) * 111320)  # Approximate meters per degree of longitude
df['y'] = ((df['latitude'] - first_latitude) * 111320)  # Approximate meters per degree of latitude

# Calculate distances between consecutive points
df['distance'] = np.sqrt((df['x'].diff() ** 2) + (df['y'].diff() ** 2))

# Calculate cumulative distance
df['cumulative_distance'] = df['distance'].cumsum() / 1000  # Convert to kilometers

# Calculate time differences between consecutive points
df['time_diff'] = df['utc_time'].diff()  # Time differences in seconds

# Calculate speed per kilometer
speed_per_km = []
current_km = 1
start_idx = 0

for i, row in df.iterrows():
    if row['cumulative_distance'] >= current_km:
        # Calculate time and distance for the current kilometer
        interval_time = df['utc_time'].iloc[start_idx:i+1].diff().sum()  # Time in seconds
        speed_kmh = 3600 / interval_time if interval_time > 0 else 0  # Convert to km/h
        speed_per_km.append((current_km, speed_kmh))
        current_km += 1
        start_idx = i  # Update the start index for the next interval

# Convert speed_per_km to a DataFrame
speed_df = pd.DataFrame(speed_per_km, columns=['Kilometer', 'Speed (km/h)'])

# Calculate total distance and average speed
total_distance = df['distance'].sum()  # In meters
total_time = df['time_diff'].sum()  # Total time in seconds
average_speed = (total_distance / 1000) / (total_time / 3600) if total_time > 0 else 0  # Convert to km/h

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], marker='o', linestyle='-')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Coordinates Relative to Start')

# Add total distance, average speed, and speed per kilometer to the plot
plt.text(0.05, 0.95, 
         f"Total Distance: {total_distance/1000:.2f} km\n"
         f"Average Speed: {average_speed:.2f} km/h\n"
         f"Speed per km:\n" + "\n".join([f"Km {k}: {s:.2f} km/h" for k, s in speed_per_km[:5]]),  # Show first 5 km
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', 
         bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.grid(True)
plt.show()
