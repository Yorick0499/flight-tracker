import requests
import json
import time
import math
import matplotlib.pyplot as plt

localization = "CITY_NAME"
loc_latitude = "CITY_LATITUDE"
loc_longitude = "CITY_LONGITUDE"
distance = 50
radians_latitude = math.radians(52.409538)
longitude_formula = distance / (111.320 * math.cos(radians_latitude))
latitude_formula = distance / 111.320

my_latitude = "YOUR_LATITUDE"
my_longitude = "YOUR_LONGITUDE"



time.sleep(10)
params = {
    "lamin": round(loc_latitude - latitude_formula,3),
    "lamax": round(loc_latitude + latitude_formula,3),
    "lomin": round(loc_longitude - longitude_formula,3),
    "lomax": round(loc_longitude + longitude_formula,3)
}

x_points = [0]
y_points = [0]

response = requests.get("https://opensky-network.org/api/states/all",params=params)
data = response.json()
if data['states'] != None:
    for i in data['states']:
        how_far_long = math.sqrt(abs(int((my_longitude-i[5])*(111.320*math.cos(radians_latitude))))**2 + abs(int((my_latitude-i[6])*111.320))**2)
        print(f"Identyfikator samolotu: {i[0]}\nZnak wywoławczy: {i[1]}\nKraj samolotu: {i[2]}\nDługość geograficzna: {i[5]}\nSzerokość geograficzna: {i[6]}\nWysokość: {"0" if i[13] == None else i[13]} m\nNa ziemi?: {"Nie" if i[8]==False else "Tak"}\nPrędkość: {round(((int(i[9])*3600)/1000),2)} km/h\nPrędkość pionowa: {"0" if i[11]==None else round((int(i[11])*3600)/1000,2)} km/h\nKurs: {i[10]}°\nWznosi się/Opada: {"-" if i[11]==None else "Opada" if i[11] < 0 else "Wznosi się" if i[11] > 0 else "-"}\nJak daleko od mojej lokalizacji: ~{round(math.sqrt(abs(int((my_longitude-i[5])*(111.320*math.cos(radians_latitude))))**2 + abs(int((my_latitude-i[6])*111.320))**2),1) if i[6] != None else "-"} km")
        print()
        y = i[6] - my_latitude
        x = i[5] - my_longitude
        x_points.append(x)
        y_points.append(y)
else:
    print(f'Brak samolotów w obszarze ~{(distance*2)*(distance*2)} km² wokół {localization}')

if len(x_points) > 1 and len(y_points) > 1:
    plt.plot(x_points[0],y_points[0],'bo',label='Moja lokalizacja')
    plt.plot(x_points[1:],y_points[1:],'ro',label='Samolot')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.legend()
    plt.show()
else:
    pass
