import pandas as pd
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
  """
  Calculate the haversine distance between two points on a sphere (Earth).

  Args:
    lat1: Latitude of the first point in decimal degrees.
    lon1: Longitude of the first point in decimal degrees.
    lat2: Latitude of the second point in decimal degrees.
    lon2: Longitude of the second point in decimal degrees.

  Returns:
    Distance between the two points in meters.
  """
  # Convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # Haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))
  radius_of_earth_m = 6371000  # Radius of Earth in meters
  return c * radius_of_earth_m

def calculate_speed_and_distance(filename):
  """
  Calculates the average speed and total distance traveled from a GPS data file.

  Args:
    filename: Path to the GPS data file.

  Returns:
    Tuple containing average speed (m/s) and total distance traveled (meters).
  """
  df = pd.read_csv(filename, header=None, names=["utc_time", "latitude", "longitude"])

  # Convert utc_time to datetime objects
  df['utc_time'] = pd.to_datetime(df['utc_time'])

  # Calculate distances between consecutive points
  distances = []
  for i in range(len(df) - 1):
    lat1, lon1 = df.loc[i, 'latitude'], df.loc[i, 'longitude']
    lat2, lon2 = df.loc[i + 1, 'latitude'], df.loc[i + 1, 'longitude']
    distances.append(haversine_distance(lat1, lon1, lat2, lon2))

  # Calculate time differences between consecutive points
  time_diffs = df['utc_time'].diff().iloc[1:].dt.total_seconds() 

  # Calculate speeds
  speeds = [d / t for d, t in zip(distances, time_diffs)]

  # Calculate average speed
  average_speed = sum(speeds) / len(speeds) 

  # Calculate total distance traveled
  total_distance = sum(distances)

  return average_speed, total_distance

if __name__ == "__main__":
  filename = "gps_data.txt"  # Replace with your filename
  average_speed, total_distance = calculate_speed_and_distance(filename)
  print(f"Average speed: {average_speed:.2f} m/s")
  print(f"Total distance traveled: {total_distance:.2f} meters")