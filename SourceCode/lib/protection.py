from machine import Pin 
from lib.debounce import Debounce
from lib.config import PROTECTION_DEF


# KLASSE
# Welche die Sensorsignale zurückgibt
class Protection:

    # KONSTRUKTOR, Protection
    # Erstellen Pindefinition Sensor oben unten
    def __init__(self):
        # Objektreferenzen speichern
        self.__syst = None
        self.__step = None
        
        # Pins definieren
        self.__pin_in_Top = Debounce(PROTECTION_DEF["pin_sensor_top"],PROTECTION_DEF["debounce_time_ms"])
        self.__pin_in_Bot = Debounce(PROTECTION_DEF["pin_sensor_bot"],PROTECTION_DEF["debounce_time_ms"])
        self.__error_timeout = PROTECTION_DEF["error_timeout"]
        
        
    # METHODE
    # Zyklisches Update, welche die Sensorpostionen liest
    def update(self):
        # Aktueller Zustand der Sensoren lesen
        self.__pin_in_Top.update()
        self.__pin_in_Bot.update()


    # PROPERTY
    # Endschalter oben auf Position
    @property
    def door_in_open_pos(self):
        return self.__pin_in_Top.state_off


    # PROPERTY
    # Endschalter unten auf Position
    @property
    def door_in_close_pos(self):
        return self.__pin_in_Bot.state_off


    # PROPERTY
    # Error timeout
    @property
    def error_timeout(self):
        return self.__error_timeout

