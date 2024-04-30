from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/create-meeting", methods=['POST'])
def create_metting():
    try: 
        print(request.json)
        return jsonify({
            "message": "Meeting Created!",
            "meeting_name": request.json["meeting_name"], 
            "code": "ABCDEF"
        }), 200
    except:
        print("Error Processing Request")
        return jsonify({
            "message": "Error Procesing Request!"
        }), 500

if __name__ == "__main__":
    app.run("localhost",8080,debug=True)