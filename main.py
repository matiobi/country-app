from flask import Flask, render_template
import requests

app = Flask(__name__)
app.debug = True


@app.route("/")
def home_page():
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()
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

        border_countries = ",".join(data[0]['borders'])
        response_neighbours= requests.get(f"https://restcountries.com/v3.1/alpha?codes={border_countries}")
        neighbours_data = list(response_neighbours.json())
        neighbours = list(map(lambda neighbour: neighbour['name']['common'], neighbours_data))

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
          "coat_of_arms" : data[0]['coatOfArms']['svg']
        }

        

        return render_template("country.html", country = country, neighbours = neighbours)
