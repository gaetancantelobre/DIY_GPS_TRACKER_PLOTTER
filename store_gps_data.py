import serial
import time
import pynmea2
from datetime import datetime

serial_port = '/dev/ttyUSB0'  # Replace with the actual serial port of your NEO-6M
baud_rate = 9600

# Open the serial port
try:
    ser = serial.Serial(serial_port, baud_rate)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

try:
    # Get current date and time for filename
    now = datetime.now()
    filename = f"gps_data_{now:%Y%m%d_%H%M%S}.txt" 

    with open(filename, "a") as f:
        while True:
            try:
                data = ser.readline().decode('utf-8')  # Read a line from the serial port

                # Parse the NMEA sentence (assuming it's a GPGGA sentence)
                msg = pynmea2.parse(data)

                # If we get the coordinates
                if msg.msgID == 'GPGGA' and msg.gps_qual > 0:
                    # Convert the time in message to object
                    utc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(msg.utc_time))
                    latitude = msg.latitude
                    longitude = msg.longitude

                    # Write data to file
                    f.write(f"{utc_time},{latitude},{longitude}\n")
                    print(f"Logged: {utc_time}, Lat: {latitude}, Lon: {longitude}")

            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")

except IOError as e:
    print(f"Error writing to file: {e}")

finally:
    ser.close()