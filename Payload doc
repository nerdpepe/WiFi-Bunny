## **Payloads in WifiBunny and 16Bunny**

Both devices carry and execute the same payloads. Payloads are written in Ducky Script.

#### **What is Ducky Script?**

Ducky Script is the payload language of Hak5 gear.

#### **How do we use the Duckyscripts in WifiBunny and 16Bunny?** 

WifiBunny and 16Bunny are two devices that use Arduino micro as the mainboard. Hacktricks uses its own converter from DuckyScripts to C files since that's the acceptable language of the Arduino boards. 

#### **How to write a simple payload in Bunny (HackTricks) devices?** 

Payloads are written in DuckyScript, to write scripts users can use any common ASCII text editor such as Notepad, nano, Sublime Text, Atom, VIM, etc. 

## **The syntax** 
DuckyScript is simple. Each command is given in a new line. Commands are case sensitive and all of them are written in ALL CAPS.

#### **REM** 

REM is a command that is the equivalent of the comment tag in other programming languages such as the # in Python or // in C++. 

REM This comment line it won't be executed. 

GUI r 

STRING cmd

ENTER 



#### **DELAY** 

DELAY kind of halts the execution of the script. This is needed to give some time to the computer to process the commands. With the delay, you need to select a value from 1-10000. The time is calculated as X(the value from 1 to 10000) ms (milliseconds) times 10. T=X\*10 ms

DELAY 500

REM Wait 5000ms before executing the next command.

#### **STRING**

STRING command will process the characters as a string type variable and use it as keyboard input. 

GUI r

DELAY 500

STRING notepad.exe

ENTER

DELAY 500

STRING Hello world!

#### **GUI** 
GUI command fires the Windows key or the SuperKey. 

GUI r 

REM emulates the Windows Key being held and pressing r. A window will pop up on the screen that is the Run menu. 

#### **ALT** 

ALT is a command that can take various options. 

ALT| END, ESC, ESCAPE, F1…F12, Single Char, SPACE, TAB. E.g ALT F4 command will close a window in Windows OS. 

#### **CTRL (CONTROL)**

CTRL| BREAK, PAUSE, F1…F12, ESCAPE, ESC, Single Char

CONTROL| BREAK, PAUSE, F1…F12, ESCAPE, ESC, Single Char

#### **EXTENDED COMMANDS**

These commands represent different keys that can be used in different shortcuts and operating system-specific functions include: 

BREAK or PAUSE

CAPSLOCK

DELETE

END

ESC or ESCAPE

HOME

INSERT

NUMLOCK

PAGEUP

PAGEDOWN

PRINTSCREEN

SCROLLOCK

SPACE

TAB

DELETE is one of the famous CTRL ALT DELETE combo.

![alt text](https://computergeeksnow.com/wp-content/uploads/2009/09/keyboard-gangs.jpg)


