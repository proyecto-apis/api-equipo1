from flask import jsonify, request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

password = "anitalavalatina"

@app.route('/api/characters/')
def show_character():
    all_characters=list(db.db.Personajes.find())
    for character in all_characters:
        del character["_id"]

    return jsonify({"all_characters":all_characters})

@app.route('/api/character/<int:Id>/', methods = ['GET'])
def show_a_character(Id):
    character = db.db.Personajes.find_one({"Id":Id})

    del character["_id"]

    if character != 'null':  
        return jsonify({"character":character})
    else:
        return jsonify({
            "status":400,
            "message":"Character not found",
        })
        

@app.route('/api/new_character/<string:token>', methods = ['POST'])
def add_new_character(token):

    if token == password:
        if len(request.json) == 6:
            db.db.Personajes.insert_one({
                "Id":request.json["Id"],
                "Nombre":request.json["Nombre"],
                "Edad":request.json["Edad"],
                "Sexo":request.json["Sexo"],
                "Ocupacion":request.json["Ocupación"],
                "Img":request.json["Img"]
            })
        else:
            return jsonify({
                "error":"ERROR",
                "message":"You´re missing some data",
            })

        return jsonify({
            "status":200,
            "message":f"{request.json['Nombre']} was added succesfully",
        })
    else:
        return jsonify({
            "status":300,
            "message":"Incorrect password"
        })


@app.route('/api/character/update/<int:Id>/<string:token>', methods=['PUT'])
def update_char(Id, token):
    if token == password:
        if db.db.Personajes.find_one({'Id':Id}):
            db.db.Personajes.update_one({'Id':Id},
            {'$set':{
                "Id":request.json["Id"],
                "Nombre":request.json["Nombre"],
                "Edad":request.json["Edad"],
                "Sexo":request.json["Sexo"],
                "Ocupacion":request.json["Ocupación"],
                "Img":request.json["Img"]
            }})
        else:
            return jsonify({'status':400, "message": f"Character # {Id} not found"})

        return jsonify({'status':200, "message": f"The Character # {Id} of the character list was updated"})
    else:
        return jsonify({
            "status":300,
            "message":"Incorrect password"
        })

@app.route('/api/character/delete/<int:Id>/<string:token>', methods=['DELETE'])
def delete_char(Id, token):
    if token == password:
        if db.db.Personajes.find_one({'Id':Id}):
            db.db.Personajes.delete_one({'Id':Id})
        else:
            return jsonify({'status':400, "message": f"The character # {Id} not found"})
        return jsonify({'status':200, "message": f"The character # {Id} of the character list was deleted with succes"})
    else: 
        return jsonify({
            "status":300,
            "message":"Incorrect password"
        })

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)