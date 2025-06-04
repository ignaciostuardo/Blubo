import time

class ServoPatternPlayer:
    """
    Ejecuta patrones de movimiento en el servo, según un diccionario de patrones.
    Cada patrón es una lista de (angulo, duracion).
    """
    def __init__(self, servo_controller, patterns):
        self.servo = servo_controller
        self.patterns = patterns

    def play(self, pattern_name):
        if pattern_name not in self.patterns:
            print(f"Patrón {pattern_name} no encontrado.")
            return
        for angle, delay in self.patterns[pattern_name]:
            self.servo.set_servo_angle(angle)
            time.sleep(delay)
        # Al finalizar podría volver a una posición neutra si se desea
        self.servo.set_servo_angle(0)
