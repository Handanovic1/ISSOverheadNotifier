import requests
import datetime as dt
import smtplib
import time

# My position
MYLAT = 38.846756
MYLONG = -77.445335

# Parameters for the API
parameters = {
    'lat': MYLAT,
    'lng': MYLONG,
    'formatted': 0
}

# Getting data from API for the sunrise and sunset at my timezone
response = requests.get(url = 'https://api.sunrisesunset.io/json', params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data['results']['sunrise'].split(':')[0]
sunset = str(int(data['results']['sunset'].split(':')[0]) + 12)

# Getting data from API for ISS position
issLocation = requests.get(url="http://api.open-notify.org/iss-now.json")
issLocation.raise_for_status()
issData = issLocation.json()
iss_latitude = float(issData["iss_position"]["latitude"])
iss_longitude = float(issData["iss_position"]["longitude"])

# My Current Hour
myHour = dt.datetime.now().hour

# To be able to infinitely run the program
x = True
while x:
    time.sleep(60)
    #Your position is within +5 or -5 degrees of the ISS position.
    if (iss_latitude-5 <= MYLAT <= iss_latitude+5) and (iss_longitude-5 <= MYLONG <= iss_longitude+5):
        if sunset < myHour > sunrise:
            myEmail = 'exampleFrom@gmail.com'
            myPassword = 'examplePassword'
            connection = smtplib.SMTP('smtp.gmail.com')
            connection.starttls()
            connection.login(user=myEmail, password=myPassword)
            connection.sendmail(from_addr=myEmail, to_addrs='exampleTo@gmail.com', msg='Subject: Look Up!\n\nThe International Space Station is above you and visible')
