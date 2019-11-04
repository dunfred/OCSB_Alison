#Author: Dunyo Fred
#Date Started:  11-02-2019

import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from PYTHON_OCSB import Automator

class OnlineCourseSkipBot(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.username.focus = True
    
    def validate_and_run(self):
        username    = self.ids.username
        password    = self.ids.password
        course_link = self.ids.link
        head_info   = self.ids.head_info
        info        = self.ids.info

        print(f"username {username.text}")
        print(f"password {password.text}")
        print(f"course_link {course_link.text}")
        #Check if user wants to login using google account
        if self.ids.google.active == True:
            Google_mode = True
        else:
            Google_mode = False

        #Check if user has filled every field
        if username.text == "" and password.text == "" and course_link.text == "":
            info.text = "[color=ff3333]Please fill all fileds![/color]"
            info.font_size = 12
            username.focus = True

        elif username.text == "" and password.text != "" and course_link.text != "":
            info.text = "[color=ff3333]The username filed is empty![/color]"
            info.font_size = 12
            username.focus = True

        elif username.text != "" and password.text == "" and course_link.text == "":
            info.text = "[color=ff3333]The Password and Course Url fields are empty![/color]"
            info.font_size = 12
            password.focus = True

        elif username.text != "" and password.text == "" and course_link.text != "":
            info.text = "[color=ff3333]The password filed is empty[/color]"
            info.font_size = 12
            password.focus = True

        elif username.text == "" and password.text != "" and course_link.text == "":
            info.text = "[color=ff3333]The Username and Course Url fields are empty![/color]"
            info.font_size = 12
            username.focus = True

        elif username.text != "" and password.text != "" and course_link.text == "":
            info.text = "[color=ff3333]Youb didn't specify a course url[/color]"
            info.font_size = 12
            course_link.focus = True
        
        elif username.text == "" and password.text == "" and course_link.text != "":
            info.text = "[color=ff3333]The Username and Password fields are empty![/color]"
            info.font_size = 12
            username.focus = True
        else:
            try:
                head_info.text = "[color=00ee00][u]Successfully Validated[/u][/color]"
                runtime_object = Automator(username.text, password.text, course_link.text, google_login_mode=Google_mode).goSkip()
            except Exception as err:
                head_info.text = f"[color=ff3333][u]Session Ended[/u][/color]"
    
    def exit(self):
        #App.get_running_app.stop()
        Window.close()

class OCSBApp(App):
    def build(self):
        return OnlineCourseSkipBot()


#if __name__ == '__main__':
OCSBApp().run()
