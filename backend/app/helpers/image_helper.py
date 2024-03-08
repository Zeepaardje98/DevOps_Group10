import face_recognition
import os
from cryptography.fernet import Fernet
import bson

print("==============================")
print(os.getcwd())
print("==============================")


def generate_image_encoding():
    face_picture = face_recognition.load_image_file("app/tabishGroup.jpeg")
    face_locations = face_recognition.face_locations(face_picture,model='hog')
    return face_recognition.face_encodings(face_picture, face_locations)

def encrypt_face_encoding(face_encoding, key):
    # Initialize Fernet with the provided key
    fernet = Fernet(key)
    
    # Convert the face encoding to a string without brackets
    face_encoding_str = ','.join(map(str, face_encoding))
    
    # Encrypt the face encoding
    encrypted_face_encoding = fernet.encrypt(face_encoding_str.encode('utf-8'))
    
    return bson.Binary(encrypted_face_encoding)

def decrypt_face_encoding(encrypted_face_encoding, key):
    # Initialize Fernet with the provided key
    fernet = Fernet(key)
    
    # Decrypt the face encoding
    decrypted_face_encoding_str = fernet.decrypt(encrypted_face_encoding).decode('utf-8')
    
    # Split the decrypted string and convert back to floats
    face_encoding = list(map(float, decrypted_face_encoding_str.split(',')))
    
    return face_encoding