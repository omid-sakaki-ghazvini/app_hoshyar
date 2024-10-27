from kivyir import *
config = Config()
config.change(
    direction='rtl',
    # font_name='Sahel',
    # file_regular='{path}.ttf',
    # file_bold='{path}.ttf',
    # file_italic='{path}.ttf',
    # file_bolditalic='{path}.ttf'
)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import easyocr
import cv2
import matplotlib.pyplot as plt
import os
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.logger import Logger
import webbrowser

#Window.clearcolor = (1, 1, 0, 0)
Window.size = (350, 400)

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""                                      
<windowManager>:
      mgr:my_lay
      lgr:sc_lay           
      MyLayout:
            id:my_lay 
      secondLayout:
            id:sc_lay
            
                    
<MyLayout>
      name:"MyLayout"
      web_cam:web_cam
      btn_photo:btn_photo
      orientation:"vertical"             
      Image:
            id:web_cam 
            size_hint:1,1
      Button:
            id:btn_photo
            text:"عکس بگیرید"
            on_release:root.manager.verify(root);root.manager.current="secondLayout"
            size_hint:1,.1                                          
                                                    



<secondLayout>
      name:"secondLayout"
      input_img:input_img
      btn_link:btn_link
      btn_back:btn_back
      orientation:"vertical"
      Image:
            id:input_img 
            size_hint:1,1              
      GridLayout:
            cols:2
            spacing:10
            padding:10 
            size_hint:1,.2     
            Button:
                  id:btn_back
                  text:"برگشت"
                  on_release:root.manager.current="MyLayout"                                          
            Button:
                  id:btn_link
                  text:"link"
                  
                    
                    """)

def for_python(instance):
        webbrowser.open("https://omidsakaki.ir/Educations") 

def for_education(instance):
        webbrowser.open("https://omidsakaki.ir/Practices")

def for_practices(instance):
        webbrowser.open("https://omidsakaki.ir")               

class windowManager(ScreenManager):
    mgr = ObjectProperty(None)
    lgr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(windowManager, self).__init__(**kwargs)
        # save a reference to the event
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self,*args):

        # Read frame from opencv
        ret, frame = self.capture.read()
        frame = frame[150:150+250, 200:200+250, :]

        # Flip horizontall and convert image to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        #self.web_cam.texture = img_texture
        MDApp.get_running_app().root.mgr.web_cam.texture = img_texture


    def verify(self, root):

        # Capture input image from our webcam
        SAVE_PATH = os.path.join('application_data', 'input_image', 'input_image.jpg')
        ret, frame = self.capture.read()
        frame = frame[120:120+250, 200:200+250, :]
        cv2.imwrite(SAVE_PATH, frame)

        img = cv2.imread(os.path.join('application_data', 'input_image', 'input_image.jpg'))

        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        MDApp.get_running_app().root.lgr.input_img.texture = img_texture

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB format
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        #img = cv2.imread("image7.jpg")

        reader = easyocr.Reader(['en'])
        result = reader.readtext(rgb_frame)
        my_list = []
        for i in result:
            i = list(i)
            i = i[1].lower()
            my_list.append(i)  

        def search(doc, keyword):
                ind=[]
                for i,j in enumerate(doc):
                    tokens = j.split()
                    normal = [token.lower() for token in tokens]
                    if keyword.lower() in normal:
                        ind.append(i)
                return(ind)
    
        def multi_search(doc, keywords):
                    ind = {}
                    for i in keywords:
                        ind[i] = search(doc, i)
                        
                    return(ind)    

        list_value = multi_search(my_list, ['python','numpy','pandas','scipy', 'for','while', 'if', 'list', 'dict', 'set', 'tuple','zip', 'map', 'lambda', 'enumerate', 'file', 'try', 'str', 'bool', 'int', 'float'])

        def topic_value(my_dict):
            my_list = list(my_dict.items())

            result_list = []

            for i in my_list:
                a = i[0]
                b = len(i[1])
                result_list.append((a,b)) 

            temp = result_list[0]
            for i in range(len(result_list)):
                if temp[1]< result_list[i][1]:
                    temp = result_list[i]
            return(temp) 


        x = topic_value(list_value)[0]

        if x == 'python' or 'for' or 'list' or 'set' or 'zip':
             MDApp.get_running_app().root.lgr.btn_link.text = 'لینک آموزش'
             MDApp.get_running_app().root.lgr.btn_link.bind(on_press=for_python)
        elif x == 'numpy' or 'pandas' or 'scipy':
             MDApp.get_running_app().root.lgr.btn_link.text = 'لینک آموزش'
             MDApp.get_running_app().root.lgr.btn_link.bind(on_press=for_education)
        else:
             MDApp.get_running_app().root.lgr.btn_link.text = 'لینک آموزش'
             MDApp.get_running_app().root.lgr.btn_link.bind(on_press=for_practices)

  



                       


        # Log out details
        Logger.info(my_list)
        Logger.info(list_value)
                
         
     
class MyLayout(Screen):
      web_cam = ObjectProperty(None)
      btn_photo = ObjectProperty(None)
      
      


class secondLayout(Screen):
    input_img = ObjectProperty(None)
    btn_link = ObjectProperty(None)
    btn_back = ObjectProperty(None)


class HoshYarApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.icon="favicon.png"
        return windowManager()
    


if __name__ == '__main__':
    HoshYarApp().run()