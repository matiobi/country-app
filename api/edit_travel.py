from pymongo import MongoClient
from flask import jsonify, request
from bson import ObjectId



def edit_travel(travel_id, travel):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["country_db"]
    collection =db ["travels"]


    try: 
        result = collection.update_one(
             {"_id":ObjectId(travel_id)},
             {"$set": {
                "title" : travel['title'],
                "desc" : travel['desc'],
                "start" : travel['start'],
                "end" : travel['end'],
                "cost": travel['cost'],
                "country" : travel['country']

             }})


        return jsonify({
            "message":"TRAVEL WAS UPDATED SUCCESFULLY",
            "error":str(e),
            "ok":False
            })

    except Exception as e:
            
            return jsonify({
            "message":"An error occured",
            "error":str(e),
            "ok":False

            })