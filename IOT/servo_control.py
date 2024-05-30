from gpiozero import Servo 
from time import sleep


def initialize_blinds_and_window_position_closed():
	blind = Servo(23)
	window = Servo(24)
	blind.min()
	window.min()
	sleep(0.5)
	blind.value = None
	window.value = None
	input("Initialization complete, press enter to continue...")
	

def set_bliders_position(pos):
	blind = Servo(23)
	input_table = [1,0.5,-0.5,-1] # 1 (OPEN), 0.5 (OPEN_50%), -0.5  (CLOSED_50%), -1  (CLOSED)
	blind.value = input_table[pos]
	sleep(0.5)
	blind.value = None	


def set_window_position(pos):
	window = Servo(24)
	input_table = [-1,0,1]
	window.value = input_table[pos]
	sleep(0.5)
	window.value = None	
