import subprocess
import logging

class RTC:
    def __init__(self):
        # Puedes agregar inicializaciones si lo requieres
        pass

    def sync_system_time(self):
        """
        Sincroniza la hora del sistema con la hora del RTC DS1307.
        """
        try:
            # hwclock -s (o --hctosys) lee la hora del RTC y la establece en el sistema
            subprocess.run(["sudo", "hwclock", "-s"], check=True)
            logging.info("La hora del sistema se sincronizó con el RTC correctamente.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al sincronizar la hora del RTC: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al sincronizar la hora del RTC: {e}")
            
    def set_rtc_time_from_system(self):
        try:
            subprocess.run(["sudo", "hwclock", "-w"], check=True)
            logging.info("Hora del sistema escrita en el RTC.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al escribir la hora en el RTC: {e}")

    def read_current_time(self):
        """
        Lee la hora actual directamente del RTC (opcional). 
        Esto se puede hacer con 'hwclock -r'.
        """
        try:
            result = subprocess.run(["sudo", "hwclock", "-r"], capture_output=True, text=True, check=True)
            logging.info(f"Hora actual del RTC: {result.stdout.strip()}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al leer la hora del RTC: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al leer la hora del RTC: {e}")
        return None