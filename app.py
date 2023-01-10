from flask import Flask,jsonify,request,send_file
import random
import os
from PIL import Image
import io

app = Flask(__name__)
PATH="room"

@app.route("/new_conversation",methods=["GET"])
def new_conversation():
    room_key = random.randint(10,100)
    os.mkdir(f"{PATH}/{room_key}")
    path_folder = f'{PATH}/{room_key}'
    print(path_folder)
    return jsonify(path=room_key)

@app.route("/join_room",methods=["GET","POST"])
def join_room():
    if request.method =="POST":
        cod_room = request.json["data"]
        print(cod_room)
        NEWPATH = f'{PATH}/{cod_room}'
        if os.path.exists(NEWPATH):
            message = {"message":True}
            return jsonify(message)
        message = {"message":False}
        return jsonify(message)
    
@app.route("/new_message",methods=["POST"])
def new_message():
    path_picture = request.files['file']
    code_room = request.form.get('code_room')
    user = request.form.get('user')
    print(path_picture)
    print(code_room)
    print(path_picture)
    if user =="user1":
        picture = Image.open(io.BytesIO(path_picture.stream.read()))
        path = f"{PATH}/{code_room}/{user}.png"
        print(path)
        picture.save(path)
    if user =="user2":
        picture = Image.open(io.BytesIO(path_picture.stream.read()))
        path = f"{PATH}/{code_room}/{user}.png"
        picture.save(path)

    return

@app.route("/get_message",methods=["POST"])
def get_message():
    cod_room=request.json['cd_room']
    user=request.json['user']
    user=str(user)
    print(cod_room)
    print(user)
    if user =="user1":
        path=f"{PATH}/{cod_room}/user2.png"
        return send_file(path,'image/png')
    
    if user =="user2":
        path=f"{PATH}/{cod_room}/user1.png"
        print(path)  
        return send_file(path,'image/png')
    
    

if __name__=='__main__':
    app.run(debug=True)