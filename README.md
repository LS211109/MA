# MA Hühnerstalltor


## Installieren
1. Unter https://thonny.org kann die Thonny IDE installiert werden, welche für dieses Projekt verwendet wurde. Es wären auch andere Programme möglich, jedoch ist Thonny das einzige Programm welches getestet wurde.
   
2. Unter https://github.com/LS211109/MA kann der gesammte Source Code gefunden werden. Folgende Dateien befinden sich dort:

* Main.py
* Config.py
* Htor.py
* System.py
* Stepper.py
* Operation.py
* Display.py
* Protection.py
* Timer.py
* Debounce.py
* Suncalculation.py
* RTC.py

3. Falls der gesammte Elektrische Aufbau mit allen Komponenten nachgebaut wird, muss auf dem Arduino GIGA R1 WiFi die Micropython Firmware installiert werden. Die passende Micropython Firmware für den Arduino GIGA R1 WiFi befindet sich hier: https://labs.arduino.cc/en/labs/micropython-installer

4. Der Arduino kann via USB-Kabel mit dem Computer verbunden werden.
   
5. In Thonny kann unter Ausführen > Konfiguriern sie den Interpreter, MicroPhyton als Art von Interpreter ausgewählt werden. Dort muss auch der passende Port ausgewählt werden.

6. Wenn der Arduino erfolgreich verbunden ist muss der Komplette Source Code auf den Arduino kopiert werden. Anschliessend kann die Datei main.py gestartet werden und wenn alles richtig zusammengebaut ist sollte alles Funktionieren.
