from flask import request,jsonify 
from pymongo import MongoClient

def add_travel():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["country_db"]
    collection =db ["travels"]
    title = request.form.get("travel_title")
    desc = request.form.get("travel_desc")
    start = request.form.get("travel_start")
    end = request.form.get("travel_end")
    cost = request.form.get("travel_cost")
    country = request.form.get("travel_country")

    # client = MongoClient("mongodb://localhost:27017/")
    # db = client["country_db"]
    # collection =db ["travels"]
    # title = request.json["travel_title"]
    # desc = request.json["travel_desc"]
    # start = request.json["travel_start"]
    # end = request.json["travel_end"]
    # cost = request.json["travel_cost"]
    # country = request.json["travel_country"]




    try:

        data = {

            "title" : title,
            "desc" : desc,
            "start" : start,
            "end" : end,
            "cost": cost,
            "country" : country
        }

        collection.insert_one(data)
        data['_id'] = str(data["_id"])

        return jsonify({

            "message": "DODANO NOWĄ PODRÓŻ",
            "ok" : True,
            "data" : data

        })

    except Exception as e:

        return jsonify({

            "message": "AN ERROR OCCURED",
            "error" : str(e),
            "ok" : False


        })