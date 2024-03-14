from flask import request, jsonify
from app import app
import json
import os
import cv2
import face_recognition
import numpy as np

from app.helpers.data_helper import get_student_encoding, get_student_rolls

from app.Services.courseServices import courseServices
from app.Services.studentServices import studentServices
from app.Services.userServices import userServices


@app.route('/initiate_attendence', methods=['POST'])
def initiate_attendence():
    """Endpoint to take attendance after a teacher initiates it
    ---
    tags:
      - Course Management
    parameters:
      - in: body
        name: courseData
        required: true
        description: The course data that will be used to query the database to fetch course information
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the course.
            department:
              type: string
              description: The department of the course.
            semester:
              type: integer
              description: The semester of the course.
      - in: formData
        name: image
        required: true
        description: The image file
        type: file
    responses:
      200:
        description: Successfully initiated attendance
      400:
        description: Problem occurred with the uploaded image
      401:
        description: No student enrolled in the course
    """
    courseData = json.loads(request.form.get('courseData'))

    course = courseServices.getCourse(filter=courseData)
    if (not course['student_enrolled']):
        return jsonify({
            "status": 200,
            "result": {
                "status": 401,
                "message": "No Students Enrolled in the Course"
            }
        })

    imagestr = request.files['file']

    try:
        image_bytes = imagestr.read()
        image_numpy = np.frombuffer(image_bytes, dtype=np.uint8)
        imageLoaded = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)

        class_image_encodings = face_recognition.face_encodings(imageLoaded, model="cnn")
        all_student_data = studentServices.get_all_students_enrolled(**courseData)
        known_face_encodings = get_student_encoding(all_student_data)
        all_student_roll_nos = get_student_rolls(all_student_data)

        courseServices.mark_all_absent(courseData)  ############ SOME ERROR

        for face_encoding, student_roll in zip(class_image_encodings, all_student_roll_nos):
            print("STUD ROLL", student_roll)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                courseServices.mark_present(student_roll, courseData)
        return jsonify({
            "status": 200,
            "result": {
                "status": 201,
                "message": "Attendance Done"
            }
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": 200,
            "result": {
                "status": 400,
                "message": "Some problem check your image"
            }
        })


@app.route('/add_course', methods=['POST'])
def add_course():
    """ Endpoint to add a course (only admins can do it)
    ---
    tags:
      - Course Management
    parameters:
      - in: body
        name: requestBody
        required: true
        description: JSON object containing course data.
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the course.
              example: "DevOps and Cloud-based Software"
            department:
              type: string
              description: The department of the course.
              example: "CS"
            semester:
              type: integer
              description: The semester of the course.
              example: 1
            teacherAssigned:
              type: string
              description: The teacher assigned to the course.
              example: "teacher"
    responses:
      200:
        description: Course successfully added.
      400:
        description: Invalid request format or missing parameters.
      409:
        description: Course already exists.
      500:
        description: Internal server error.
    """
    # Structur of "data"
    # data = {
    #     "name": "",
    #     "teacherAssigned"
    courseData = json.loads(request.data.decode('utf8'))

    filter = {
        "name": courseData['teacherAssigned'],
        "department": courseData['department']
    }
    userServices.updateCourseInfoOfUser(courseData['name'], filter, "teacher")
    return courseServices.add_course(courseData)


@app.route('/get_all_courses', methods=['POST'])
def get_all_courses():
    """
Retrieve all courses based on optional filters and projection.

---
tags:
  - Course Management
parameters:
  - in: body
    name: filters
    description: Optional JSON object containing filters for course attributes.
    schema:
      type: object
      properties:
        department:
          type: string
          description: Filter by department name.
          example: "CS"
        name:
          type: string
          description: Filter by course name.
          example: "DevOps and Cloud-based Software"
        semester:
          type: string
          description: Filter by semester.
          example: 1
        teacherAssigned:
          type: string
          description: Filter by teacher assigned.
          example: "Yuri Demchenko"
  - in: body
    name: projection
    description: Optional JSON object containing projection settings for course attributes.
    schema:
      type: object
      properties:
        department:
          type: boolean
          description: Include department field in the response.
        name:
          type: boolean
          description: Include name field in the response.
        semester:
          type: boolean
          description: Include semester field in the response.
        teacherAssigned:
          type: boolean
          description: Include teacherAssigned field in the response.
responses:
  200:
    description: List of courses retrieved successfully.
  400:
    description: Invalid request format.
    """
    ## Called From (check for call of getAndSetCourses action in these js file which intern calls get_all_courses)
    # 1)AttendancePage/AttendancePage.js
    # 2)ShowCoursePage/ShowCoursePage.js
    # 3)EnrollToCoursePage/EnrollToCoursePage.js

    ## Loading the data request data
    filters = json.loads(request.data.decode('utf8')).get('filters')
    projection = json.loads(request.data.decode('utf8')).get('projection')

    curser = courseServices.get_all_courses(filters, projection)

    allCourses = []
    for course in curser:
        if not projection:
            del course['student_enrolled']
        del course['_id']
        allCourses.append(course)

    response = jsonify({
        "allCourses": allCourses
    })

    return response


@app.route('/getAttendance', methods=['POST'])
def getAttendance():
    """
Retrieve attendance information based on specified criteria.

---
tags:
  - Course Management
parameters:
  - in: body
    name: requestBody
    required: true
    description: JSON object containing attendance query parameters.
    schema:
      type: object
      properties:
        all_or_one:
          type: string
          description: Specify whether to retrieve attendance for all time or just one month.
          enum: ["all", "one"]
          example: "one"
        course:
          type: string
          description: The name of the course.
          example: "Experimental Design and Data Analysis"
        department:
          type: string
          description: The department of the course.
          example: "CS"
        month:
          type: integer
          description: The month number (Uses 0-based indexing, so January is 0).
          example: 1
        role:
          type: string
          description: The role of the entity (e.g., student, teacher).
          example: "student"
        roll_no:
          type: integer
          description: The roll number (student ID) of the entity.
          example: 1
        semester:
          type: integer
          description: The semester of the course.
          example: 1
responses:
  200:
    description: Attendance information retrieved successfully.
  400:
    description: Invalid request format or missing parameters.
    """
    data = json.loads(request.data.decode('utf8'))
    print("DATA", data)

    if (data['role'] == 'student'):
        filters = {
            "name": data['course'],
            "department": data['department'],
            "semester": data['semester']
        }
        others = {
            "month": data['month'],
            "all_or_one": data['all_or_one'],
            "roll_no": data['roll_no'] if data['roll_no'] else None,
            "role": data['role']
        }
    else:
        filters = {
            "name": data['course'],
            "department": data['department'],
            "teacherAssigned": data['teacherAssigned']
        }
        others = {
            "month": data['month'],
            "all_or_one": data['all_or_one'],
            "role": data['role']
        }

    try:
        attendance = courseServices.getAttendance(filters, others)
        print("COURSE CONTROLLER", attendance)
        return jsonify({
            "status": 200,
            "result": {
                "status": 200,
                "message": "Fetched",
                "data": attendance
            }
        })
    except:
        return jsonify({
            "status": 200,
            "result": {
                "status": 400,
                "message": "Some Problem while fetching...",
                "data": []
            }
        })
