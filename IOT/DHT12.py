import sys
import smbus
import time

i2c_bus = smbus.SMBus(1)
DHT12_sensor_address = int(0x5c)

###This function returns temperature and humidity read from DHT12 sensor with the help of I2C interface 
def read_dht12():
	offset = 0x00 # read from offset 0
	number_of_bytes_read = 5 # number of read bytes
	result = i2c_bus.read_i2c_block_data(DHT12_sensor_address,offset, number_of_bytes_read)
	if(result[0] + result[1] + result[2] + result[3] == result[4]):
		print("Checksum is correct!(Temperature collected)")
		#print("Humidity: ", str(result[0]) + "." + str(result[1]) + "%")
		#print("Temperature: ", str(result[2]) + "." + str(result[3]) + "C")
		temperature = float(result[2]) + (float(result[3])/10)
		#print(temperature)
		humidity = float(result[0]) + float(result[1]/10)
		#print(humidity)
		return temperature, humidity
	else:
		print("Checksum is incorect!(Problem with DHT12!!!)")
		return None, None
