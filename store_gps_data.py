import serial
from datetime import datetime
import paho.mqtt.client as mqtt
import time

# Serial port configuration
serial_port = '/dev/ttyACM0'  # Replace with the actual serial port of your NEO-6M
baud_rate = 9600

# MQTT configuration
mqtt_topic = "gps/status"  # Topic to publish status
mqtt_client_id = "gps_logger"  # Unique client ID


unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.user_data_set(unacked_publish)
mqttc.connect("129.151.251.252",27050)
mqttc.loop_start()

# Our application produce some messages
msg_info = mqttc.publish(mqtt_topic, "100", qos=1)
unacked_publish.add(msg_info.mid)

try:
    ser = serial.Serial(serial_port, baud_rate)
except (serial.SerialException, serial.SerialTimeoutException) as e:
    print(f"Error opening serial port: {e}")
    mqttc.publish(mqtt_topic, "false", retain=True)  # Publish "false" if serial port fails
    exit()

try:
    filename = f"gps_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt" 
    with open(filename, "w") as f:
        mqttc.publish(mqtt_topic, "true", retain=True)  # Publish "true" when logging starts
        print("Started logging GPS data...")
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
    mqttc.publish(mqtt_topic, "false", retain=True)  # Publish "false" when exiting
    ser.close()
    mqttc.disconnect()
