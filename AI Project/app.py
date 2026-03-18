from flask import Flask, render_template, request
import requests
import math
import random

app = Flask(__name__)

API_KEY = "38fb7b071ee842448897be2bc715cf9d"

# Example user location (Hyderabad)
USER_LAT = 17.3850
USER_LON = 78.4867


def get_coordinates(place):

    url = f"https://api.opencagedata.com/geocode/v1/json?q={place}&key={API_KEY}"

    response = requests.get(url).json()

    if response["results"]:

        lat = response["results"][0]["geometry"]["lat"]
        lon = response["results"][0]["geometry"]["lng"]

        return lat, lon

    return None


def calculate_distance(lat1,lon1,lat2,lon2):

    return round(math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)*111,2)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/domain")
def domain():
    return render_template("domain.html")


@app.route("/travel")
def travel():
    return render_template("travel.html")


@app.route("/travel_result",methods=["POST"])
def travel_result():

    destination = request.form["destination"]

    coords = get_coordinates(destination)

    if coords is None:
        return "Location not found. Try another place."

    lat2,lon2 = coords

    dist = calculate_distance(USER_LAT,USER_LON,lat2,lon2)

    ola_bike = 20 + dist*8 + random.randint(5,15)
    ola_auto = 40 + dist*10 + random.randint(10,20)
    ola_car = 80 + dist*15 + random.randint(20,30)

    uber_bike = 25 + dist*9 + random.randint(5,15)
    uber_auto = 45 + dist*11 + random.randint(10,20)
    uber_car = 90 + dist*16 + random.randint(20,30)

    rapido_bike = 18 + dist*7 + random.randint(5,15)
    rapido_auto = 38 + dist*9 + random.randint(10,20)
    rapido_car = 85 + dist*14 + random.randint(20,30)

    prices = {
        "Ola Bike":ola_bike,
        "Ola Auto":ola_auto,
        "Ola Car":ola_car,
        "Uber Bike":uber_bike,
        "Uber Auto":uber_auto,
        "Uber Car":uber_car,
        "Rapido Bike":rapido_bike,
        "Rapido Auto":rapido_auto,
        "Rapido Car":rapido_car
    }

    best = min(prices,key=prices.get)

    return render_template(
        "travel_result.html",
        destination=destination,
        ola_bike=round(ola_bike),
        ola_auto=round(ola_auto),
        ola_car=round(ola_car),
        uber_bike=round(uber_bike),
        uber_auto=round(uber_auto),
        uber_car=round(uber_car),
        rapido_bike=round(rapido_bike),
        rapido_auto=round(rapido_auto),
        rapido_car=round(rapido_car),
        best=best
    )


@app.route("/food")
def food():
    return render_template("food.html")


@app.route("/food_result",methods=["POST"])
def food_result():

    item = request.form["food"].lower()

    food_db = {

        "pizza":{
            "Dominos":{"Zomato":350,"Swiggy":370},
            "Pizza Hut":{"Zomato":380,"Swiggy":400}
        },

        "biryani":{
            "Paradise":{"Zomato":280,"Swiggy":300},
            "Mehfil":{"Zomato":250,"Swiggy":260}
        },

        "burger":{
            "McDonalds":{"Zomato":200,"Swiggy":210},
            "KFC":{"Zomato":220,"Swiggy":230}
        }

    }

    if item not in food_db:
        return "Try pizza, biryani or burger"

    data = food_db[item]

    return render_template("food_result.html",item=item,data=data)


if __name__ == "__main__":
    app.run(debug=True)