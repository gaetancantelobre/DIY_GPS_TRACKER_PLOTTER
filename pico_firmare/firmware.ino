#include <Adafruit_SSD1306.h>
#include "bitmaps.h"
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 64, &Wire);
#define GPS_SERIAL Serial1
int numSatellites = 0;
float latitude = 0;
float longitude = 0;
String timeStr;
const int potPin = 26;
const int chipSelect = 10;

String currentTime ="";

String latitudeStr ="";
String latitudeDir ="";
String longitudeStr ="";
String longitudeDir ="";

#define prt(x) Serial.println(x)

void setupGNSS()
{
  GPS_SERIAL.begin(9600);
}

void setupOLED()
{
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  display.clearDisplay();
  display.drawBitmap(0, 0, epd_bitmap_test, 128, 64, WHITE); // Draw the bitmap
  display.display();
  delay(1000);
  display.clearDisplay();
  display.display();
}

float convertToDecimalDegrees(String degreesMinutesStr, String direction) {
  int degrees = degreesMinutesStr.substring(0, 2).toInt();
  float minutes = degreesMinutesStr.substring(2).toFloat();
  float decimalDegrees = degrees + minutes / 60.0;

  if (direction == "S" || direction == "W") {
    decimalDegrees *= -1;
  }

  return decimalDegrees;
}

void updatePrtGNSS()
{
  if (GPS_SERIAL.available() > 0) {
    // Read a line of gpsData from the GPS module
    String gpsData = GPS_SERIAL.readStringUntil('\n');

    if (gpsData.startsWith("$GPGSV")) {
      // Parse the $GPGSV sentence
      numSatellites = gpsData.substring(7, 9).toInt();
    }

    if(numSatellites >= 3)
    {
      if (gpsData.startsWith("$GPGGA")) { 
      int commaIndex1 = gpsData.indexOf(',');
      int commaIndex2 = gpsData.indexOf(',', commaIndex1 + 1);
      int commaIndex3 = gpsData.indexOf(',', commaIndex2 + 1);
      int commaIndex4 = gpsData.indexOf(',', commaIndex3 + 1);
      int commaIndex5 = gpsData.indexOf(',', commaIndex4 + 1);

      latitudeStr = gpsData.substring(commaIndex2 + 1, commaIndex3);
      longitudeStr = gpsData.substring(commaIndex4 + 1, commaIndex5);

      // Extract time from GPGGA sentence (assuming format: HHMMSS.sss)
      timeStr = gpsData.substring(commaIndex1 + 1, commaIndex1 + 7); 

      // Convert latitude to decimal degrees
      char latHemisphere = latitudeStr.charAt(latitudeStr.length() - 1);
      double latDegrees = latitudeStr.substring(0, 2).toDouble();
      double latMinutes = latitudeStr.substring(2).toDouble() / 60;
      double latitudeDecimal = latDegrees + latMinutes;
      if (latHemisphere == 'S') {
        latitudeDecimal = -latitudeDecimal;
      }

      // Convert longitude to decimal degrees
      char lonHemisphere = longitudeStr.charAt(longitudeStr.length() - 1);
      double lonDegrees = longitudeStr.substring(0, 3).toDouble();
      double lonMinutes = longitudeStr.substring(3).toDouble() / 60;
      double longitudeDecimal = lonDegrees + lonMinutes;
      if (lonHemisphere == 'W') {
        longitudeDecimal = -longitudeDecimal;
      }

      latitudeStr = String(latitudeDecimal, 6);
      longitudeStr = String(longitudeDecimal, 6);

      // Send data to Serial Monitor
      Serial.print(timeStr); 
      Serial.print(" ");
      Serial.print(latitudeStr); // Print latitude with 6 decimal places
      Serial.print(" ");
      Serial.println(longitudeStr); // Print longitude with 6 decimal places 

    }
    // uncomment to get position on google maps
    // Serial.print("https://www.google.com/maps/place/");
    // Serial.print(latitude, 6);
    // Serial.print(",");
    // Serial.print(longitude, 6);
    // Serial.println("");
    }
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.print("Satellites: ");
  display.println(numSatellites);
    if(numSatellites >= 3)
  {
    display.setCursor(0, 20);
    display.print("Latitude: ");
    display.println(latitudeStr);
    display.setCursor(0, 30);
    display.print("Longitude: ");
    display.println(longitudeStr);
    display.setCursor(0, 40);
    display.println(timeStr);
  }
  display.display();
}

void mapTo12Bit(float value) {
  // 12-bit resolution provides 4096 possible values (2^12)
  uint16_t max_value = 4095; 

  // Scale the input value to the 12-bit range
  uint16_t mapped_value = (uint16_t)(value * 5.0 / max_value); 
  display.setCursor(0, 40);
  display.print(mapped_value);
  display.setCursor(0, 60);
  display.print(value);
  display.display();
}

void setup() {
  setupOLED();
  setupGNSS();
  analogReadResolution(24);
  Serial.begin(115200);
}

void loop() {
  updatePrtGNSS();
 }