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
CDROOM1=''
CDROOM2=''

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
    return    

#==========================================================================================

  def new_conversation(self):
    global USER1,CDROOM1
    request=requests.get("http://"+IP+"/new_conversation")
    json = request.json()
    room_key = json['path']
    USER1="user1"
    CDROOM1 = room_key
    print(CDROOM1)
    self.file.get_screen('home').ids['idsala'].text=f'{room_key}'
    return  

#==========================================================================================

  def join_room(self):
    global USER2,CDROOM2
    cd_room=int(self.file.get_screen('home').ids["inpt_codigo_room"].text)
    cod_room = {"data":cd_room}
    print(cod_room)
    response=requests.post("http://"+IP+"/join_room",json=cod_room)
    message = response.json()
    if message['message'] ==True:
      print("resposta")
      cod_room =int(self.file.get_screen('home').ids["inpt_codigo_room"].text)
      USER2="user2"
      CDROOM2=cd_room
      print(CDROOM2)
    if message['message'] ==False:
      self.file.get_screen('home').ids['idsala'].text=f'codigo da sala inexistente'

  def capture(self):
    global USER1,USER2,CDROOM1,CDROOM2    
    if USER1 == "user1":
        camera = self.file.get_screen('camera').ids['camera']
        camera.export_to_png("/sdcard/user1.png")
        data = {"code_room":CDROOM1,"user":"user1"}
        print(data)
        file = {'file':open('/sdcard/user1.png','rb')}
        requests.post("http://"+IP+"/new_message",files=file,data=data)

    if USER2 =="user2":
        camera = self.file.get_screen('camera').ids['camera']
        camera.export_to_png("/sdcard/user2.png")
        data = {"code_room":CDROOM2,"user":"user2"}
        file = {'file':open('/sdcard/user2.png','rb')}
        requests.post("http://"+IP+"/new_message",files=file,data=data)
  def get_message(self):
    global USER1,USER2,CDROOM1,CDROOM2
    if USER1 =="user1":
        cod_room = {"cd_room":CDROOM1,"user":"user1"}
        request=requests.post("http://"+IP+"/get_message",json=cod_room)
        image = Image.open(io.BytesIO(request.content))
        image.save(f'res2.png')
        image='res2.png'
        self.file.get_screen('home').ids['imguser'].reload() 
        self.file.get_screen('home').ids['imguser'].source = image   
        
    if USER2 =="user2":
        cod_room = {"cd_room":CDROOM2,"user":"user2"}
        print(cod_room)
        request=requests.post("http://"+IP+"/get_message",json=cod_room)
        image = Image.open(io.BytesIO(request.content))
        image.save(f'res1.png')
        image='res1.png'
        self.file.get_screen('home').ids['imguser'].reload() 
        self.file.get_screen('home').ids['imguser'].source = image    

MeuAplicativo().run()