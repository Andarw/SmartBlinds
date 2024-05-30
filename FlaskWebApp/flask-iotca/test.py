import random
import datetime

# Function to generate a realistic temperature value
def generate_temperature(hour):
    if 6 <= hour <= 18:  # Daytime temperature
        return round(random.uniform(20.0, 35.0), 1)
    else:  # Nighttime temperature
        return round(random.uniform(15.0, 25.0), 1)

# Function to generate a realistic humidity value
def generate_humidity():
    return round(random.uniform(40.0, 80.0), 1)

# Function to generate a realistic light intensity value
def generate_light_intensity(hour):
    if 6 <= hour <= 18:  # Daytime light intensity
        return round(random.uniform(50.0, 100.0), 1)
    else:  # Nighttime light intensity
        return round(random.uniform(0.0, 20.0), 1)

# Function to generate a realistic blind position based on light intensity
def generate_blind_pos(light_intensity):
    if light_intensity > 80:
        return 3  # Closed blinds
    elif light_intensity > 60:
        return 2  # Mostly closed
    elif light_intensity > 30:
        return 1  # Semi-open
    else:
        return 0  # Open blinds

# Function to generate a realistic window position based on temperature
def generate_window_pos(temperature):
    if temperature > 30:
        return 2  # Open window
    elif temperature > 20:
        return 1  # Semi-open
    else:
        return 0  # Closed window

# Function to generate a sensitivity value
def generate_sensitivity():
    return random.randint(0, 100)

# Generate insert statements for the past week
base_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
delta = datetime.timedelta(hours=1)

# List to hold the generated SQL statements
sql_statements = []

id = 168
for day in range(7):
    for hour in range(24, 0, -1):
        current_time = base_time - datetime.timedelta(days=day) + datetime.timedelta(hours=hour)
        temperature = generate_temperature(current_time.hour)
        humidity = generate_humidity()
        light_intensity = generate_light_intensity(current_time.hour)
        blind_pos = generate_blind_pos(light_intensity)
        window_pos = generate_window_pos(temperature)
        sensitivity = generate_sensitivity()
        rdate = current_time.strftime("%Y-%m-%d %H:%M:%S")

        sql_statement = f"INSERT INTO sensor_data (id, temperature, humidity, light_intensity, blind_pos, window_pos, sensitivity, rdate) VALUES ({id}, {temperature}, {humidity}, {light_intensity}, {blind_pos}, {window_pos}, {sensitivity}, '{rdate}');"
        sql_statements.append(sql_statement)
        id -= 1

# Print the generated SQL statements
for statement in sql_statements:
    print(statement)

print(len(sql_statements))
