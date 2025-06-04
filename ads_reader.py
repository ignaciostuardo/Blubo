import logging
import sys
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ADSReader:
    """
    Lee valores analógicos desde el ADS1115.
    """
    def __init__(self, i2c_address=0x49):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS.ADS1115(i2c, address=i2c_address)
            self.channels = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2)]
        except Exception as e:
            logging.error(f"Error initializing ADS: {e}")
            sys.exit(1)
    
    def read_values(self):
        """
        Retorna (values, voltages) desde los canales del ADS1115.
        """
        values = [chan.value for chan in self.channels]
        voltages = ["%0.4f" % chan.voltage for chan in self.channels]
        return values, voltages
