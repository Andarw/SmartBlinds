import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
import mysql.connector
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics 
import joblib

def process_input(x):
    def label_date(row):
        weekd = row['rdate'].weekday()
        return float(weekd)

    def label_hour(row):
        return float(row['rdate'].hour)
    
    def label_month(row):
        return float(row['rdate'].month)
    
    x['weekday'] = x.apply(label_date, axis=1)
    x['hour'] = x.apply(label_hour, axis=1)
    x['month'] = x.apply(label_month, axis=1)
    x = x.drop(columns = ['rdate'])

    return x
    
def get_inference_input():
    mydb = mysql.connector.connect(
        host="window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com",
        user="adminflask",
        password="bmwseria5",
        database="blind"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT temperature, humidity, light_intensity, rdate FROM sensor_data order by rdate desc limit 1")

    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns =['temperature', 'humidity', 'light_intensity','rdate'])
    df = process_input(df)

    return df


def get_data():
    mydb = mysql.connector.connect(
        host="window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com",
        user="adminflask",
        password="bmwseria5",
        database="blind"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sensor_data")

    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns =['id', 'temperature', 'humidity', 'light_intensity', 'blind_pos', 'window_pos', 'sensitivity','rdate'])
    y = df[['blind_pos', 'window_pos', 'sensitivity']]

    def label_date(row):
        weekd = row['rdate'].weekday()
        return float(weekd)

    def label_hour(row):
        return float(row['rdate'].hour)
    
    def label_month(row):
        return float(row['rdate'].month)

    df['weekday'] = df.apply(label_date, axis=1)
    df['hour'] = df.apply(label_hour, axis=1)
    df['month'] = df.apply(label_month, axis=1)
    df = df.drop(columns = ['id', 'blind_pos', 'window_pos', 'sensitivity', 'rdate'])
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=.25, random_state=42)
    y_blind_train = y_train['blind_pos']
    y_blind_test = y_test['blind_pos']
    y_window_train = y_train['window_pos']
    y_window_test = y_test['window_pos']

    return {
        'x_train': x_train,
        'x_test': x_test,
        'y_blind_train': y_blind_train,
        'y_blind_test': y_blind_test,
        'y_window_train': y_window_train,
        'y_window_test': y_window_test,
    }

def train_model(path, x_train, y_train, x_test, y_test):
    clf = RandomForestClassifier(n_estimators = 100) 
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    acc = metrics.accuracy_score(y_test, y_pred)
    print(acc)

    joblib.dump(clf, path)

blinds_path = "./blinds.joblib"
window_path = "./window.joblib"

def run_inference():
    x = get_inference_input()
    clfb = joblib.load(blinds_path)
    clfw = joblib.load(window_path)
    yb = clfb.predict(x)[0]
    yw = clfw.predict(x)[0]
    mydb = mysql.connector.connect(
        host="window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com",
        user="adminpi",
        password="bmwseria5",
        database="blind"
        )
    mycursor = mydb.cursor()
    queryb = 'UPDATE preferences SET pvalue = ' + str(yb) + ' WHERE ptype = "rec_blind_pos"'
    queryw = 'UPDATE preferences SET pvalue = ' + str(yw) + ' WHERE ptype = "rec_window_pos"'
    mycursor.execute(queryb)
    mycursor.execute(queryw)
    mydb.commit()
    print(yb, yw)

# df = get_data()
# train_model(blinds_path, df['x_train'], df['y_blind_train'], df['x_test'], df['y_blind_test'])
# train_model(window_path, df['x_train'], df['y_window_train'], df['x_test'], df['y_window_test'])
run_inference()




