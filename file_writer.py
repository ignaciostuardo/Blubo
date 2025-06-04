import os
import sys
import time
from datetime import datetime
import socket

class FileWriter:
    def __init__(self, config, last_rtc_update):
        hostname = socket.gethostname()
        instrument_id = ''.join(filter(str.isdigit, hostname))
        if not instrument_id:
            instrument_id = "Unknown"

        device_type = "blubo"
        data_supplier = config.get("data_supplier", "")
        location_name = config.get("location_name", "")
        position = config.get("position", "")

        self.header_info = f"""
#HEADER
# Device type: {device_type}
# Instrument ID: {instrument_id}
# Data supplier: {data_supplier}
# Location name: {location_name}
# Position: {position}
# Local timezone: UTC
# Time Synchronization: Last RTC Update: {last_rtc_update}
# Moving / Stationary position: STATIONARY
# Moving / Fixed look direction: FIXED
# Number of channels: 3
# Filters per channel: 1
# Measurement direction per channel:
# Field of view:
# Number of fields per line:
# Device specific characteristics:
# UTC Date & Time, Local Date & Time, R, G, B meanADU
# YYYY-MM-DDTHH:mm:ss.fff;YYYY-M
# END OF HEADER"""

        # Obtener el home del usuario actual
        home_dir = os.path.expanduser('~')
        base_dir = os.path.join(home_dir, "blubo", "data")
        os.makedirs(base_dir, exist_ok=True)

        date_str = datetime.utcnow().strftime("%Y%m%d")
        base_filename = f"{date_str}_BLUBO{instrument_id}.txt"
        file_path = os.path.join(base_dir, base_filename)

        count = 1
        while os.path.exists(file_path):
            file_path = os.path.join(base_dir, f"{date_str}_{count}_BLUBO{instrument_id}.txt")
            count += 1

        self.filename = file_path

        try:
            with open(self.filename, 'w') as f:
                f.write(self.header_info + "\n")
        except Exception as e:
            print(f"Error initializing file: {e}")
            sys.exit(1)

    def write_data(self, timestamp, values):
        utc_formato = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        local_formato = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        with open(self.filename, 'a') as f:
            f.write(utc_formato + ";" + local_formato + ";" + ";".join(map(str, values)) + "\n")