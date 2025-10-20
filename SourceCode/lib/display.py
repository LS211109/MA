'''
Helferklasse für Display, wurde mit Hilfe von Microsoft Copilot generiert, damit die 2 Klassen von Git für das Display verwendet werden kann 

Eigne Methode
show_display, welche das Display für die aktuelle Betriebsart macht


'''


from lib.config import DISPLAY_DEF
from machine import I2C, Pin
from time import sleep
from lib.operation import Operation
from lib.operation import OperationModes

# KLASSE
# Displaysteuerung
class Display:
    
    # KONSTRUKTOR, einlesen Konfiguration, erstellen Displayobjekt
    def __init__(self):
        self.i2c = I2C(DISPLAY_DEF["i2c"])
        self.addr = DISPLAY_DEF["address"]
        self.num_lines = DISPLAY_DEF["num_lines"]
        self.num_columns = DISPLAY_DEF["num_columns"]
        self.backlight = 0x08
        self.ENABLE = 0x04
        self.init_lcd()
        
        # Marker
        self.__marker_op_mode = OperationModes.NONE
        self.____marker_old_var = None


    # METHODE
    # Objektreferenzen setzen, um Werte für Displayausgabe zu lesen
    def set_references(self, syst, rtc, timer, op):
        self.__syst = syst
        self.__rtc = rtc
        self.__timer = timer
        self.__op = op


    # METHODE
    # Intialiseren Display 
    def init_lcd(self):
        self.write_init_cmd(0x33)
        self.write_init_cmd(0x32)
        self.write_init_cmd(0x28)
        self.write_init_cmd(0x0C)
        self.write_init_cmd(0x06)
        self.clear()


    # METHODE
    def strobe(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.ENABLE | self.backlight]))
        sleep(0.0005)
        self.i2c.writeto(self.addr, bytes([(data & ~self.ENABLE) | self.backlight]))
        sleep(0.0001)

    #METHODE
    def write_four_bits(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))
        self.strobe(data)


    # METHODE
    def send(self, data, mode=0):
        high = mode | (data & 0xF0)
        low = mode | ((data << 4) & 0xF0)
        self.write_four_bits(high)
        self.write_four_bits(low)


    # METHODE
    def write_init_cmd(self, cmd):
        self.send(cmd, 0)


    # METHODE 
    def clear(self):
        self.send(0x01)
        sleep(0.002)


    # METHODE
    def putstr(self, string):
        for char in string:
            self.send(ord(char), 0x01)


    #METHODE
    def move_to(self, row, col):
        addr = col + 0x40 * row
        self.send(0x80 | addr)


    # METHODE
    # Ausgeben eines Texts auf dem Display, Übergabe Zeile und Text
    def writeDisplay(self,row,text,clearDisplay):
        if clearDisplay:
            self.clear()
        if (row ==1):
            self.move_to(0, 0)
        elif (row ==2):
            self.move_to(1, 0)
        self.putstr(text)


    # METHODE
    # Überprüfen ob Display funktioniert, Buchstabe A pro Segment abwechselnd schreiben
    def test_display(self):
        total_positions = self.num_columns * self.num_lines
        for pos in range(total_positions):
            # Ganze Anzeige löschen
            self.clear()
            # Berechnung von Zeile und Spalte (1-basiert)
            row = pos // self.num_columns + 1
            col = pos % self.num_columns + 1
            # Erzeuge String mit 'A' an gewünschter Position
            if row == 1:
                text = " " * (col - 1) + "A"
                self.writeDisplay(1, text, clearDisplay=False)
            elif row == 2:
                text = " " * (col - 1) + "A"
                self.writeDisplay(2, text, clearDisplay=False)
            # 500 ms warten
            sleep(0.5)

    def __write_at(self, row, pos, length, text):
        # Zeile von 1 und Spalte von 1 in 0-basierte Indizes umwandeln
        row_idx = row - 1
        pos_idx = pos - 1

        # Text auf die angegebene Länge kürzen oder falls zu kurz, auffüllen
        if len(text) == length:
            pass
        elif len(text) > length:
            text = text[:length]
        else:
            # Auffüllen mit Leerzeichen rechts
            text = text + ' ' * (length - len(text))

        # Position auf dem Display setzen
        self.move_to(row_idx, pos_idx)

        # Text schreiben
        self.putstr(text)
        

    # METHODE
    # Anzeigen aktuelle Betriebasrt, Informationen
    def show_display(self, act_op_mode, force=False):
        if (
            act_op_mode == OperationModes.NONE or
            act_op_mode == OperationModes.SETUP or
            act_op_mode == OperationModes.MANUAL
            ):   
                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()

                # Anzeigen OP-Mode
                self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())

        # SETUP: Einstellen Jahr
        elif (act_op_mode == OperationModes.SETUP_DATE_YEAR):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.year) or force:
                # Merken aktuelles Jahr
                self.__marker_old_var = self.__rtc.year   

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Jahr
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    self.__write_at(2, 1, 5, "Year:")
                
                # Anzeigen aktuelles Jahr
                self.__write_at(2, 11 , 4, f"{self.__rtc.year:04d}")
                
        # SETUP: Einstellen Monat
        elif (act_op_mode == OperationModes.SETUP_DATE_MONTH):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.month) or force:
                # Merken aktuelles Jahr
                self.__marker_old_var = self.__rtc.month   

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Monat
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    self.__write_at(2, 1, 6, "Month:")
                
                # Anzeigen aktuelles Monat
                self.__write_at(2, 14, 2, f"{self.__rtc.month:02d}")

        # SETUP: Einstellen Tag
        elif (act_op_mode == OperationModes.SETUP_DATE_DAY):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.day) or force:
                # Merken aktuelles Jahr
                self.__marker_old_var = self.__rtc.day   

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Tag
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    self.__write_at(2, 1, 4, "Tag:")
                
                # Anzeigen aktuelles Tag
                self.__write_at(2, 12, 2, f"{self.__rtc.day:02d}")

        # SETUP: Einstellen Stunden
        elif (act_op_mode == OperationModes.SETUP_TIME_HOUR):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.hour) or force:
                # Merken aktuelles Jahr
                self.__marker_old_var = self.__rtc.hour   

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Stunden
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    self.__write_at(2, 1, 8, "Stunden:")
                
                # Anzeigen aktuelles Stunden
                self.__write_at(2, 13, 2, f"{self.__rtc.hour:02d}")

        # SETUP: Einstellen Minuten
        elif (act_op_mode == OperationModes.SETUP_TIME_MINUTE):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.minute) or force:
                # Merken aktuelles Jahr
                self.__marker_old_var = self.__rtc.minute   

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Minuten
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    self.__write_at(2, 1, 8, "Minuten:")
                
                # Anzeigen aktuelle Minuten
                self.__write_at(2, 15, 2, f"{self.__rtc.minute:02d}")

        # SETUP: Einstellen Verzögerung Sonnenaufgang
        elif (act_op_mode == OperationModes.SETUP_DELAY_SUNRISE):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__syst.sunrise_delay) or force:
                # Merken aktuelle Verzögerung
                self.__marker_old_var = self.__syst.sunrise_delay
                
                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    # Anzeigen Text Min
                    self.__write_at(2, 5, 3, "Min")

                # Anzeigen Sonnenaufgang- Verzögerung
                self.__write_at(2, 1, 4, str(self.__syst.sunrise_delay))

        # SETUP: Einstellen Verzögerung Sonnenuntergang
        elif (act_op_mode == OperationModes.SETUP_DELAY_SUNSET):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__syst.sunset_delay) or force:
                # Merken aktuelle Verzögerung
                self.__marker_old_var = self.__syst.sunset_delay

                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                    # Anzeigen Text Min
                    self.__write_at(2, 5, 3, "Min")

                # Anzeigen Sonnenuntergang- Verzögerung
                self.__write_at(2, 1, 4, str(self.__syst.sunset_delay))


        # MANUELL: Tor öffnen
        elif (act_op_mode == OperationModes.MANUAL_OPEN_DOOR) or (act_op_mode == OperationModes.MANUAL_CLOSE_DOOR) or (act_op_mode == OperationModes.MANUAL_ENDLESS):
            if (self.__marker_op_mode != act_op_mode) or force:

                # Display nur löschen, falls Betriebasrt gewechselt hat
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()
                    # Anzeigen OP-Mode, Status
                    self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                

        elif (act_op_mode == OperationModes.AUTOMATIC):
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.minute) or force:
                # Merken aktuell Minuten
                self.__marker_old_var = self.__rtc.minute
                
                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()

                # Anzeigen OP-Mode, Uhrzeit, Datum
                self.__write_at(1, 1, self.num_columns, self.__op.getOpMode())
                self.__write_at(1, (self.num_columns-4), 5, self.__rtc.time)
                self.__write_at(2, (self.num_columns-9), 10, self.__rtc.date)

                # Anzeigen Sollzustand vom Tor
                if self.__timer.open_door:
                    self.__write_at(2, 1, 5, "open")
                else:
                    self.__write_at(2, 1, 5, "close")
                    

        elif (act_op_mode == OperationModes.AUTOMATIC_INFOS):       
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.minute) or force:
                # Merken aktuell Minuten
                self.__marker_old_var = self.__rtc.minute
                
                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()

                # Anzeigen Uhrzeit
                self.__write_at(1, (self.num_columns-4), 5, self.__rtc.time)
                
                # Anzeigen Sonnenaufgang
                self.__write_at(1, 1, 5, "up:")
                self.__write_at(1, 6, 5, self.__timer.open_door_time)
                
                # Anzeigen Sonnenuntergang
                self.__write_at(2, 1, 5, "down:")
                self.__write_at(2, 6, 5, self.__timer.close_door_time)


        elif (act_op_mode == OperationModes.ERROR):       
            if (self.__marker_op_mode != act_op_mode) or (self.__marker_old_var != self.__rtc.minute) or force:
                # Merken aktuell Minuten
                self.__marker_old_var = self.__rtc.minute
                
                # Display löschen, falls Betriebasrt gewechselt wurde
                if (self.__marker_op_mode != act_op_mode) or force:
                    self.clear()

                # Anzeigen Uhrzeit
                self.__write_at(1, (self.num_columns-4), 5, self.__rtc.time)
                
                # Anzeigen Sonnenaufgang
                self.__write_at(1, 1, 5, "Error")
                
                # Anzeigen Sonnenuntergang
                self.__write_at(2, 1, 12, "Please check")



        # Merken der letzten Betriebsart
        self.__marker_op_mode = act_op_mode
        

        

