##**Writing your first payload**

Now that we saw what the syntax of DuckyScripts is we can take a look into a simple payload.

REM My first payload

DELAY 500

GUI r

DELAY 500

STRING https://giphy.com/clips/AnimationOnFOX-the-simpsons-fox-foxtv-KpJ47gKe6b7v7xQyWj

DELAY 500

ENTER

As we saw in the documentation and the GIF, a payload is a piece of script that contains keystrokes combinations. Throughout these combinations, we can write payloads that can help us navigate, modify and see contents in a computer.

REM Creating a file

DELAY 500

GUI r

DELAY 500

STRING notepad.exe

DELAY 500

ENTER

DELAY 500

REM Until now we opened the notepad. Since Notepad 
you can insert code through couple STRING commands.

DELAY 500

REM Let's make a funny prank to our friends.

STRING @echo off

DELAY 500

ENTER

DELAY 500

STRING color 02

DELAY 500

ENTER

DELAY 500

STRING :start

DELAY 500

ENTER

DELAY 500

STRING  echo %random% %random% %random% %random% 
%random% %random% %random% %random% %random% 
%random%.

DELAY 500

ENTER

DELAY 500

STRING  goto start

DELAY 500

CTRL S

DELAY 500

STRING It is just a prank.bat

ENTER

DELAY 500

GUI

DELAY 500

STRING It is just a prank

DELAY 500

ENTER

####**The example payload that we just saw gives us an idea of the possibilities and usages of the payloads. They can vary from funny pranks we can do to our friends to malicious codes that can be executed. Please use the devices with responsibility! :)**
