from flask import Flask,Response
import pymongo
import json
app = Flask(__name__)
from flask import request
from bson.objectid import ObjectId


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info()
    print("----------------Mission pass-----------------")
except:
    print("----------------Mongo not connected-----------------")



@app.route("/user/",methods=["POST"] )
def create_user():
    try:
        user = {"name" : request.form["name"],"last_name":request.form["last_name"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps( {"message":"user created ","id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        print(e)



@app.route("/users/",methods=["GET"])
def get_user_list():
    try:

        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            response=json.dumps( {"message":"Error" }),
            status=500,
            mimetype="application/json"
        )


@app.route("/user/<id>", methods=["PATCH"])
def user_update(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )

        # for attr in dir(dbResponse):
        #     print(attr)
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message":"User Updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message":"Nothing to update"}),
                status=200,
                mimetype="application/json"
            )

    except Exception as e:
        return Response(
            response=json.dumps( {"message":"Error" }),
            status=500,
            mimetype="application/json"
        )



@app.route("/user/delete/<id>",methods=["DELETE"])
def user_delete(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps({"message":"User Deleted"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message":"User Not Found"}),
                status=200,
                mimetype="application/json"
            )
        
    except Exception as e:
        return Response(
            response=json.dumps( {"message":"Error" }),
            status=500,
            mimetype="application/json"
        )


if __name__ == '__main__':
    app.run(port=80,debug=True)