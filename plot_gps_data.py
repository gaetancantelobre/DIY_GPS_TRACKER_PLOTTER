import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("gps_data.txt", header=None, names=["utc_time", "latitude", "longitude"])

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