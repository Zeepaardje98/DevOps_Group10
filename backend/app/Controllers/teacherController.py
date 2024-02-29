from app import app

import json 
from flask import jsonify,request
from app.Services.teacherServices import teacherServices


@app.route('/get_all_teachers',methods=['POST'])
def get_all_teachers():
    """
Retrieve all teachers based on optional filters and projection.

---
tags:
  - Teacher Management
parameters:
  - in: body
    name: filters
    description: Optional JSON object containing filters for teacher attributes.
    schema:
      type: object
      properties:
        confirmed:
          type: boolean
          description: Filter by confirmation status of teacher account.
        username:
          type: string
          description: Filter by username of the teacher.
        name:
          type: string
          description: Filter by name of the teacher.
        courseAssigned:
          type: array
          description: Filter by courses assigned to the teacher.
          items:
            type: string
          example: ["Math 101", "Physics 201"]
        department:
          type: string
          description: Filter by department of the teacher.
        password:
          type: string
          description: Filter by password of the teacher.
        role:
          type: string
          description: Filter by role of the teacher.
  - in: body
    name: projection
    description: Optional JSON object containing projection settings for teacher attributes.
    schema:
      type: object
      properties:
        confirmed:
          type: boolean
          description: Include confirmation status field in the response.
        username:
          type: boolean
          description: Include username field in the response.
        name:
          type: boolean
          description: Include name field in the response.
        courseAssigned:
          type: boolean
          description: Include courses assigned field in the response.
        department:
          type: boolean
          description: Include department field in the response.
        password:
          type: boolean
          description: Include password field in the response.
        role:
          type: boolean
          description: Include role field in the response.
responses:
  200:
    description: List of teachers retrieved successfully.
  400:
    description: Invalid request format.
  500:
    description: Internal server error.
    """
    filters = json.loads(request.data.decode('utf8'))['filters']
    projection = json.loads(request.data.decode('utf8'))['projection']
    filters = None if not filters else filters 
    projection = None if  not projection else projection
    
    print("*********************")
    print("*********************")
    print("*********************")
    print("*********************")
    print(filters)
    print(projection)
    
    try:
        filters['_id'] = filters.pop('username')
    except:
        pass
    
    curser = teacherServices.get_all_teachers(filters, projection)
    
    allTeachers = []
    for teacher in curser:
        try:
            teacher['username'] = teacher.pop('_id')
        except: pass
        allTeachers.append(teacher)
    
    print("*********************")
    print("*********************")
    print("*********************")
    print("*********************")
    print(allTeachers)
    print("*********************")
    print("*********************")
    print("*********************")
        
    return jsonify({
        "allTeachers": allTeachers
    })

@app.route('/update_teacher',methods=['POST'])
def update_teacher():
    """
Update teacher information.

---
tags:
  - Teacher Management
parameters:
  - in: body
    name: requestBody
    required: true
    description: JSON object containing update parameters.
    schema:
      type: object
      properties:
        whatToUpdate:
          type: object
          description: JSON object containing fields to update for the teacher.
          properties:
            confirmed:
              type: boolean
              description: Confirmation status of teacher account.
            username:
              type: string
              description: Username of the teacher.
            name:
              type: string
              description: Name of the teacher.
            courseAssigned:
              type: array
              description: Courses assigned to the teacher.
              items:
                type: string
            department:
              type: string
              description: Department of the teacher.
            password:
              type: string
              description: Password of the teacher.
            role:
              type: string
              description: Role of the teacher.
        whomToUpdate:
          type: string
          description: Username of the teacher to update.
responses:
  200:
    description: Teacher information updated successfully.
  400:
    description: Invalid request format or missing parameters.
  404:
    description: Teacher not found.
  500:
    description: Internal server error.
    """
    updateData = json.loads(request.data.decode('utf8'))
    print("updateData : ",updateData)
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return teacherServices.update_teacher(whomToUpdate,whatToUpdate)