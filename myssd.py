import pyautogui
import os.path
import time
import configparser
import datetime
import random
import shutil


#Constants
CONST_BASENAME = 'myssd'
CONST_INI_FILE_NAME         = os.getcwd() + f'\\{CONST_BASENAME}.ini'
CONST_LOG_FILE_NAME         = os.getcwd() + f'\\{CONST_BASENAME}.log'
CONST_STOP_FILE_NAME        = os.getcwd() + '\\STOP.txt'
CONST_VBS_START_FILE_NAME   = os.getcwd() + '\\START.vbs'
CONST_VBS_STOP_FILE_NAME    = os.getcwd() + '\\STOP.vbs'
CONST_README_FILE_NAME      = os.getcwd() + '\\README.txt'

#endregion 

#Def
class Settings:
    waiting_sec: int
    max_screen: int
    screenshot_path: str

    def __init__(self):
        self.waiting_sec     = 5
        self.max_screen      = 10000
        self.screenshot_path = os.getcwd() #current path 

    #Validate values from ini 
    def validate(self):
        res = True
        res_msg = ''
        res_vals =dict()

        #Errors
        if self.waiting_sec <= 0 or self.max_screen <=0: 
            res = False
            res_msg = " ERROR: Parameter waiting_sec and max_screen must be > 0 , please set correct parameters in INI file > 0.\n"
        if self.screenshot_path:
            #screenshot_path not empty in INI file
            #Prev actions
            last_char = self.screenshot_path[-1]
            if last_char == '\\':
                #Delete last splash
                self.screenshot_path = self.screenshot_path[:-1]
            if not os.path.exists(self.screenshot_path):
                res = False
                res_msg += "ERROR: Parameter screenshot_path = " + self.screenshot_path + ". Path not exist! Set in INI file exist path for screenshot_path\n"
        else:
            #screenshot_path empty in INI file
            self.screenshot_path = os.getcwd() #current path 
        #Warnings
        if self.waiting_sec > 30:
            res_msg += "WARNING: Parameter waiting_sec > 30 it's mean screenshot will be done very seldom, please set waiting_sec in INI file 1-10.\n"
        if self.max_screen < 100:
            res_msg += "WARNING: Parameter max_screen < 100 it's very little, please set max_screen in INI file > 1000.\n"
        if self.max_screen > 500000:
            res_msg += "WARNING: Parameter max_screen > 500.000 it's a lot of pics, please set max_screen in INI file < 500000.\n"

        res_vals['res'] = res
        res_vals['msg'] = res_msg

        return res_vals


#Read values from ini file
def read_ini():
    s = Settings()
    cfg = configparser.RawConfigParser()
    cfg.read(CONST_INI_FILE_NAME)
    s.screenshot_path = cfg.get('DEFAULT', 'screenshot_path')
    s.waiting_sec = int(cfg.get('DEFAULT', 'waiting_sec'))
    s.max_screen  = int(cfg.get('DEFAULT', 'max_screen'))
    return s

#Create ini file if not exist
def create_ini():
    text = """[DEFAULT]
screenshot_path = 
waiting_sec     = 5
max_screen      = 10000
"""
    with open(CONST_INI_FILE_NAME, 'w+') as f:
        f.write(text)

    return 0

#Create readme file if not exist
def create_readme():
    text = """The program makes screenshots in background.

-------------------
1. How start?
-------------------
Start programm (it will create console screen) or start Start.vbs (it will prevent console screen and created automaticly)
You can create\edit start.vbs manually with code:
Set Shell = CreateObject("WScript.Shell")
Shell.Run \"\"\"myssd.exe\"\"\", 0, False

You also may change file name, example screenshot.exe

-------------------
2. INI parameters
-------------------
Programm get parameters from INI file (if it doesnt exist, it will be create with default parameters)
Parameters:
screenshot_path - if empty then make folder and save screenshots in folder with programm, else create folder by path example - c:\\tmp
waiting_sec - seconds between screenshots, example 5
max_screen - maximum number of screen to be done, example 10000

-------------------
3. How stop?
-------------------
Run STOP.vbs script (it create STOP.txt file) or create manually file STOP.txt in directory with running programm

-------------------
4. How get info about result after terminated.
-------------------
All info write into myssd.log file. 

-------------------
Algorithm:
-------------------
1. If not exist ini or readme or vbs then create it.
2. Create folder for screenshots:
    if parameter screenshot_path  = '' then create in current dir
    else create in parameter's directory, 
        if not exist then write to log and stop
3. If file STOP.txt exist then rename to _STOP.txt
4. Create screenshots in loop for max_screen with interval waiting_sec untill find file STOP.txt in current dir
5. If some error happens in previos item then script restart for max_screen times with interval 2 seconds
"""
    with open(CONST_README_FILE_NAME, 'w+') as f:
        f.write(text)

    return 0

#Create vbs file for start without console window
def create_vbs_start():
    text = f"""
Set Shell = CreateObject("WScript.Shell")
Shell.Run \"\"\"{CONST_BASENAME}\"\"\", 0, False
    """
    with open(CONST_VBS_START_FILE_NAME, 'w+') as f:
        f.write(text)
    return 0

def create_vbs_stop():
    text = f"""
Set fs = CreateObject("Scripting.FileSystemObject")
Set a = fs.CreateTextFile("STOP.txt", True)
"""
    with open(CONST_VBS_STOP_FILE_NAME, 'w+') as f:
        f.write(text)
    return 0

#Write to log
def add_log(s: str):
    res = True
    try:
        
        prev = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        s = prev + ": " + s + "\n"
        with open(CONST_LOG_FILE_NAME, 'a') as f:
            f.write(s)
        console(s)
    except:
        res = False

    return res

#-------------------
#MAIN PROGRAMM
#-------------------

#Vars
s: Settings
s = Settings()

# If happen some exception then trying max_screen times with a break of 2 seconds
i = 0
while i < s.max_screen:
    try:
        add_log('START') if i==0 else add_log('RESTART')

        #README file
        if not os.path.isfile(CONST_README_FILE_NAME):
            create_readme()
            add_log('CREATE README FILE')    

        #STOP file
        if i == 0:
            #IF first start then rename stop file to _STOP.txt because it's error probably
            if os.path.isfile(CONST_STOP_FILE_NAME):
                shutil.move(CONST_STOP_FILE_NAME, os.getcwd() + '\\_STOP.txt')
                add_log('Detect STOP.txt on first start. Rename to _end.txt and continue.')
        else:
            if os.path.isfile(CONST_STOP_FILE_NAME):
                add_log('Detect STOP.txt.')
                break
        
        #VBS start script
        if not os.path.isfile(CONST_VBS_START_FILE_NAME):
            add_log('Create start.vbs file for start without console screen.')
            create_vbs_start()

        #VBS stop script
        if not os.path.isfile(CONST_VBS_STOP_FILE_NAME):
            add_log('Create stop.vbs file for stop screen.')
            create_vbs_stop()
        
        #INI file
        if not os.path.isfile(CONST_INI_FILE_NAME):
            create_ini()
            add_log('CREATE INI FILE')
        s = read_ini()
        res_vals = s.validate()
        if i == 0:
            add_log(f'screenshot_path: {s.screenshot_path}')
            add_log(f'waiting_sec: {s.waiting_sec}')
            add_log(f'max_screen: {s.max_screen}')

        #Errors
        if not res_vals['res']:
            add_log(res_vals['msg'])
            break
        #Warnings
        if res_vals['msg']:
            add_log(res_vals['msg'])

        #Create folder for screenshot
        folder_name = datetime.datetime.now().strftime("myss_%d%m%Y_%H%M%S")
        screenshot_path = s.screenshot_path + "\\" + folder_name
        if os.path.exists(screenshot_path):
            screenshot_path = s.screenshot_path + "\\" + folder_name + str(random.randint(10,100))
        os.mkdir(screenshot_path)

        #Screenshots loop
        for j in range(s.max_screen):
            datetime_name = datetime.datetime.now().strftime("myss_%d%m%Y_%H%M%S")
            image_name = f'{screenshot_path}\{datetime_name}_{j}.png'
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(image_name) 
            if os.path.isfile(CONST_STOP_FILE_NAME):
                add_log('Detect STOP.txt.')
                add_log(f"Created {j+1} screenshots.")
                break
            time.sleep(s.waiting_sec)
        
        #Exit
        add_log('EXIT.')
        break
    except Exception as ex:
        add_log('ERROR: ' + str(ex) + " " + str(type(ex)) + " " + str(ex.args))
        time.sleep(2)
    i += 1
