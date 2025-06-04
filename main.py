#!/usr/bin/env python3

import signal
import sys

from config_manager import ConfigManager
from servo_controller import PigpioServoController
from ads_reader import ADSReader
from file_writer import FileWriter
from servo_pattern_player import ServoPatternPlayer
from logic_controller import LogicController
from rtc import RTC  # Asumiendo que tienes esta clase para la sincronización

def main():
    config = ConfigManager()
    servo = PigpioServoController(servo_pin=config.get("servo_pin", 13))
    ads_reader = ADSReader()
    rtc = RTC()
    rtc.sync_system_time()
    last_rtc_update = rtc.read_current_time()

    file_writer = FileWriter(config, last_rtc_update)
    error_patterns = config.get("error_patterns", {})
    servo_pattern_player = ServoPatternPlayer(servo, error_patterns)

    logic = LogicController(config, servo, ads_reader, file_writer, servo_pattern_player)

    # --- Manejo de señales para cerrar el programa limpiamente ---
 
    def shutdown_handler(signum, frame):
        print("Finalizando... apagando servo.")
        try:
            servo.shutdown()
        except Exception as e:
            print(f"Error al apagar el servo: {e}")
        sys.exit(0)


    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # --------------------------------------------------------------

    logic.run()

if __name__ == "__main__":
    main()