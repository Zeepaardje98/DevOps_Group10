from flask import request,jsonify
from app import app
import json

from app.Services.departmentServices import departmentServices


@app.route('/get_all_departments',methods=['POST'])
def get_all_departments():
    """
Retrieve all departments.

---
tags:
  - Department Management
parameters: []
responses:
  200:
    description: List of all departments retrieved successfully.
  400:
    description: Error retrieving departments.
  500:
    description: Internal server error.
    """
    curser = departmentServices.get_all_departments()
    
    allDepartments = []
    for department in curser:
        dataToSend = {
            "name" : department['name']
        }
        
        allDepartments.append(dataToSend)
        
    return jsonify({
        "allDepartments": allDepartments
    })
    
    
    
@app.route('/add_department', methods=['POST'])
def add_department():
    """
Add a new department.

---
tags:
  - Department Management
parameters:
  - in: body
    name: body
    required: true
    description: The name of the department.
    schema:
      id: Department
      required:
        - name
      properties:
        name:
          type: string
          description: The name of the department.
responses:
  200:
    description: Department added successfully.
  400:
    description: Invalid request format or missing parameters.
  409:
    description: Department already exists.
  500:
    description: Internal server error.
    """
    # Structure of Department
    # data = [{
    #   "name" : ""   
    #}]
    departmentData = json.loads(request.data.decode('utf8'))
    name = departmentData['name']
    
    return departmentServices.add_department(name)