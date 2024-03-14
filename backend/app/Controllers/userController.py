from app import app
import json
from flask import request
from app.Services.userServices import userServices


@app.route('/signup',methods=['POST'])
def signup():
    """
Sign up a new user.

---
tags:
  - User Management
parameters:
  - in: formData
    name: username
    type: string
    required: true
    description: Username of the user.
  - in: formData
    name: name
    type: string
    required: true
    description: Name of the user.
  - in: formData
    name: department
    type: string
    required: true
    description: Department of the user.
  - in: formData
    name: password
    type: string
    required: true
    description: Password of the user.
  - in: formData
    name: role
    type: string
    required: true
    description: Role of the user.
  - in: formData
    name: confirmed
    type: boolean
    required: true
    description: Confirmation status of the user account.
  - in: formData
    name: semester
    type: integer
    required: true
    description: Semester of the user.
  - in: formData
    name: roll_no
    type: integer
    required: true
    description: Roll number of the user.
responses:
  200:
    description: User signed up successfully.
  400:
    description: Invalid request format or missing parameters.
  409:
    description: User name already exists.
  422:
    description: Wrong input.
  500:
    description: Internal server error.
    """
    user_data = json.loads(request.data.decode('utf8'))

    return userServices.signup(user_data)



@app.route('/login',methods=['POST'])
def login():
    """
Login to the system.

---
tags:
  - User Management
parameters:
  - in: formData
    name: username
    type: string
    required: true
    description: Username of the user.
  - in: formData
    name: password
    type: string
    required: true
    description: Password of the user.
  - in: formData
    name: remember_me
    type: boolean
    required: false
    description: Indicates whether the user wants to be remembered.
responses:
  200:
    description: User logged in successfully.
  400:
    description: Invalid request format or missing parameters.
  401:
    description: Unauthorized access, incorrect username or password.
  403:
    description: Confirmation pending.
  500:
    description: Internal server error.
    """
    user_data = json.loads(request.data.decode('utf8'))
    
    print(user_data)
    username = user_data['username']
    password = user_data['password']

    return userServices.login(username,password)


@app.route('/get_user',methods=['POST'])
def get_user():
    """
Retrieve user information by username.

---
tags:
  - User Management
parameters:
  - in: query
    name: username
    type: string
    required: true
    description: Username of the user to retrieve information for.
responses:
  200:
    description: User information retrieved successfully.
  400:
    description: Invalid request format or missing parameters.
  404:
    description: User not found.
  500:
    description: Internal server error.
    """
    print(json.loads(request.data.decode('utf8')))
    
    username = json.loads(request.data.decode('utf8'))['username']
    return userServices.get_user(username)




    
    

    

    

    

