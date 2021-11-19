#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *

##################      TEMPLATE     ######################
FILE1 = """#include "Keyboard.h"    

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
  // Begining the Keyboard stream
  Keyboard.begin();"""

FILE2 = """  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}"""

REM = "//"

DELAY1 = "delay("
DELAY2 = ");"

STRING1 = 'Keyboard.print(F("'
STRING2 = '"));'

REPEAT1 = "for(int i = 0; i < "
REPEAT2 = "; i++){"
REPEAT3 = "}"

keys  = ["GUI","WINDOWS","SHIFT","ALT","CONTROL","CTRL","DOWNARROW","DOWN","LEFTARROW","LEFT","RIGHTARROW","RIGHT","UPARROW","UP","CAPSLOCK","DELETE","END","ESC","ESCAPE","HOME","INSERT","PAGEUP","PAGEDOWN","PRINTSCREEN","SPACE","TAB","ENTER"]

GUI = WINDOWS = "KEY_LEFT_GUI"      #0 1
SHIFT = "KEY_LEFT_SHIFT"        #2
ALT = "KEY_LEFT_ALT"        #3
CONTROL = CTRL = "KEY_LEFT_CTRL"        #4 5
DOWNARROW = DOWN = "KEY_DOWN_ARROW"     #6 7
LEFTARROW = LEFT = "KEY_LEFT_ARROW"     #8 9
RIGHTARROW = RIGHT = "KEY_RIGHT_ARROW"      #10 11
UPARROW = UP = "KEY_UP_ARROW"       #12 13
#BREAK = PAUSE = "KEY_BREAK"
CAPSLOCK = "KEY_CAPS_LOCK"      #14
DELETE = "KEY_DELETE"       #15
END = "KEY_END"     #16
ESC = ESCAPE = "KEY_ESC"        #17 18
HOME = "KEY_HOME"       #19
INSERT = "KEY_INSERT"       #20
PAGEUP = "KEY_PAGE_UP"      #21
PAGEDOWN = "KEY_PAGE_DOWN"      #22
PRINTSCREEN = "206"     #23
SPACE = " "     #24
TAB = "KEY_TAB"     #25
ENTER = "KEY_RETURN"		#26

TYPEKEY1 = "typeKey("
TYPEKEY2 = ");"

KEYPRESS1 = "Keyboard.press("
KEYPRESS2 = ");"

RELEASE = "Keyboard.releaseAll();"




##################      GUI     ######################

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Duckyscript2Arduino')
        self.master.geometry('800x500')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TCommand1.TButton', font=('宋体',9))
        self.Command1 = Button(self.top, text='Export .ino file', command=self.Data_Process, style='TCommand1.TButton')
        self.Command1.place(relx=0.676, rely=0.336, relwidth=0.206, relheight=0.137)

        self.Text1Font = Font(font=('宋体',9))
        self.Text1 = scrolledtext.ScrolledText(self.top, font=self.Text1Font)
        self.Text1.place(relx=0.038, rely=0.112, relwidth=0.539, relheight=0.72)
        self.Text1.insert('1.0','')

        self.style.configure('TLabel3.TLabel', anchor='center', foreground='#646464', background='#E3E3E3', font=('宋体',9))
        self.Label3 = Label(self.top, text='Hacktricks 2021', style='TLabel3.TLabel')
        self.Label3.place(relx=0.154, rely=0.919, relwidth=0.693, relheight=0.048)

        self.style.configure('TLabel2.TLabel', anchor='center', font=('宋体',9))
        self.Label2 = Label(self.top, text='When you have finished typing the DuckyScript code, press the button below to generate the Arduino project file.', wraplength=300, style='TLabel2.TLabel')
        self.Label2.place(relx=0.602, rely=0.134, relwidth=0.373, relheight=0.137)

        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体',9))
        self.Label1 = Label(self.top, text='Input DuckyScript Code Here:', style='TLabel1.TLabel')
        self.Label1.place(relx=0.038, rely=0.045, relwidth=0.269, relheight=0.034)

        self.MainMenu = Menu(self.top, tearoff=0)

        self.Wenjian = Menu(self.MainMenu, tearoff=0)
        self.Wenjian.add_command(label='Exit', command=self.Exit_Cmd)
        self.MainMenu.add_cascade(menu=self.Wenjian, label='File')
        self.MainMenu.add_command(label='About', command=self.About_Cmd)
        self.top['menu'] = self.MainMenu

        self.style.configure('TLine1.TSeparator', background='#000000')
        self.Line1 = Separator(self.top, orient='horizontal', style='TLine1.TSeparator')
        self.Line1.place(relx=0.589, rely=0.538, relwidth=0.397, relheight=0.0028)

        self.style.configure('TCommand2.TButton', font=('宋体',9))
        self.Command2 = Button(self.top, text='Compile', command=self.Compile, style='TCommand2.TButton')
        self.Command2.place(relx=0.627, rely=0.695, relwidth=0.13, relheight=0.092)

        self.style.configure('TCommand3.TButton', font=('宋体',9))
        self.Command3 = Button(self.top, text='Upload', command=self.Upload, style='TCommand3.TButton')
        self.Command3.place(relx=0.819, rely=0.695, relwidth=0.13, relheight=0.092)



##################      CORE     ######################

class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
	def __init__(self, master=None):
		Application_ui.__init__(self, master)

	def Data_Process(self, event=None):
		text_content = self.Text1.get("0.0","end").split("\n")
		text_content.pop()
		#print(text_content)
		FILE = FILE1
		flag = 1   #Determine whether an error has occurred
		flag_repeat = 0		#REPEAT
		count = 0
		for line in text_content:
			if line:
				count += 1
				commands = line.split()
				if commands[0] == "REM":
					if(flag_repeat == 0):
						FILE += "\n" + "  " + REM + " ".join(commands[1:]) + "\n"
					else:
						#FILE += "\n" + "  " + REPEAT1 + str(flag_repeat) + REPEAT2 + "\n" + "    " + REM + " ".join(commands[1:]) + "\n" + "  " + REPEAT3 + "\n"
						FILE += "\n" + "  " + REM + " ".join(commands[1:]) + "\n"
						flag_repeat = 0
				elif commands[0] == "DELAY":
					if len(commands) != 2:
						flag = 0
						error_delay = "line " + str(count) + "; Invalid use of \"DELAY\": Too many arguments"
						messagebox.showwarning('Error',error_delay)
						break
					else:
						if(flag_repeat == 0):
							FILE += "\n" + "  " + DELAY1 + "".join(commands[1]) + DELAY2 + "\n"
						else:
							FILE += "\n" + "  " + REPEAT1 + str(flag_repeat) + REPEAT2 + "\n" + "    " + DELAY1 + "".join(commands[1]) + DELAY2 + "\n" + "  " + REPEAT3 + "\n"
							flag_repeat = 0
				elif commands[0] == "STRING":
					if(flag_repeat == 0):
						FILE += "\n" + "  " + STRING1 + " ".join(commands[1:]) + STRING2 + "\n"
					else:
						FILE += "\n" + "  " + REPEAT1 + str(flag_repeat) + REPEAT2 + "\n" + "    " + STRING1 + " ".join(commands[1:]) + STRING2 + "\n" + "  " + REPEAT3 + "\n"
						flag_repeat = 0
				elif commands[0] == "REPEAT":
					if len(commands) != 2:
						flag = 0
						error_repeat = "line " + str(count) + "; Invalid use of \"REPEAT\": Too many arguments"
						messagebox.showwarning('Error',error_repeat)
						break
					else:
						flag_repeat = commands[1]
				elif commands[0] in keys:
					if len(commands) > 1:
						for p in commands:
							if p == keys[0]:
								RESPONSE = GUI
							elif p == keys[1]:
								RESPONSE = WINDOWS
							elif p == keys[2]:
								RESPONSE = SHIFT
							elif p == keys[3]:
								RESPONSE = ALT
							elif p == keys[4]:
								RESPONSE = CONTROL
							elif p == keys[5]:
								RESPONSE = CTRL
							elif p == keys[6]:
								RESPONSE = DOWNARROW
							elif p == keys[7]:
								RESPONSE = DOWN
							elif p == keys[8]:
								RESPONSE = LEFTARROW
							elif p == keys[9]:
								RESPONSE = LEFT
							elif p == keys[10]:
								RESPONSE = RIGHTARROW
							elif p == keys[11]:
								RESPONSE = RIGHT
							elif p == keys[12]:
								RESPONSE = UPARROW
							elif p == keys[13]:
								RESPONSE = UP
							elif p == keys[14]:
								RESPONSE = CAPSLOCK
							elif p == keys[15]:
								RESPONSE = DELETE
							elif p == keys[16]:
								RESPONSE = END
							elif p == keys[17]:
								RESPONSE = ESC
							elif p == keys[18]:
								RESPONSE = ESCAPE
							elif p == keys[19]:
								RESPONSE = HOME
							elif p == keys[20]:
								RESPONSE = INSERT
							elif p == keys[21]:
								RESPONSE = PAGEUP
							elif p == keys[22]:
								RESPONSE = PAGEDOWN
							elif p == keys[23]:
								RESPONSE = PRINTSCREEN
							elif p == keys[24]:
								RESPONSE =  SPACE
							elif p ==  keys[25]:
								RESPONSE = TAB
							elif p ==  keys[26]:
								RESPONSE = ENTER
							elif len(p) == 1:
								RESPONSE = "'" + p + "'"
							else:
								flag = 0
								error_unknown = "line " + str(count) + "; Exist unknown argument, please check!"
								messagebox.showwarning('Error',error_unknown)
								break
							if(flag_repeat == 0):
								FILE += "\n" + "  " + KEYPRESS1 + RESPONSE + KEYPRESS2 + "\n"
							else:
								FILE += "\n" + "  " + REPEAT1 + str(flag_repeat) + REPEAT2 + "\n" + "    " + KEYPRESS1 + RESPONSE + KEYPRESS2 + "\n" + "  " + REPEAT3 + "\n"
								flag_repeat = 0
						FILE += "\n" + "  " + RELEASE + "\n"
					else:
						if commands[0] == keys[0]:
							RESPONSE = GUI
						elif commands[0] == keys[1]:
							RESPONSE = WINDOWS
						elif commands[0] == keys[2]:
							RESPONSE = SHIFT
						elif commands[0] == keys[3]:
							RESPONSE = ALT
						elif commands[0] == keys[4]:
							RESPONSE = CONTROL
						elif commands[0] == CTRL[5]:
							RESPONSE = CONTROL
						elif commands[0] == keys[6]:
							RESPONSE = DOWNARROW
						elif commands[0] == keys[7]:
							RESPONSE = DOWN
						elif commands[0] == keys[8]:
							RESPONSE = LEFTARROW
						elif commands[0] == keys[9]:
							RESPONSE = LEFT
						elif commands[0] == keys[10]:
							RESPONSE = RIGHTARROW
						elif commands[0] == keys[11]:
							RESPONSE = RIGHT
						elif commands[0] == keys[12]:
							RESPONSE = UPARROW
						elif commands[0] == keys[13]:
							RESPONSE = UP
						elif commands[0] == keys[14]:
							RESPONSE = CAPSLOCK
						elif commands[0] == keys[15]:
							RESPONSE = DELETE
						elif commands[0] == keys[16]:
							RESPONSE = END
						elif commands[0] == keys[17]:
							RESPONSE = ESC
						elif commands[0] == keys[18]:
							RESPONSE = ESCAPE
						elif commands[0] == keys[19]:
							RESPONSE = HOME
						elif commands[0] == keys[20]:
							RESPONSE = INSERT
						elif commands[0] == keys[21]:
							RESPONSE = PAGEUP
						elif commands[0] == keys[22]:
							RESPONSE = PAGEDOWN
						elif commands[0] == keys[23]:
							RESPONSE = PRINTSCREEN
						elif commands[0] == keys[24]:
							RESPONSE = SPACE
						elif commands[0] == keys[25]:
							RESPONSE = TAB
						elif commands[0] == keys[26]:
							RESPONSE = ENTER
						elif len(commands[0]) == 1:
							RESPONSE = "'" + commands[0] + "'"
						else:
							flag = 0
							messagebox.showwarning('Error','Exist unknown argument, please check!')
							break
						if(flag_repeat == 0):
							FILE += "\n" + "  " + TYPEKEY1 + RESPONSE + TYPEKEY2 + "\n"
						else:
							FILE += "\n" + "  " + REPEAT1 + str(flag_repeat) + REPEAT2 + "\n" + "    " + TYPEKEY1 + RESPONSE + TYPEKEY2 + "\n" + "  " + REPEAT3 + "\n"
							flag_repeat = 0
				else:
					flag = 0
					error_unknown = "line " + str(count) + "; Exist unknown argument, please check!"
					messagebox.showwarning('Error',error_unknown)
					break
			else:
				messagebox.showwarning('Error','Please enter the contents')
				flag = 0
				break

		FILE += FILE2
		if(flag == 1):
			filepath = filedialog.asksaveasfile(title='Select the location to save',filetypes=[("Arduino Project", ".ino")],defaultextension='.ino')
			#filepath = open(filepath.name + ".ino", 'w')
			#filepath.write(FILE)
			path_folder = filepath.name.split('.')[0]
			path_filename = path_folder.split('/')[-1] + ".ino" 
			if not os.path.exists(path_folder):
				os.makedirs(path_folder)
				filepath_new = path_folder + '/' + path_filename
				fo = open(filepath_new, "w")
				fo.write(FILE)
				messagebox.showinfo('Succeed','File created successfully')
				fo.close()
				filepath.close()
				os.remove(path_folder + ".ino") 
			else:
				filepath.close()
				os.remove(path_folder + ".ino") 
				messagebox.showwarning('Error','Exist a folder with the same name as the generated file, please change the name of the generated file!')


	def Exit_Cmd(self, event=None):
		exit(0)

	def About_Cmd(self, event=None):
		messagebox.showinfo('About','Duckyscript2Arduino V1.0')

	def Compile(self, event=None):
		filepath = filedialog.askdirectory(title='Select a directory')
		if(len(filepath) == 0):
			messagebox.showwarning('Error','Please select the correct path!')
		else:
			com_compile = 'arduino-cli.exe compile -b arduino:avr:leonardo -e ' + filepath
			p = os.popen(com_compile)
			if(p.readlines() == ['\n']):
				messagebox.showwarning('Error','Failed!')
			else:
				messagebox.showinfo('---','Succeed!')
		


	def Upload(self, event=None):
		filepath = filedialog.askdirectory(title='Select a directory')
		if(len(filepath) == 0):
			messagebox.showwarning('Error','Please select the correct path!')
		else:
			upload = 'arduino-cli.exe upload -b arduino:avr:leonardo ' + filepath
			p = os.popen(upload)
			print(p.readlines())
			if(p.readlines() == []):
				messagebox.showwarning('Error','Failed!')
			else:
				messagebox.showinfo('---','Succeed!')



if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
