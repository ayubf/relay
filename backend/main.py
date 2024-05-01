from flask import Flask, request, jsonify
from datetime import datetime, timedelta 
import bcrypt 
import psycopg2
import string 
import random 

app = Flask(__name__)
db = psycopg2.connect(database="relaydb",
                      host="localhost",
                      user="postgres",
                      password="postgres",
                      port="5432")

cursor = db.cursor()
commands = {
    "create_meeting": '''INSERT INTO meetings(meeting_name, code, expiration_time) VALUES (%s,%s, %s);''',
    "signup": '''INSERT INTO users(username, pwd) VALUES (%s, %s);''', 
    "login": '''SELECT username, pwd FROM users WHERE username=%s;'''
}
code_gen = lambda n: ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
expiration_time = lambda m: (datetime.today() + timedelta(minutes=m)).strftime('%Y-%m-%d %H:%M:%S')
salt = bcrypt.gensalt() 

@app.route("/signup", methods=['POST'])
def signup():
    try: 
        print(request.json)
        cursor.execute(commands["login"], (request.json["username"],))
        res = cursor.fetchall()
        if res != []: return jsonify({
            "message": "User Already Exists"
        }), 403
        password = bcrypt.hashpw(request.json["password"].encode("utf-8"), salt)
        cursor.execute(commands["signup"], (request.json["username"], password.decode("utf-8")))
        db.commit()
        return jsonify({
            "message": "User Created!",
            "username": request.json['username']
        }), 200
    except:
        print("Error Processing Request")
        return jsonify({
            "message": "Error Processing Request"
        }), 500
    
@app.route("/login", methods=['POST'])
def login():
    try:
        print(request.json)
        cursor.execute(commands['login'], (request.json['username'],))
        res = cursor.fetchall()
        if res == []: return jsonify({
            "message": "Username Or Password Was Incorrect"
        }), 403 
        _, pwd = res[0]
        if bcrypt.checkpw(request.json["password"].encode('utf-8'), pwd.encode('utf-8')):
            return jsonify({
                "message": "Login Was Successful!"
            }), 200 
        else:
            return jsonify({
                "message":"Username Or Password Was Incorrect"
            }), 403
    except:
        print("Error Processing Request")
        return jsonify({
            "message": "Error Processing Request"
        }), 500

@app.route("/create-meeting", methods=['POST'])
def create_metting():
    try: 
        print(request.json)
        cursor.execute(commands["create_meeting"], (request.json["meeting_name"], code_gen(6), expiration_time(request.json["minutes"])))
        db.commit()
        return jsonify({
            "message": "Meeting Created!",
            "meeting_name": request.json["meeting_name"], 
            "code": "ABCDEF"
        }), 200
    except:
        print("Error Processing Request")
        return jsonify({
            "message": "Error Procesing Request"
        }), 500

if __name__ == "__main__":
    app.run("localhost",8080,debug=True)