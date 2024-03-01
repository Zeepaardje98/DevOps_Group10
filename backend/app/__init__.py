from flask import Flask
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS


app = Flask(__name__)
CORS(app=app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type, Authorization, x-access-tokens, Access-Control-Allow-Origin'

app.config['IMAGE_UPLOAD_PATH'] = "app/static/images"

# Create a new client and connect to the server
uri = "mongodb+srv://DevOps:SHdDA77rE1CvVW5M@devops.wi51crs.mongodb.net/?retryWrites=true&w=majority&appName=DevOps"
client = MongoClient(uri, server_api=ServerApi('1'))

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


