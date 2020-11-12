The program makes screenshots in background.

-------------------
1. How start?
-------------------
Start programm (it will create console screen) or start Start.vbs (it will prevent console screen and created automaticly)
You can create\edit start.vbs manually with code:
Set Shell = CreateObject("WScript.Shell")
Shell.Run """myssd.exe""", 0, False

You also may change file name, example screenshot.exe

-------------------
2. INI parameters
-------------------
Programm get parameters from INI file (if it doesnt exist, it will be create with default parameters)
Parameters:
screenshot_path - if empty then make folder and save screenshots in folder with programm, else create folder by path example - c:\tmp
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
