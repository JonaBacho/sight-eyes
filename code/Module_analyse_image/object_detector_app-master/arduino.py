import serial
import time

class ArduinoCommunication:
    def __init__(self, port, baudrate):
        try:
            self.serial_conn = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Délai pour établir la connexion
        except serial.SerialException as e:
            raise RuntimeError(f"Erreur de connexion avec Arduino : {e}")

    def send_data(self, horizontal_angle, vertical_angle, speed, is_close=False, rotate=False, obstacle=False):
        """Envoie les données à l'Arduino."""
        try:
            data = f"{horizontal_angle},{vertical_angle},{speed},{int(is_close)}, {int(rotate)}, {int(obstacle)}\n"
            self.serial_conn.write(data.encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")

    def receive_distance(self):
        """Reçoit la distance depuis l'Arduino."""
        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode().strip()
                return float(line)
        except ValueError:
            print("Erreur de format dans les données reçues.")
        except Exception as e:
            print(f"Erreur lors de la réception des données : {e}")
        return float('inf')  # Retourne une grande valeur si aucune donnée
