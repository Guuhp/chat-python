from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.lang import Builder
import requests
from PIL import Image
import io


IP="http://192.168.101.11:5000"
USER1=''
USER2=''
CODE_ROOM1=''
CODE_ROOM2=''

class JanelaGerenciador(ScreenManager):
  pass

class Ip(Screen):
  pass

class Home(Screen):
  pass

class CameraClick(Screen):
  pass

class SeePhoto(Screen):
  pass

class MeuAplicativo(App):
  def build(self):
    self.file = Builder.load_file("main.kv")
    return self.file

#==========================================================================================

  def ip(self):
    global IP
    IP = self.file.get_screen('ip').ids['inp_ip'].text
    print(IP)
    return    

#==========================================================================================

  def new_conversation(self):
    global USER1,CODE_ROOM1
    request=requests.get("http://"+IP+"/new_conversation")
    json = request.json()
    room_key = json['path']
    USER1="user1"
    CODE_ROOM1 = room_key
    self.file.get_screen('home').ids['idsala'].text=f'{room_key}'
    return  

#==========================================================================================

  def join_room(self):
    global USER2,CODE_ROOM2
    code_room=int(self.file.get_screen('home').ids["inpt_codigo_room"].text)
    code_room = {"data":code_room}
    response=requests.post("http://"+IP+"/join_room",json=code_room)
    message = response.json()
    if message['message'] ==True:
      print("resposta")
      code_room =int(self.file.get_screen('home').ids["inpt_codigo_room"].text)
      USER2="user2"
      CODE_ROOM2=code_room
    if message['message'] ==False:
      self.file.get_screen('home').ids['idsala'].text=f'codigo da sala inexistente'

#==========================================================================================

  def capture(self):
    global USER1,USER2,CODE_ROOM1,CODE_ROOM2    
    if USER1 == "user1":
        camera = self.file.get_screen('camera').ids['camera']
        camera.export_to_png("/sdcard/user1.png")
        self.file.get_screen('verfoto').ids['imguser'].source='/sdcard/user1.png'
        self.file.get_screen('verfoto').ids['imguser'].reload() 
        data = {"code_room":CODE_ROOM1,"user":"user1"}
        file = {'file':open('/sdcard/user1.png','rb')}
        requests.post("http://"+IP+"/new_message",files=file,data=data)

    if USER2 =="user2":
        camera = self.file.get_screen('camera').ids['camera']
        camera.export_to_png("/sdcard/user2.png")
        self.file.get_screen('verfoto').ids['imguser'].source='/sdcard/user2.png'
        self.file.get_screen('verfoto').ids['imguser'].reload() 
        data = {"code_room":CODE_ROOM2,"user":"user2"}
        file = {'file':open('/sdcard/user2.png','rb')}
        requests.post("http://"+IP+"/new_message",files=file,data=data)
        
#==========================================================================================
  
  def get_message(self):
    global USER1,USER2,CODE_ROOM1,CODE_ROOM2
    if USER1 =="user1":
        cod_room = {"cd_room":CODE_ROOM1,"user":"user1"}
        request=requests.post("http://"+IP+"/get_message",json=cod_room)
        print(request.content)
        image = Image.open(io.BytesIO(request.content))
        image.save(f'/sdcard/res2.png')
        image='/sdcard/res2.png'
        self.file.get_screen('home').ids['imguser'].reload() 
        self.file.get_screen('home').ids['imguser'].source = image   
        
    if USER2 =="user2":
        cod_room = {"cd_room":CODE_ROOM2,"user":"user2"}
        print(cod_room)
        request=requests.post("http://"+IP+"/get_message",json=cod_room)
        print(request.content)
        image = Image.open(io.BytesIO(request.content))
        image.save(f'/sdcard/res1.png')
        image='/sdcard/res1.png'
        self.file.get_screen('home').ids['imguser'].reload() 
        self.file.get_screen('home').ids['imguser'].source = image    

MeuAplicativo().run()