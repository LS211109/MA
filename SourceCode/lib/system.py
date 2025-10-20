import machine
import os

from lib.config import PROJECT_NAME
from lib.config import PROJECT_AUTHOR
from lib.debounce import Debounce
from lib.config import OPERATION_DEF
from lib.config import PROJECT_NAME
from lib.config import PROJECT_AUTHOR
from lib.rtc import Rtc


# KLASSE
# Filehandling, Tasten S3 und S4 verwalten, Methoden um Werte im System anzupassen
class System:

    # KONSTRUKTOR für System
    def __init__(self):
        # Pins definieren
        self.pin_in_T3 = Debounce(OPERATION_DEF["pin_s3"],OPERATION_DEF["debounce_time_ms"])
        self.pin_in_T4 = Debounce(OPERATION_DEF["pin_s4"],OPERATION_DEF["debounce_time_ms"])
        self.project_name = PROJECT_NAME
        self.project_author = PROJECT_AUTHOR
        
        # Interne Variablen
        self.__delay_sunrise = 0
        self.__delay_sunset = 0
        
        # File-Handling
        self.__filename = "variables.txt"
        self.__load_variables_from_file()


    # PROPERTY
    # Delay für Sonnenaufgang, Rückgabe Minuten
    @property
    def sunrise_delay(self):
        return self.__delay_sunrise


    # PROPERTY
    # Delay für Sonnenuntergnag, Rückgabe Minuten
    @property
    def sunset_delay(self):
        return self.__delay_sunset


    # METHODE
    # Objektreferenzen setzen
    def set_references(self, step, rtc):
        self.__step = step
        self.__rtc = rtc
        

    # METHODE
    # Zyklisches Update, ewinlesen der Taster
    def update(self):
        self.pin_in_T3.update()
        self.pin_in_T4.update()


    # METHODE
    # RTC-Uhr anzupassen: JAHR
    def change_rtc_year(self):
        if self.pin_in_T3.state_down:
            self.__rtc.year = self.__change_value(self.__rtc.year, 1, 2020, 2065)
        elif self.pin_in_T4.state_down:
            self.__rtc.year = self.__change_value(self.__rtc.year, -1, 2020, 2065)


    # METHODE
    # RTC-Uhr anzupassen: MONAT
    def change_rtc_month(self):
        if self.pin_in_T3.state_down:
            self.__rtc.month = self.__change_value(self.__rtc.month, 1, 1, 12)
        elif self.pin_in_T4.state_down:
            self.__rtc.month = self.__change_value(self.__rtc.month, -1, 1, 12)


    # METHODE
    # RTC-Uhr anzupassen: TAG
    def change_rtc_day(self):
        if self.pin_in_T3.state_down:
            self.__rtc.day = self.__change_value(self.__rtc.day, 1, 1, 31)
        elif self.pin_in_T4.state_down:
            self.__rtc.day = self.__change_value(self.__rtc.day, -1, 1, 31)


    # METHODE
    # RTC-Uhr anzupassen: STUNDEN
    def change_rtc_hour(self):
        if self.pin_in_T3.state_down:
            self.__rtc.hour = self.__change_value(self.__rtc.hour, 1, 0, 23)
        elif self.pin_in_T4.state_down:
            self.__rtc.hour = self.__change_value(self.__rtc.hour, -1, 0, 23)


    # METHODE
    # RTC-Uhr anzupassen: MINUTEN
    def change_rtc_minute(self):
        if self.pin_in_T3.state_down:
            self.__rtc.minute = self.__change_value(self.__rtc.minute, 1, 0, 59)
        elif self.pin_in_T4.state_down:
            self.__rtc.minute = self.__change_value(self.__rtc.minute, -1, 0, 59)


    # METHODE
    # Sonnenaufgangverzögerung ändern
    def change_sunrise_delay(self):
        if self.pin_in_T3.state_down:
            self.__delay_sunrise = self.__change_value(self.__delay_sunrise, 10, -120, 120)
            self.__save_variables_to_file()
        elif self.pin_in_T4.state_down:
            self.__delay_sunrise = self.__change_value(self.__delay_sunrise, -10, -120, 120)
            self.__save_variables_to_file()


    # METHODE
    # Sonnenuntergangverzögerung ändern
    def change_sunset_delay(self):
        if self.pin_in_T3.state_down:
            self.__delay_sunset = self.__change_value(self.__delay_sunset, 10, -120, 120)
            self.__save_variables_to_file()
        elif self.pin_in_T4.state_down:
            self.__delay_sunset = self.__change_value(self.__delay_sunset, -10, -120, 120)
            self.__save_variables_to_file()


    # METHODE
    # Hlfsmethode, um einen Wert um einen Schritt zu ändern. Es werden Min und Max berücksichtigt
    def __change_value(self, value, step, min_val, max_val):
        value += step 
        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val
        return value
    
    
    # METHODE
    # Speichern von Werten in das Filesystem vom Arduino
    def __save_variables_to_file(self):
        print(os.listdir())
        with open(self.__filename, "w") as f:
            # Werte als Text speichern, bool als 0 (False) oder 1 (True)
            f.write(
                f"{self.__delay_sunrise}, "
                f"{self.__delay_sunset}\n"
            )


    # METHODE
    # Lesen von gespeicherten Werten
    def __load_variables_from_file(self):
        if self.__filename in os.listdir():
            print("Vars loaded")
            with open(self.__filename, "r") as f:
                line = f.readline()
                values = line.strip().split(",")
                if len(values) == 2:
                    self.__delay_sunrise = int(values[0])
                    self.__delay_sunset = int(values[1])
        else:
            print("No vars loaded")
            self.__delay_sunrise = 0
            self.__delay_sunset = 0


