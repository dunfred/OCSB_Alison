#Author:        Dunyo Fred
#Date Started:  11-02-2019

import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as sp
from selenium.webdriver.common.keys import Keys
driver_path = "/home/dunfred/webdrivers/chromedriver"

#All automation will be done with the help of a class 
class Automator:
    def __init__(self, email, password, course_url, google_login_mode=False, *args, **kwargs):
        
        #Initialize the neccessary parameters we will be using later in the code
        self.email              = email        
        self.password           = password        
        self.course_url         = course_url
        self.google_login_mode  = google_login_mode
        self.driver             = webdriver.Chrome(driver_path)        
    #The main automation function
    def goSkip(self):                
        #Set the browser window to fullscreen or Maximize the window
        self.driver.set_window_size(1024, 720)
        self.driver.maximize_window()
        #Open the course url link
        self.driver.get(self.course_url)
        self.driver.implicitly_wait(60)
        #Search for login button and click
        login = self.driver.find_element_by_xpath('/html/body/header/div/div[3]/div[1]/a[2]').click()
        #If user chooses to sign in using Google Account details (google_login_mode = True)
        #Use this method to login
        if self.google_login_mode:
            #Storing current window handle
            main_page = self.driver.current_window_handle
            self.driver.implicitly_wait(60)

            self.google_login = self.driver.find_element_by_xpath('//*[@id="login"]/div[3]/div[2]/div[1]/div[1]/div[2]/a').click()
            # changing the handles to access login page 
            for handle in self.driver.window_handles:
                if handle != main_page: 
                    login_page = handle 

            # change the control to signin page         
            self.driver.switch_to.window(login_page) 
            #Try below script for google first login template.
            #And when any error is returned try else code
            self.driver.implicitly_wait(30)
            try:
                g_email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)      
                self.driver.implicitly_wait(30)              

                g_password = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)


            except Exception as error:
                g_email = self.driver.find_element_by_xpath('//*[@id="Email"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)
                #next_page = self.driver.find_element_by_xpath('//*[@id="identifierNext"]/div[2]').click()                                                    
                self.driver.implicitly_wait(30)

                g_password = self.driver.find_element_by_xpath('//*[@id="Passwd"]')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)

            #Wait till google login widow closes and Switch back to default window
            count = 0
            while count < 1000:
                if not (login_page in self.driver.window_handles):
                    count += 1000
                else:
                    count += 1

            self.driver.implicitly_wait(20)
            self.driver.switch_to.window(main_page)               
            count = 0
            
        #login into google using script for second template
        else:    
            usern_or_email = self.driver.find_element_by_xpath('//*[@id="login"]/div[3]/div[2]/div[2]/div/form/div[1]/input')
            usern_or_email.send_keys(self.email)

            paswrd = self.driver.find_element_by_xpath('//*[@id="login"]/div[3]/div[2]/div[2]/div/form/div[2]/input')
            paswrd.send_keys(self.password)
            paswrd.send_keys(Keys.ENTER)                 

        #Logged in successfuly        
        print("Starting Beautiful soup")
        content_page = requests.get(self.course_url + "/content").content
        module_num = int(sp(content_page, "lxml").find('div', {"class":"info-amount"}).text)                
        print(f"\n\nNumber of Modules: {module_num}\n\n")
                                 
        #Step one Find The Start Course/Continue Course Button
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//*[@id="main-holder"]/div[1]/div/div[2]/div[2]/div[3]/div').click()
        time.sleep(10)  
        
        #The logic below tries to find an element and if this is successful,
        #the program clicks it and repeats the same search again else the next search below is fired
        while module_num > 0:
            #Step two Start Topic
            try:                
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath('//*[@id="bottom_bar_start_topic"]').click()
                print("Start Course Clicked")                         
            except Exception:                                                                                          
                #Click next slide 
                try:             
                    self.driver.implicitly_wait(5)
                    self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/a[4]').click()
                    print("Next Slide Clicked")    
                    pass  
                except Exception:                                                        
                    #Cick Continue Course                        
                    try:               
                        self.driver.implicitly_wait(5)                  
                        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[1]/div[2]/a').click()
                        print("Clicked Continue Course")  
                        module_num -= 1
                        print(f"Modules left: {module_num}")
                        pass  
                    except Exception:                                                                                                                        
                        try: 
                            #Switch to course assessment iframe window and run js script
                            print("Starting Assessment")
                            self.driver.implicitly_wait(10)
                            iframe =  self.driver.find_element_by_id("iframe")
                            self.driver.switch_to.frame(iframe)
                            self.driver.execute_script("document.getElementsByClassName('head')[0].scrollIntoView();")
                            print("Switched to assessment frame")

                            self.driver.implicitly_wait(10)
                            self.driver.find_element_by_id('start').click()
                            print("First Start Button Clicked")

                            self.driver.implicitly_wait(10)
                            self.driver.find_element_by_id('start2').click()
                            print("Second Start Button Clicked")

                            self.driver.execute_script("correctAnswers = questionsToDisplay; initializeFinish();")

                            self.driver.implicitly_wait(10)
                            ass_finish =  self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div[2]/a[1]').click()
                            self.driver.switch_to.default_content()
                            print("Pass Assessment was successful")
                        except Exception:                   
                            self.driver.switch_to.default_content()                                     
                            print('Assessment Failed')
                            
    
bot_obj = Automator("exp@gmail.com","****", course_link(Als), google_login_mode=False).goSkip()
print("done!")

