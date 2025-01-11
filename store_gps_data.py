import serial
from datetime import datetime

serial_port = '/dev/ttyACM0'  # Replace with the actual serial port of your NEO-6M
baud_rate = 9600

try:
    ser = serial.Serial(serial_port, baud_rate)
except (serial.SerialException, serial.SerialTimeoutException) as e:
    print(f"Error opening serial port: {e}")
    exit()

try:
    filename = f"gps_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt" 
    with open(filename, "w") as f: 
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        data = line.split(" ") 
                        time_str = data[0]
                        latitude = float(data[1])
                        longitude = float(data[2])

                        # Write data to file
                        f.write(f"{time_str} {latitude} {longitude}\n") 
                        print(f"Logged: {time_str} {latitude} {longitude}")

                    except (ValueError, IndexError):
                        print("Error parsing data:", line)  # Print the line for debugging

            except UnicodeDecodeError:
                print("Error decoding serial data")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()