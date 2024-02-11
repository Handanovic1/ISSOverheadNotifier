import requests
import datetime as dt
import smtplib
import time

MYLAT = 38.846756
MYLONG = -77.445335

def isNight():
    parameters = {
    'lat': MYLAT,
    'lng': MYLONG,
    'formatted': 0
    }
    response = requests.get(url = 'https://api.sunrisesunset.io/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data['results']['sunrise'].split(':')[0]
    sunset = str(int(data['results']['sunset'].split(':')[0]) + 12)
    myHour = dt.datetime.now().hour
    if sunset < myHour > sunrise:
        return True

def isOverhead():
    issLocation = requests.get(url="http://api.open-notify.org/iss-now.json")
    issLocation.raise_for_status()
    issData = issLocation.json()

    iss_latitude = float(issData["iss_position"]["latitude"])
    iss_longitude = float(issData["iss_position"]["longitude"])
    if (iss_latitude-5 <= MYLAT <= iss_latitude+5) and (iss_longitude-5 <= MYLONG <= iss_longitude+5):
         return True

while True:
    time.sleep(60)
    if isOverhead() and isNight(): 
        myEmail = 'exampleFrom@gmail.com'
        myPassword = 'examplePassword'
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=myEmail, password=myPassword)
        connection.sendmail(from_addr=myEmail, to_addrs='exampleTo@gmail.com', msg='Subject: Look Up!\n\nThe International Space Station is above you and visible')
