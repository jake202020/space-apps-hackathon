"""START OF SPACE APPS API"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Resource
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'postgresql:///space_db')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "thisisthelocalsecretkey")

connect_db(app)

@app.route('/')
def index_page():
    """Renders html template - NOT PART OF JSON API!"""
    return render_template('index.html')

# *****************************
# RESTFUL SPACE RESOURCES JSON API
# *****************************
@app.route('/api/resources')
def list_resources():
    """Returns JSON w/ all resources"""
    all_resources = [resource.serialize() for resource in Resource.query.all()]
    return jsonify(resources=all_resources)

@app.route('/api/resources', methods=["POST"])
def create_resource():
    """Creates a new todo and returns JSON of that created todo"""
    new_resource = Resource(name = request.json["name"], 
                url = request.json["url"],
                description = request.json["description"],
                login_required = request.json["login_required"],
                api_available = request.json["api_available"],
                country_of_origin = request.json["country_of_origin"],
                documentation_url = request.json["documentation_url"],
                keywords = request.json["keywords"])
    db.session.add(new_resource)
    db.session.commit()
    response_json = jsonify(resource=new_resource.serialize())
    return (response_json, 201)