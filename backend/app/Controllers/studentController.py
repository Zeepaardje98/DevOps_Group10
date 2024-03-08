from app import app
import json
import os
import cv2
import face_recognition
from flask import jsonify, request
from app.Services.studentServices import studentServices
from app.Services.userServices import userServices
import numpy as np
from app.helpers.image_helper import encrypt_face_encoding
from app import key

@app.route('/get_all_students',methods=['POST'])
def get_all_students():
    """
Retrieve all students based on optional filters and projection.

---
tags:
  - Student Management
parameters:
  - in: body
    name: filters
    description: Optional JSON object containing filters for student attributes.
    schema:
      type: object
      properties:
        confirmed:
          type: boolean
          description: Filter by confirmation status of student account.
          example: true
        courseEnrolled:
          type: array
          description: Filter by courses in which the student is enrolled.
          items:
            type: string
          example: ["Math 101", "Physics 201"]
        department:
          type: string
          description: Filter by department of the student.
          example: "CS"
        name:
          type: string
          description: Filter by name of the student.
          example: "John Doe"
        password:
          type: string
          description: Filter by password of the student.
          example: "password123"
        role:
          type: string
          description: Filter by role of the student.
          example: "student"
        roll_no:
          type: integer
          description: Filter by roll number of the student.
          example: 123
        semester:
          type: integer
          description: Filter by semester of the student.
          example: 1
        username:
          type: string
          description: Filter by username of the student.
          example: "john123"
  - in: body
    name: projection
    description: Optional JSON object containing projection settings for student attributes.
    schema:
      type: object
      properties:
        confirmed:
          type: boolean
          description: Include confirmation status field in the response.
          example: true
        courseEnrolled:
          type: boolean
          description: Include courses enrolled field in the response.
          example: true
        department:
          type: boolean
          description: Include department field in the response.
          example: false
        name:
          type: boolean
          description: Include name field in the response.
          example: true
        password:
          type: boolean
          description: Include password field in the response.
          example: false
        role:
          type: boolean
          description: Include role field in the response.
          example: false
        roll_no:
          type: boolean
          description: Include roll number field in the response.
          example: true
        semester:
          type: boolean
          description: Include semester field in the response.
          example: false
        username:
          type: boolean
          description: Include username field in the response.
          example: true
responses:
  200:
    description: List of students retrieved successfully.
  400:
    description: Invalid request format.
  500:
    description: Internal server error.
    """
    data = json.loads(request.data.decode('utf8'))
    filters = data.get('filters')
    projection = data.get('projection')
    
    print("***********************")
    print(filters, projection)
    
    try:
        filters['_id'] = filters.pop('username')
    except: pass    
    
    curser = studentServices.get_all_students(filters, projection)
    
    allStudents = []
    for student in curser:
        student['username'] = student.pop('_id')
        student['courseEnrolled'] = studentServices.get_all_enrolled_courses(student["roll_no"])
        allStudents.append(student)
        
    return jsonify({
        "allStudents" : allStudents
    })
    
    
@app.route('/update_student',methods=['POST'])
def update_sudent():
    """
Update student information.

---
tags:
  - Student Management
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
          description: JSON object containing fields to update for the student.
          properties:
            confirmed:
              type: boolean
              description: Confirmation status of student account.
            courseEnrolled:
              type: array
              description: Courses in which the student is enrolled.
              items:
                type: string
            department:
              type: string
              description: Department of the student.
            name:
              type: string
              description: Name of the student.
            password:
              type: string
              description: Password of the student.
            role:
              type: string
              description: Role of the student.
            roll_no:
              type: integer
              description: Roll number of the student.
            semester:
              type: integer
              description: Semester of the student.
            username:
              type: string
              description: Username of the student.
        whomToUpdate:
          type: string
          description: Username of the student to update.
responses:
  200:
    description: Student information updated successfully.
  400:
    description: Invalid request format or missing parameters.
  404:
    description: Student not found.
  500:
    description: Internal server error.
    """
    updateData = json.loads(request.data.decode('utf8'))
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return studentServices.update_student(whomToUpdate,whatToUpdate)



@app.route('/enroll_student',methods=['POST'])
def enroll_student():
    """
Enroll a student in courses.

---
tags:
  - Student Management
parameters:
  - in: formData
    name: image
    type: file
    required: true
    description: Image file containing student details.
  - in: body
    name: courseData
    type: object
    required: true
    description: JSON object containing course enrollment data.
    schema:
      type: object
      additionalProperties:
        type: boolean
        description: Boolean indicating whether the student is enrolled in the course.
    example:
        Math 101: true
        Physics 201: false
        Chemistry 301: true
  - in: formData
    name: roll_no
    type: integer
    required: true
    description: Roll number of the student.
responses:
  200:
    description: Student enrolled successfully.
  400:
    description: Invalid request format or missing parameters.
  409:
    description: Student already enrolled.
  500:
    description: Internal server error.
    """
    """Enroll The Student Passed Through Request With Its Image"""
    ################ FROM DATA ###############
    courseData = json.loads(request.form.get('courseData'))
    student_roll = request.form.get('roll_no')
    imagestr = request.files['file']
    ##########################################
    
    ### SAVING THE IMAGE 
    image_bytes = imagestr.read()
    image_numpy = np.frombuffer(image_bytes, dtype=np.uint8)
    imageLoaded = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)

    ### CREATING ENCODING OF THE FACE OF THE STUDENT
    student_image_encoding = encrypt_face_encoding(list(face_recognition.face_encodings(imageLoaded)[0]), key)
    responseObjectArray = []
    ######## LOOP THROUGH ALL THE COURSE TO ENROLL ########### 
    for course,condition in courseData.items(): 
        # IF CONDITION === TRUE(TRUE IF CLICKED THE CHECKBOX WHILE ENROLLING) 
        #    ONLY THEN ENROLL STUDENT TO THE COURSE
        if condition:    
            student_data = {
                "roll_no": student_roll,
                "encoding": student_image_encoding
            }
            courseResponse = studentServices.enroll_student(course,student_data)
            userServices.updateCourseInfoOfUser(course,{"roll_no": student_roll},'student')
            responseObjectArray.append(courseResponse)
    return jsonify(responseObjectArray)