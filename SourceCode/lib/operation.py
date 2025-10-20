from machine import Pin 
from lib.debounce import Debounce
from lib.config import OPERATION_DEF
from lib.config import START_OPMODE_AUTOMATIC

# KLASSE
# Definition der verschiedenen Betriebasrten
# Micropython unterstützt Enum nicht
class OperationModes:
    # Betriebsarten
    NONE = 0

    SETUP = 100
    SETUP_DATE_YEAR = 101
    SETUP_DATE_MONTH = 102
    SETUP_DATE_DAY = 103
    SETUP_TIME_HOUR = 104
    SETUP_TIME_MINUTE = 105
    SETUP_DELAY_SUNSET = 106
    SETUP_DELAY_SUNRISE = 107

    MANUAL = 200
    MANUAL_OPEN_DOOR = 201
    MANUAL_CLOSE_DOOR = 202
    MANUAL_ENDLESS = 203
    
    AUTOMATIC = 300
    AUTOMATIC_INFOS = 301

    ERROR = 400

# KLASSE
# Welche für die Betriebarten zustädig ist
class Operation:
    
    # KONSTRUKTOR, Operation
    # Übergabe Pindefinition T1_Betriebsart, T2_Subbetriebsart
    def __init__(self):
        # Pins definieren
        self.__pin_in_T1 = Debounce(OPERATION_DEF["pin_s1"],OPERATION_DEF["debounce_time_ms"])
        self.__pin_in_T2 = Debounce(OPERATION_DEF["pin_s2"],OPERATION_DEF["debounce_time_ms"])
  
        # Start OP-Mode definieren
        if START_OPMODE_AUTOMATIC:
            self.__act_op_mode = OperationModes.AUTOMATIC
        else:
            self.__act_op_mode = OperationModes.NONE
        self.__op_mode_changed = False


    # PROPERTY
    # Aktuelle Betriebsart, Typ OperationModes
    @property
    def act_op_mode(self):
        return self.__act_op_mode
    
    
    # PROPERTY
    # Trigger, welcher gesetzt wird, wenn die Betriebsart gewechselt hat  
    @property
    def op_mode_changed(self):
        return self.__op_mode_changed


    # METHODE
    # Zyklisches Update, welches gegebenenfalls die Betriebsart wechselt
    def update(self):
        # Aktueller Zustand der Tasten lesen
        self.__pin_in_T1.update()
        self.__pin_in_T2.update()

        #Überprüfen und ev. Wechseln vom OP-Mode
        self.__changeOp()


    # METHODE
    # Wechseln der Betriebsart, falls Taste gedrückt
    def __changeOp(self):
        # Merker, aktuelle Betriebsart, bevor gewechselt
        old_op_mode = self.__act_op_mode
        #Status der zwei Tasten lesen
        pinT1 = self.__pin_in_T1.state_down
        pinT2 = self.__pin_in_T2.state_down

        # Keine Betriebsart
        if self.__act_op_mode == OperationModes.NONE or self.__act_op_mode == OperationModes.ERROR:
            if pinT1:
                self.__act_op_mode = OperationModes.SETUP

        # Betriebsart Setup
        elif (self.__act_op_mode == OperationModes.SETUP or
            self.__act_op_mode == OperationModes.SETUP_DATE_YEAR or
            self.__act_op_mode == OperationModes.SETUP_DATE_MONTH or
            self.__act_op_mode == OperationModes.SETUP_DATE_DAY or
            self.__act_op_mode == OperationModes.SETUP_TIME_HOUR or
            self.__act_op_mode == OperationModes.SETUP_TIME_MINUTE or
            self.__act_op_mode == OperationModes.SETUP_DELAY_SUNRISE or
            self.__act_op_mode == OperationModes.SETUP_DELAY_SUNSET):
            if pinT1:
                self.__act_op_mode = OperationModes.MANUAL
            elif pinT2:
                if self.__act_op_mode == OperationModes.SETUP:
                    self.__act_op_mode = OperationModes.SETUP_DATE_YEAR
                elif self.__act_op_mode == OperationModes.SETUP_DATE_YEAR:
                    self.__act_op_mode = OperationModes.SETUP_DATE_MONTH
                elif self.__act_op_mode == OperationModes.SETUP_DATE_MONTH:
                    self.__act_op_mode = OperationModes.SETUP_DATE_DAY
                elif self.__act_op_mode == OperationModes.SETUP_DATE_DAY:
                    self.__act_op_mode = OperationModes.SETUP_TIME_HOUR
                elif self.__act_op_mode == OperationModes.SETUP_TIME_HOUR:
                    self.__act_op_mode = OperationModes.SETUP_TIME_MINUTE
                elif self.__act_op_mode == OperationModes.SETUP_TIME_MINUTE:
                    self.__act_op_mode = OperationModes.SETUP_DELAY_SUNRISE
                elif self.__act_op_mode == OperationModes.SETUP_DELAY_SUNRISE:
                    self.__act_op_mode = OperationModes.SETUP_DELAY_SUNSET
                elif self.__act_op_mode == OperationModes.SETUP_DELAY_SUNSET:
                    self.__act_op_mode = OperationModes.SETUP_DATE_YEAR
      
        # Betriebsart Hand
        elif (self.__act_op_mode == OperationModes.MANUAL or
            self.__act_op_mode == OperationModes.MANUAL_OPEN_DOOR or
            self.__act_op_mode == OperationModes.MANUAL_CLOSE_DOOR or
            self.__act_op_mode == OperationModes.MANUAL_ENDLESS):
            if pinT1:
                self.__act_op_mode = OperationModes.AUTOMATIC
            elif pinT2:
                if self.__act_op_mode == OperationModes.MANUAL:
                    self.__act_op_mode = OperationModes.MANUAL_OPEN_DOOR
                elif self.__act_op_mode == OperationModes.MANUAL_OPEN_DOOR:
                    self.__act_op_mode = OperationModes.MANUAL_CLOSE_DOOR
                elif self.__act_op_mode == OperationModes.MANUAL_CLOSE_DOOR:
                    self.__act_op_mode = OperationModes.MANUAL_ENDLESS
                elif self.__act_op_mode == OperationModes.MANUAL_ENDLESS:
                    self.__act_op_mode = OperationModes.MANUAL_OPEN_DOOR
      
        # Betriebsart Automatik
        elif (self.__act_op_mode == OperationModes.AUTOMATIC or
            self.__act_op_mode == OperationModes.AUTOMATIC_INFOS):
            if pinT1:
                self.__act_op_mode = OperationModes.NONE
            elif pinT2:
                if self.__act_op_mode == OperationModes.AUTOMATIC:
                    self.__act_op_mode = OperationModes.AUTOMATIC_INFOS
                elif self.__act_op_mode == OperationModes.AUTOMATIC_INFOS:
                    self.__act_op_mode = OperationModes.AUTOMATIC

        # Überprüfen ob die Betriebsart gewechselt hat
        if (old_op_mode == self.__act_op_mode):
            self.__op_mode_changed = False
        else:
            self.__op_mode_changed = True


    # METHODE
    # Um in den Fehlerzustand zu wechseln
    def change_to_error(self):
        self.__act_op_mode = OperationModes.ERROR


    # METHODE
    # Rückgabe aktuelle Betriebsart als String
    def getOpMode(self):
        mode_names = {
            OperationModes.NONE: "NONE",

            OperationModes.SETUP: "SETUP",
            OperationModes.SETUP_DATE_YEAR: "S: Change Year",
            OperationModes.SETUP_DATE_MONTH: "S: Change Month",
            OperationModes.SETUP_DATE_DAY: "S: Change Day",
            OperationModes.SETUP_TIME_HOUR: "S: Change Hour",
            OperationModes.SETUP_TIME_MINUTE: "S: Change Minute",
            OperationModes.SETUP_DELAY_SUNRISE: "S: Sunrise Delay",
            OperationModes.SETUP_DELAY_SUNSET: "S: Sunset Delay",

            OperationModes.MANUAL: "MANUAL",
            OperationModes.MANUAL_OPEN_DOOR: "M: Open door",
            OperationModes.MANUAL_CLOSE_DOOR: "M: Close door",
            OperationModes.MANUAL_ENDLESS: "M: Move Endless",

            OperationModes.AUTOMATIC: "AUTOMATIC",
            OperationModes.AUTOMATIC_INFOS: "AUTOMATIC INFO",

            OperationModes.ERROR: "Error"
            }
        if self.act_op_mode in mode_names:
            return mode_names[self.act_op_mode]
