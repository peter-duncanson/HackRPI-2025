import serial
import time

ser = serial.Serial("COM5", 9600, timeout = 1)

time.sleep(2)
data = ""
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            print(f"Recieved from Arduino: {line}")
            data = line
except KeyboardInterrupt:
    print("Exiting Program")
finally:
    ser.close()

print("")
print("")
print("Morse code collected: ")
print(line)