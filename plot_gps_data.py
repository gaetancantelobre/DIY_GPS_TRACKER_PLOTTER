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
total_distance = df['distance'].sum()  # In meters


df['time_diff'] = df['utc_time'].diff()
total_time = df['time_diff'].sum()  
average_speed = total_distance / total_time if total_time > 0 else 0
df['normalized_time'] = (df['utc_time'] - df['utc_time'].min()) / (df['utc_time'].max() - df['utc_time'].min())

# Plotting
plt.figure(figsize=(10, 6))

# Use a colormap to color lines based on normalized time
norm = plt.Normalize(df['normalized_time'].min(), df['normalized_time'].max())
cmap = plt.get_cmap('viridis')

for i in range(len(df) - 1):
    plt.plot(df['x'].iloc[i:i+2], df['y'].iloc[i:i+2], color=cmap(norm(df['normalized_time'].iloc[i])), linewidth=2)

# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical')
cbar.set_label('Normalized Time (Older to Newer)', fontsize=10)

# Add labels and title
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Coordinates Relative to Start')

# Convert total time to a readable format (hours, minutes, seconds)
hours = int(total_time // 3600)
minutes = int((total_time % 3600) // 60)
seconds = int(total_time % 60)
formatted_time = f"{hours}h {minutes}m {seconds}s"

# Add total distance, average speed, and total time to the plot
plt.text(0.05, 0.95, f"Total Distance: {total_distance:.2f} m\n"
                     f"Average Speed: {average_speed:.2f} m/s\n"
                     f"Total Time: {formatted_time}",
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', 
         bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))



plt.grid(True)
plt.show()
