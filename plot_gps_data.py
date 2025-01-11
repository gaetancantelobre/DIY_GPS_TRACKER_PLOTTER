import pandas as pd
import matplotlib.pyplot as plt

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

# Calculate the relative coordinates 
first_latitude = df['latitude'].iloc[0]
first_longitude = df['longitude'].iloc[0]
df['x'] = (df['longitude'] - first_longitude) * 111320  # Approximate meters per degree of longitude
df['y'] = (df['latitude'] - first_latitude) * 111320  # Approximate meters per degree of latitude

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], marker='o', linestyle='-')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Coordinates Relative to Start')
plt.grid(True)
plt.show()