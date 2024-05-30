from flask import Flask, render_template
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import ai_model
import seaborn as sns

application = Flask(__name__)

def get_data_lw():
    mydb = mysql.connector.connect(
        host="window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com",
        user="adminflask",
        password="bmwseria5",
        database="blind"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT temperature, humidity, light_intensity, rdate FROM sensor_data limit 24")

    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns =['temperature', 'humidity', 'light_intensity', 'rdate'])
    return df

def get_data():
    mydb = mysql.connector.connect(
        host="window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com",
        user="adminflask",
        password="bmwseria5",
        database="blind"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT temperature, humidity, light_intensity, rdate FROM sensor_data")

    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns =['temperature', 'humidity', 'light_intensity', 'rdate'])
    return df
    

@application.route('/')
def index():
    df = get_data()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='temperature', label='T in C degrees', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title('Weekly Temperature')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode()


    df = get_data_lw()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='temperature', label='T in C degrees', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title('Daily Temperature')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url1=plot_url1, plot_url2=plot_url2)

@application.route('/ai', methods=['GET'])
def inference():
    ai_model.run_inference()
    return "Inference was executed succesfully!"


@application.route('/bar')
def bar_chart():
    df = get_data()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='humidity', label='Humidity in %', color='green')
    plt.xlabel('Date')
    plt.ylabel('Humidity')
    plt.title('Weekly Humidity')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode()


    df = get_data_lw()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='humidity', label='Humidity in %', color='green')
    plt.xlabel('Date')
    plt.ylabel('Humidity')
    plt.title('Daily Humidity')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode()

    return render_template('bar.html', plot_url1=plot_url1, plot_url2=plot_url2)

@application.route('/int')
def int_chart():
    df = get_data()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='light_intensity', label='Intensity in %', color='red')
    plt.xlabel('Date')
    plt.ylabel('Light Intensity')
    plt.title('Weekly Light Intensity')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode()


    df = get_data_lw()
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.lineplot(data=df, x='rdate', y='light_intensity', label='Intensity in %', color='red')
    plt.xlabel('Date')
    plt.ylabel('Light Intensity')
    plt.title('Daily Light Intensity')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode()

    return render_template('int.html', plot_url1=plot_url1, plot_url2=plot_url2)

if __name__ == '__main__':
    application.run(host='192.168.56.1', debug=True)
