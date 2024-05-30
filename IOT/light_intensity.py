import serial
import struct
from time import sleep


def light_intensity(): # returns a value between 0 100 which represents the % light intensity, calculated with the value of the vlotage read and the max vlotage produced by the solar panel
	arduino_serial = serial.Serial("/dev/ttyUSB0",9600)
	arduino_serial.baudrate=9600
	read_arduino_value = arduino_serial.read(4)
	read_arduino_value = read_arduino_value.decode('utf-8')
	read_arduino_value = float(read_arduino_value)
	light = read_arduino_value / 5.5 * 100
	light = round(light,1)
	return light
