"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos/user', methods=['GET'])
def read_users():
    try:
        all_users = User.get_all_users()
        return jsonify(all_users), 200
    except:
        return "Couldn't find the user",400

@app.route('/todos/user/<username>', methods=['POST'])
def create_user(username):
    # body=request.get_json()
    try:
        # if body is None:
            # return "Body content is missing", 400
        new_user= User(user_name= username)
        new_user.add_user()
        return jsonify(new_user.serialize()), 200
    except:
        return "Couldn't create the user",409

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/todos/user/<username>', methods=['GET'])
def get_users(username):
    try:
        users_nick = User.get_user(username)
        return jsonify(users_nick), 200
    except:
        return "Couldn't find the user",404

@app.route('/todos/user/<username>/task', methods=['POST'])
def create_tasks(username):
    body=request.get_json()
    try:
        if body is None:
            return "Body content is missing", 400
        new_task = Task(user_to_do= username ,label=body["label"],done=body["done"])
        new_task.add_task()
        return jsonify(new_task.serialize()), 200
    except:
        return "Couldn't create the task", 409

@app.route('/todos/user/<username>/task', methods= ['GET'])
def read_tasks(username):
    try:
        todos = Task.get_user_tasks(username)
        return jsonify(todos),200
    except:
        return "Couldn't find the task", 404

@app.route('/todos/user/<username>/task', methods=['PUT'])
def update_tasks(username):
    body=request.get_json()
    try:
        task = Task(user_to_do= username, id =body["id"] , label=body["label"],done=body["done"])
        task.update_task(username, body["label"],body["done"],body["id"])
        return jsonify(task.serialize()),202
    except:
        return "Couldn't update the task", 409

@app.route('/todos/user/<username>', methods=['DELETE'])
def delete(username):
    try:
        deleted_user = User.delete_user(username)
        return jsonify(deleted_user), 202
    except:
        return "Couldn't delete the task", 409