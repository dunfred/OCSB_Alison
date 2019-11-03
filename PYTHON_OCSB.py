import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from main import OnlineCourseSkipBot

courses = {
            #"ms2010_Rev_2018"    : "https://alison.com/courses/microsoft-office-2010-revised-2018/",
            "dip_in_DB_and_TSQL" : "https://alison.com/course/diploma-in-databases-and-t-sql-revised",
            "ma2013_Advn_master" : "https://alison.com/course/microsoft-access-2013-advanced-master-databases",
            "ma2013_begginers"   : "https://alison.com/course/microsoft-access-2013-for-beginners-start-your-database-journey",
            "saylor_Into_to_MDS" : "https://learn.saylor.org/login/index.php",
        }

class Automator:
    def __init__(self, email, password, course_url, google_login_mode=False, *args, **kwargs):
        self.email              = email        
        self.password           = password        
        self.course_url         = course_url
        self.google_login_mode  = google_login_mode

        driver_path = "/home/dunfred/webdrivers/chromedriver"
        driver = webdriver.Chrome(driver_path)
        self.driver             = driver

    def goSkip(self):                
        self.driver.set_window_size(1024, 720)
        self.driver.maximize_window()

        self.driver.get(self.course_url)
        self.driver.implicitly_wait(60)
        
        login = self.driver.find_element_by_xpath('/html/body/header/div/div[3]/div[1]/a[2]').click()
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
            #login
            self.driver.implicitly_wait(20)
            try:
                g_email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)      
                self.driver.implicitly_wait(20)              

                g_password = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)


            except Exception as error:
                g_email = self.driver.find_element_by_xpath('//*[@id="Email"]')
                g_email.send_keys(self.email)
                g_email.send_keys(Keys.ENTER)
                #next_page = self.driver.find_element_by_xpath('//*[@id="identifierNext"]/div[2]').click()                                                    
                self.driver.implicitly_wait(20)

                g_password = self.driver.find_element_by_xpath('//*[@id="Passwd"]')
                g_password.send_keys(self.password)
                g_password.send_keys(Keys.ENTER)

            #Switch back
            count = 0
            while count < 1000:
                if not (login_page in self.driver.window_handles):
                    count += 1000
                else:
                    count += 1

            self.driver.implicitly_wait(20)
            self.driver.switch_to.window(main_page)               
            count = 0
    
        else:    
            usern_or_email = self.driver.find_element_by_xpath('//*[@id="login"]/div[3]/div[2]/div[2]/div/form/div[1]/input')
            usern_or_email.send_keys(self.email)

            paswrd = self.driver.find_element_by_xpath('//*[@id="login"]/div[3]/div[2]/div[2]/div/form/div[2]/input')
            paswrd.send_keys(self.password)
            paswrd.send_keys(Keys.ENTER)                 

        #Logged in successfuly
        time.sleep(10)
        self.driver.implicitly_wait(30)

        #Step one Find The Start Course/Continue Course Button
        self.driver.find_element_by_xpath('//*[@id="main-holder"]/div[1]/div/div[2]/div[2]/div[3]/div').click()
        while True:
            #Step two Start Topic
            try:
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath('//*[@id="bottom_bar_start_topic"]').click()
            except Exception:
                pass
            #Click next slide
            try:            
                self.driver.implicitly_wait(10)        
                self.driver.find_element_by_xpath('//*[@id="player-page"]/div[2]/a[4]').click()
            except Exception: 
                pass
            
            
        start_course = self.driver.find_element_by_xpath('//*[@id="top_button_right"]').send_keys(Keys.RETURN)
        #start_course = driver.find_element_by_css_cselector("#top_button_right").click()  
        
        start_topic_check = True
        next_slide_check = False
        next_topic_check = False 
            
        while True:
            try:
                if start_topic_check:           
                    self.driver.implicitly_wait(20)
                    start_topic = self.driver.find_element_by_xpath('//*[@id="player_button_right"]').click()
            except Exception:
                next_slide_check = True
            
            try:
                if next_slide_check:
                    self.driver.implicitly_wait(20)
                    next_slide = driver.find_element_by_xpath('//*[@id="butNext"]')
                    next_slide.click()
            except Exception:
                next_topic = True
                
            try:
                if next_topic:
                    driver.implicitly_wait(20)
                    self.driver.find_element_by_id("bottom_bar_next_topic").click()
                    #OnlineCourseSkipBot.ids.bar += 2
                    time.sleep(5)
            except Exception:
                start_topic_check = True
        
            try:
                self.driver.find_element_by_xpath('//*[@id="top_button"]').click()
                self.driver.find_element_by_link_text("Continue Learning").click()
            except Exception:
                pass

            


#bot_obj = Automator("benedictaegbenya18@gmail.com","seyram", google_login_mode=False)
#bot_obj = Automator("charleskp138@gmail.com","Itxcharlie@1", google_login_mode=False)       
#bot_obj.goSkip()

#print("End of program")





#correctAnswers = questionsToDisplay; initializeFinish();
#ScormProcessSetValue('cmi.core.lesson_ststus','completed');

