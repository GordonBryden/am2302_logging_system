import time
import sqlite3
import Adafruit_DHT

# DHT22 sensor setup
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Database setup
DB_FILE = 'sensor_data.db'

def log_sensor_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    while True:
        try:
        # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            if humidity is not None and temperature is not None:
                cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
                conn.commit()
                print(f"Temperature: {temperature}°C, Humidity: {humidity}% recorded.")
                time.sleep(60)
        except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
            time.sleep(60)
        

if __name__ == '__main__':
    log_sensor_data()
