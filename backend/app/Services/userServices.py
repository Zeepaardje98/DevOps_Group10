from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, Response
import datetime 
import jwt
from app import bcrypt
from flask_bcrypt import Bcrypt
class userServices():
    

        
    @staticmethod
    def usernameExists(username:str):
        users = db['users']
        return users.find_one({"_id":username})

    @staticmethod
    def signup(userData:dict):
        users = db['users']
        
        userData['_id'] = userData.pop('username')
        print(userData['_id'])
        userData.update({
            "confirmed": userData['confirmed'] if userData['confirmed'] else False

        })
        user = {
            "_id": userData['_id'],
            "name": userData['_id'],
            "department": userData.get("department", "CS"),
            "password": userData["password"],
            "role": userData["role"],
            "confirmed": userData["confirmed"],
            "semester": int(userData.get("semester", 0)),
            "roll_no": int(userData.get("roll_no", 0))
        }
        # userData = {
        #     "_id": user['username'],
        #     "name": user['name'],
        #     "department": user['department'],
        #     "password": user['password'],
        #     "role": user['role'],
        #     "confirmed": user['confirmed'] if user['confirmed'] else False
        # }
        # if(userData['role'] == "student"):
        #     user['semester'] = userData['semester']
        #     user["roll_no"] = userData["roll_no"]


        if(userServices.usernameExists(user['_id'])):
            response = {
                "status": 200,
                "result": {
                    "status": 409,
                    "message": "username already exists!"
                }
            }
        else:
            try:
                users.insert_one(user)
                response = {
                    "status": 200,
                    "result" : {
                        "status": 201,
                        "message": "user created"
                    }
                }
            except WriteError:
                response = {
                    "status": 400,
                    "result": {
                        "status": 422,
                        "message": "wrong input by user"
                    }
                }
    
        return jsonify(response)


    @staticmethod
    def check_user(username:str,password:str):
        Users = db['users']
        
        return Users.find_one({"_id": username,"password":password})

    @staticmethod
    def check_user_wo_password(username: str):
        Users = db['users']

        return Users.find_one({"_id": username})

    @staticmethod
    def get_user(username:str):
        Users = db['users']
        
        return jsonify(Users.find_one({"_id":username}))
    
    @staticmethod
    def login(username,password):
        # user = userServices.check_user(username,password)
        user = userServices.check_user_wo_password(username)

        # salt = "$2a$10$ThisIsACustomSaltValue"
        # pass_hash = Bcrypt.generate_password_hash(bcrypt, password, 10)
        if (user and Bcrypt.check_password_hash(bcrypt, user['password'], password)):
            if(user['role'] != "admin" and (not user['confirmed'])):
                responseData = {
                    "status": 200,
                    "result": {
                        "status":403,
                        "message": "Confirmation is Pending"
                    }
                }
                response = jsonify(responseData)
            elif(user):
                # jwToken = jwt.encode(user,username).decode()
                responseData = {
                    "status":200,
                    "result":{
                        "data":{
                            "username":username,
                            "role":user['role']
                            },
                        "status": 200,
                        "message": "User is Logged In"
                    }
                }
                response = jsonify(responseData)
            

        else:
            responseData = {
                "status": 200,
                "result":{
                    "status": 401,
                    "message": "username or password is wrong"
                }
            }
            response = jsonify(responseData)
            
        return response
    
    @staticmethod
    def updateCourseInfoOfUser(course, filter, role):
        Users = db['users']
        if role == "student":
            print("INSIDE updateCourseInfoOfUser")
            Users.update_one( {**filter}, {"$push": {"courseEnrolled": course} } )
        elif role == "teacher":
            Users.update_one({**filter}, {"$push": {"courseAssigned": course}} )
        
        
    
    
    
    
    
    
    
            
    
            
            