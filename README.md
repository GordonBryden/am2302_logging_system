# am2302_logging_system

pip3 install adafruit-circuitpython-dht

sudo apt-get install libgpiod2
sudo apt-get install sqlite3
import board
import adafruit_dht

#apt-get instead of pip to avoid hanging on install
sudo apt-get install python3-matplotlib 

#To do

sqlite3 sensor_data.db

CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL
);

@reboot sleep 30 && /usr/bin/python3 /path/to/data_logger.py
@reboot sleep 60 && /usr/bin/python3 /path/to/app.py
