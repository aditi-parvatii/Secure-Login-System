import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import urllib.parse as up
import uuid
import bcrypt
import re
import base64

load_dotenv()

app = Flask(__name__)

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])
connection = psycopg2.connect(database=url.path[1:],
                              user=url.username,
                              password=url.password,
                              host=url.hostname,
                              port=url.port)
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS userlogin (
            user_id UUID PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()

@app.route("/createuser", methods=["POST"])
def createuser():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username is None or password is None:
        return jsonify({"error": "Username and password are required"}), 400
    
    cursor = connection.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM userlogin WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 409
    
    password_regex = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    username_regex= re.compile(r"[^-\s]")
    
    if not username_regex.match(username):
        error_message1= "Username must have some charaters"
        return jsonify({"message": error_message1}), 400

    if not password_regex.match(password):
        error_message = "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character"
        return jsonify({"message": error_message}), 400
    
    # Generate a unique UUID
    user_id = str(uuid.uuid4())

    # Encrypt the password using bcrypt
    salt=bcrypt.gensalt(rounds=15)
    bytes=password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes, salt)
    hashed_password_base64 = base64.b64encode(hashed_password).decode("utf-8")
    # Insert new user into the database
    cursor.execute("INSERT INTO userlogin (user_id, username, password) VALUES (%s, %s, %s)", (user_id, username,hashed_password_base64))
    connection.commit()

    cursor.close()

    return jsonify({"user_id": user_id}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username1 = data.get("username")
    password1 = data.get("password")

    if username1 is None or password1 is None:
        return jsonify({"error": "Username and password are required"}), 400
    
    cursor = connection.cursor()

    # Retrieve user's hashed password from the database
    cursor.execute("SELECT * FROM userlogin WHERE username = %s", (username1,))
    existinguser = cursor.fetchone()

    if existinguser:
        # Compare the hashed password
        hashed_password = existinguser[2]
        stored_hashed_password_bytes = base64.b64decode(hashed_password)
        if bcrypt.checkpw(password1.encode("utf-8"),stored_hashed_password_bytes):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Login unsuccessful, incorrect name or password"}), 401
    else:
        return jsonify({"error": "This username doesnt exist please register"}), 401

    cursor.close()

if __name__ == "__main__":
    app.run(debug=True)