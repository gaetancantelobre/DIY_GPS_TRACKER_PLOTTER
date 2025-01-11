import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = []

with open("gps_data.txt", "r") as f:
    for line in f:
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

# Calculate total distance
total_distance = df['distance'].sum()  # In meters

# Calculate time differences between consecutive points
df['time_diff'] = df['utc_time'].diff()  # Time differences in seconds

# Calculate average speed (meters per second)
total_time = df['time_diff'].sum()  # Total time in seconds
average_speed = total_distance / total_time if total_time > 0 else 0  # Avoid division by zero

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], marker='o', linestyle='-')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Coordinates Relative to Start')

# Add total distance and average speed to the plot
plt.text(0.05, 0.95, f"Total Distance: {total_distance:.2f} m\nAverage Speed: {average_speed:.2f} m/s",
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.grid(True)
plt.show()
