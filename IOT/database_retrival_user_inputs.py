import mysql.connector
from time import sleep
from servo_control import set_bliders_position,set_window_position,initialize_blinds_and_window_position_closed
import json
from light_intensity import light_intensity
from MQTT5_UPDATE import send_data_with_MQTT
import datetime

blind_mode_query = "SELECT pvalue FROM preferences where ptype = \"blind_mode\""
preferences_query = "SELECT pvalue FROM preferences where ptype != \"blind_mode\" AND ptype != \"rec_blind_pos\" AND ptype != \"rec_window_pos\""

initialize_blinds_and_window_position_closed()

blinds_position = None
window_position = None
sensitivity = None
light_int = None
first_treshold = 25
second_treshold = 50
third_treshold = 75
last_message_timestamp = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

while True:
    connection = mysql.connector.connect(
    host='window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com',
    user='adminpi',
    password='bmwseria5',
    database='blind'
    )

    if not connection.is_connected():
        print("Failed connection!!!")
        exit()
    #initialize the cursors
    blind_mode_cursor = connection.cursor()
    preferences_cursor = connection.cursor()
    
    #blind_mode retrival
    blind_mode_cursor.execute(blind_mode_query)
    blind_mode = blind_mode_cursor.fetchall()[0][0]
    
    #preferences retrival
    preferences_cursor.execute(preferences_query)
    preferences = preferences_cursor.fetchall()
    
    #print(blind_mode)
    print("preferneces", preferences)
    
    if blind_mode == 0: #manual
        print("Manual")
        if blinds_position != preferences[1][0]:
            blinds_position = preferences[1][0]
            set_bliders_position(blinds_position)

        if window_position != preferences[2][0]:
            window_position = preferences[2][0]
            set_window_position(window_position)
    else: #auto
        print("Automatic")
        #if sensitivity changed we recalculate the tresholds, the higher the sensitivity the lower the tresholds for the intensity
        if sensitivity != preferences[0][0]:
            sensitivity = preferences[0][0]
            first_treshold =  0.5 * (100-sensitivity)
            second_treshold = (100-sensitivity)
            third_treshold =  1.5 * (100-sensitivity)

        #we retrive the light intensity
        light_int = light_intensity()

        #based on the light intensity we determine the blind_position
        if light_int <= first_treshold and blinds_position != 0:
            blinds_position = 0
        elif light_int <= second_treshold and blinds_position != 1:
            blinds_position = 1
        elif light_int <= third_treshold and blinds_position != 2:
            blinds_position = 2
        elif blinds_position != 3:
            blinds_position = 3
        set_bliders_position(blinds_position)
        
    #We determine weather we need to update the sensor data in the database
    if datetime.datetime.now().replace(minute=0, second=0, microsecond=0) > last_message_timestamp:
        last_message_timestamp = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        send_data_with_MQTT()
            
    sleep(5)
    connection.close()
