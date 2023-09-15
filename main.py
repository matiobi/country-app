from flask import Flask, render_template, request, jsonify, redirect
import requests
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

#Połączenie z bazą danych

clinet = MongoClient("mongodb+srv://mobirek:0x4JoghzVJeQdNUe@bazadanych.qi41g3x.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
poland_db = clinet["polska"]
poland_cities = poland_db["miasta"]

@app.route('/api/get-cities')
def get_all_cities():
    data = list(poland_cities.find({},{"_id":0}))
    return jsonify(data)

@app.route("/cities")
def cities_page():
    cities = list(poland_cities.find({},{"_id":0}))
    return render_template("cities.html", cities=cities)


#------------------------------------------------------

@app.route("/add-city", methods=['POST'])
def add_city():
    name = request.form.get("city_name")
    population = request.form.get("city_population")
    type = request.form.get("city_type")

    poland_cities.insert_one({
        "name":name,
        "population": population,
        "type":type

    })

    return redirect("/cities", code=302)




@app.route("/", methods=["GET", "POST"])
def home_page():
    

    search_query = request.form.get("query")
    continent_filter = request.form.get("continent_filter")
    print(search_query)

    url =""
    if search_query:
        url = f"https://restcountries.com/v3.1/name/{search_query}"
    else:
        url = "https://restcountries.com/v3.1/all"


    try:
        response = requests.get(url)
        countries = response.json()

        if continent_filter:
            countries = filter(lambda country:country['region'] == continent_filter, countries)

        return render_template("index.html", countries = countries)
    except Exception as e:
        print("WYSTĄPIŁ BŁĄD", str(e))
        return " NIE DZIAŁA "
        
@app.route("/country/<name>")
def country_page(name):

        response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
        data = response.json()

        currency_key = list(data[0]['currencies'].keys())[0]
        native_name_key = list(data[0]['name']['nativeName'].keys())[0]
        languages = list(data[0]['languages'].values())

        neighbours = []

        for field in data:
          if "borders" not in field:
              print("NIE MA BORDERS!!")
          else:
              border_countries = ",".join(data[0]['borders']) 
              response_neighbours= requests.get(f"http://restcountries.com/v3.1/alpha?codes={border_countries}")
              neighbours_data = list(response_neighbours.json())
              neighbours = map(lambda neighbour: neighbour['name']['common'], neighbours_data)
        

        country = {
          "currency_name": data[0]['currencies'][currency_key]['name'],
          "native_name":data[0]['name']['nativeName'][native_name_key]['common'],
          "common_name": data[0]['name']['common'],
          "languages" : ", " .join(languages),
          "population": data[0]['population'],
          "region" : data[0]['region'],
          "subregion" : data[0]['subregion'],
          "capital" : data[0]['capital'][0],
          "tld" : data[0]['tld'],
          "coat_of_arms":data[0]["coatOfArms"]['svg'] if data[0]['coatOfArms'] else data[0]['flags']['svg']
        }

        

        return render_template("country.html", country = country, neighbours = neighbours)
