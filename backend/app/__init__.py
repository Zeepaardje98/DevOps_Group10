from flask import Flask
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
import certifi
from flasgger import Swagger
from flask_bcrypt import Bcrypt
import os
from cryptography.fernet import Fernet
from app.helpers.secrets import get_secret


app = Flask(__name__)
CORS(app=app, support_credentials=True)
bcrypt = Bcrypt(app)
key = b'Bujq_ddUgRyPQ2dwOKSWxTBYKmpeTKtrDxDptdsYrY8='

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Documentation for Attendance App",
        "description": "API Documentation for the attendance application",
        "contact": {
            "name": "DevOps Group 10",
        },
        "version": "1.0",
        "basePath": "https://localhost:3000" if os.environ.get('FLASK_ENV') == 'production' else "http://localhost:3000"
    },
    "schemes": ["https"] if os.environ.get('FLASK_ENV') == 'production' else ["http", "https"]
}

swagger_config = {
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'OPTIONS, POST, GET, DELETE'),
        ('Access-Control-Allow-Headers', '*'),
    ],
    "specs": [
        {
            "endpoint": 'Attendance_App',
            "route": "/Attendance_App.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)
app.config['CORS_HEADERS'] = 'Content-Type, Authorization, x-access-tokens, Access-Control-Allow-Origin'

# OLD WAY TO CREATE CLIENT: LEAVING IT HERE JUST IN CASE
# client = MongoClient(host='localhost',port=27017)

# Create a new client and connect to the server
username, password = get_secret()
uri = "mongodb+srv://" + username + ":" + password + "@devops.wi51crs.mongodb.net/?retryWrites=true&w=majority&appName=DevOps"
# uri = "mongodb+srv://DevOps:SHdDA77rE1CvVW5M@devops.wi51crs.mongodb.net/?retryWrites=true&w=majority&appName=DevOps"
# client = MongoClient(uri, server_api=ServerApi('1'))
client = MongoClient(uri, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.AttendenceSystem

## INITIATING COLLECTIONS
from app.Collections.Courses import Courses
from app.Collections.Departments import Departments
from app.Collections.Users import Users

Courses.create()
Departments.create()
Users.create()

from app.Controllers import courseController
from app.Controllers import departmentController
from app.Controllers import userController
from app.Controllers import studentController
from app.Controllers import teacherController
from app.Controllers import rootController
