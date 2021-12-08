# WiFi-Bunny
Harmless looking HID through which we can execute scripts.

> 16Bunny - Attacker works with dip-switch and runs different scripts according to the input chosen.

> WiFi-Bunny - Once this device is connected to the target's system, attacker connects to the WiFi network and can execute scripts remotely.

We use Ducky Script language to write the scripts.

> How do we use the Duckyscripts in WifiBunny and 16Bunny?

WifiBunny and 16Bunny are two devices that use Arduino micro as the mainboard. Hacktricks uses its own converter from DuckyScripts to C files since that's the acceptable language of the Arduino boards.

> How to write a simple payload in Bunny (HackTricks) devices?

Payloads are written in DuckyScript, to write scripts users can use any common ASCII text editor such as Notepad, nano, Sublime Text, Atom, VIM, etc.

---

### Duckyscript to Arduino Convertor

Hacktricks has made it's own convertor - which converts the scripts in Ducky Script language to Arduino code which can then be used for programming the device.

![DuckyscriptArduino](https://github.com/nerdpepe/WiFi-Bunny/blob/main/media/web-convertor.png)

User can paste the script and export the Arduino Code

---

### 16Bunny

![DuckyscriptArduino](https://github.com/nerdpepe/WiFi-Bunny/blob/main/media/Dip-switch_55.png)

> Attacker connects this device to target's system. 
>
> With the help of switches (and based on the corresponding combination), the appropriate script gets executed.

---

### WiFi Bunny

![WifiBunny](https://github.com/nerdpepe/WiFi-Bunny/blob/main/media/WiFi-bunny.png)

> Attacker connects this device to the target's system.

> Attacker connects to the device's WiFi network

> Scripts can be stored and executed from any remote device connected to the WiFi network.

### Web Interface 

![FinalVersion](https://github.com/nerdpepe/WiFi-Bunny/blob/main/media/web-interface-2.png)

> Status : Shows the current connection status of the device

> Scripts : The list of scripts currently stored in the device

> Editor : User can write , save and run ducky scripts on the target's system.

