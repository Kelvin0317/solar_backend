from flask import Flask
from flask_cors import CORS, cross_origin

import json
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

mydb = mysql.connector.connect(
    host='sql6.freemysqlhosting.net',
    port='3306',
    username='sql6471154',
    password='85vc3m4TgB',
    database='sql6471154'
)

cursor = mydb.cursor()
selectquery = "select * from energy_consumption"
cursor.execute(selectquery)
records = cursor.fetchall()

x = 1
i = 0

# ------------------------------------------ Days ---------------------------------------------------------
#
Days_Data = []
Day = []
pv_Data = []
im_Data = []
ex_Data = []
t_Data = []
d = []
a = 0
Time = []
i = 1

for row in records:
    Day.append(row[0])
    Time.append(row[1])
    pv_Data.append(row[2])
    im_Data.append(row[3])
    ex_Data.append(row[4])
    t_Data.append(row[5])
    d.append(a)
    if i == 48:
        a += 1
        i = 0
    i = i + 1

Days_Data.append(Day)
Days_Data.append(Time)
Days_Data.append(pv_Data)
Days_Data.append(im_Data)
Days_Data.append(ex_Data)
Days_Data.append(t_Data)
Days_Data.append(d)

# print(d)


# ------------------------------------------ Weeks ---------------------------------------------------------
Weeks_Data = []
WeeksData = ["Wednesday", "Thursday", "Friday", "Saturdays", "Sunday", "Monday", "Tuesday"]
pv_Data = []
im_Data = []
Weeks = []
WeeksNum = []
d = 0
i = 1
pv = 0
im = 0
n = 0

for row in records:
    pv += row[2]
    im += row[3]
    if i == 48:
        pv_Data.append(pv)ci
        im_Data.append(im)
        Weeks.append(WeeksData[d])
        pv = 0
        im = 0
        i = 0
        d += 1
    i = i + 1

    if d == 7:
        d = 0

for row in records:
    if row == "Monday":
        n += 1
    WeeksNum.append(n)

Weeks_Data.append(pv_Data)
Weeks_Data.append(im_Data)
Weeks_Data.append(Weeks)
Weeks_Data.append(WeeksNum)

print(Weeks_Data)

# ------------------------------------------ Month - Total ---------------------------------------------------------

pvim_Data = []
pv_Data = []
im_Data = []
TP_Data = []
ex_Data = []
Days = []
d = 1
i = 1
pv = 0
im = 0
tp = 0
ex = 0

for row in records:
    pv += row[2]
    im += row[3]
    tp += row[5]
    ex += row[4]
    if i == 48:
        pv_Data.append(pv)
        im_Data.append(im)
        TP_Data.append(tp)
        ex_Data.append(ex)
        Days.append(str("Day") + str(d))
        pv = 0
        im = 0
        tp = 0
        ex = 0
        i = 0
        d += 1
    i = i + 1

pvim_Data.append(pv_Data)
pvim_Data.append(im_Data)
pvim_Data.append(TP_Data)
pvim_Data.append(Days)
pvim_Data.append(ex_Data)



app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home_page():
    data = Days_Data;
    json_dump = json.dumps(data)
    return json_dump

@app.route('/full', methods=['GET'])
def e_page():
    data = pvim_Data;
    json_dump = json.dumps(data)
    return json_dump

@app.route('/week', methods=['GET'])
def w_page():
    data = Weeks_Data;
    json_dump = json.dumps(data)
    return json_dump

if __name__ == '__main__':
    app.run(debug=True)

