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
        