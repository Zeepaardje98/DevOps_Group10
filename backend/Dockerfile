FROM jasonchristo99/python3.9-slim-lambda-adapter-dlib-face-rec-models-opencv
WORKDIR /var/task
COPY . .
RUN python -m pip install -r requirements.txt
RUN ls
# The module is the name of the Python module.
# The variable is the name of the variable that is a WSGI app.
CMD ["gunicorn", "-b=:8080", "-w=1", "run:app", "--timeout", "90"]
