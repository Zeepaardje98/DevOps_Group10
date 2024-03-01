from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app=app, support_credentials=True)

swagger_template ={
    "swagger": "2.0",
    "info": {
      "title": "Documentation for Attendance App",
      "description": "API Documentation for the attendance application",
      "contact": {
        "name": "DevOps Group 10",
        },
      "version": "1.0",
      "basePath":"http://localhost:3000",
              },
    "schemes": [
        "http",
        "https"
    ],
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

app.config['IMAGE_UPLOAD_PATH'] = "app/static/images"


client = MongoClient(host='localhost',port=27017)
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
