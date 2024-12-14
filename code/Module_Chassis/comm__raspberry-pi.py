import serial
import sys
import time

# Serial Port and Speed Settings
serial_port = '/dev/ttyUSB0'  # Port connected to Arduino
baud_rate = 9600

try:
    # Serial Port Initialization
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

# Function to send data to Arduino
def send_data(speed, angle, active):
    # Format: speed,angle,boolean
    data_string = f"{speed},{angle},{1 if active else 0}\n"
    try:
        ser.write(data_string.encode())
        print(f"Sent: {data_string.strip()}")
    except Exception as e:
        print(f"Error sending data: {e}")

# Main execution
if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python send_data.py <speed> <angle> <active>")
        print("Example: python send_data.py 50 90 1")
        sys.exit(1)
    
    try:
        # Parse command-line arguments
        speed = int(sys.argv[1])
        angle = int(sys.argv[2])
        active = bool(int(sys.argv[3]))
        
        # Send data to Arduino
        while True:
            # Envoi des données toutes les 1 secondes
            # Vous pouvez modifier ces valeurs à chaque itération si nécessaire
            send_data(speed, angle, True)
            time.sleep(1)  # Pause de 1 seconde
            
            
    except ValueError:
        print("Error: Arguments must be integers")
        print("Usage: python send_data.py <speed> <angle> <active>")
        sys.exit(1)
    finally:
        # Close the serial connection
        ser.close()
