from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.debug = True


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
