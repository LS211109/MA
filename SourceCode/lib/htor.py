from time import sleep_ms

from lib.system import System
from lib.operation import Operation
from lib.operation import OperationModes
from lib.stepper import Stepper
from lib.protection import Protection
from lib.display import Display
from lib.rtc import Rtc
from lib.timer import Timer
from lib.suncalculation import Suncalculation
from lib.config import HTOR_DEF
    

# KLASSE
# Definition der verschiedenen States
# Micropython unterstützt Enum nicht
class States:
    step_init = 0
    step_show_info = 1
    step_show_info_delay = 2
    step_check_op_mode = 3

    step_setup_year = 100
    step_setup_month = 101
    step_setup_day = 102
    step_setup_hour = 103
    step_setup_minute = 104
    step_setup_sunrise = 105
    step_setup_sunset = 106

    step_manual_open_door = 200
    step_manual_close_door = 201
    step_manual_endless = 202

    step_automatic = 300

    step_exit = 900
    
    
# KLASSE
# Torsteuerung. Alle Objekte werden hier erzeugt und das Tor anhand einer Schrittkette gesteuert
class Htor:

    # KONSTRUKTOR für Hühnertor
    def __init__(self):
        # Objekte erstellen
        self.__init_objects()
        
        # Variablen initialisieren
        self.__act_step = States.step_init
        
        # Marker error
        self.__error_time = 0
        

    # METHODE
    # Objekte erstellen und Objektreferenzen an andere Objekte übergeben
    def __init_objects(self):
        self.__syst = System()
        self.__op = Operation()
        self.__step = Stepper()
        self.__prot = Protection()
        self.__disp = Display()
        self.__rtc = Rtc()
        self.__sun = Suncalculation()
        self.__timer = Timer()
        
        # Referenzen zuweisen
        self.__syst.set_references(self.__step, self.__rtc)
        self.__sun.set_references(self.__rtc)
        self.__timer.set_references(self.__syst, self.__rtc, self.__sun)
        self.__disp.set_references(self.__syst, self.__rtc, self.__timer, self.__op)
  
  
    # METHODE
    # Wird zyklisch aufgerufen (Updates durchführen, Steuern des Tor's (Betriebsart)
    # Micropython unterstützt leider MATCH CASE nicht. Alles muss mit if, elif, else gemacht werden 
    def run(self):
        while True:
            # Update objects
            self.__op.update()
            self.__syst.update()
            self.__prot.update()
            self.__rtc.update()
            self.__rtc.update()
            self.__sun.update()
            self.__timer.update()

            # Schrittkette
            if self.__act_step == States.step_init:
                self.__act_step = States.step_show_info
                print("programm started")
              
            # Projektinfo auf Display ausgeben
            elif self.__act_step == States.step_show_info:
                self.__disp.writeDisplay(1,self.__syst.project_name,True)
                self.__disp.writeDisplay(2,self.__syst.project_author,False)
                self.__act_step = States.step_show_info_delay

            # 2s Verzögerung, dann aktuelle Betriebart darstellen
            elif self.__act_step == States.step_show_info_delay:
                sleep_ms(2000)
              
                # Display anzeigen
                self.__disp.show_display(self.__op.act_op_mode, True)               
                self.__act_step = States.step_check_op_mode

            # Überprüfen Betriebsart
            elif self.__act_step == States.step_check_op_mode:
                #SETUP
                if self.__op.act_op_mode == OperationModes.SETUP_DATE_YEAR:
                    self.__act_step = States.step_setup_year
                elif self.__op.act_op_mode == OperationModes.SETUP_DATE_MONTH:
                    self.__act_step = States.step_setup_month
                elif self.__op.act_op_mode == OperationModes.SETUP_DATE_DAY:
                    self.__act_step = States.step_setup_day
                elif self.__op.act_op_mode == OperationModes.SETUP_TIME_HOUR:
                    self.__act_step = States.step_setup_hour
                elif self.__op.act_op_mode == OperationModes.SETUP_TIME_MINUTE:
                    self.__act_step = States.step_setup_minute
                elif self.__op.act_op_mode == OperationModes.SETUP_DELAY_SUNRISE:
                    self.__act_step = States.step_setup_sunrise
                elif self.__op.act_op_mode == OperationModes.SETUP_DELAY_SUNSET:
                    self.__act_step = States.step_setup_sunset

                #MANUAL
                elif self.__op.act_op_mode == OperationModes.MANUAL_ENDLESS:
                    self.__act_step = States.step_manual_endless
                elif self.__op.act_op_mode == OperationModes.MANUAL_OPEN_DOOR:
                    self.__act_step = States.step_manual_open_door
                elif self.__op.act_op_mode == OperationModes.MANUAL_CLOSE_DOOR:
                    self.__act_step = States.step_manual_close_door
                    
                # AUTOMATIK
                elif (self.__op.act_op_mode == OperationModes.AUTOMATIC or
                    self.__op.act_op_mode == OperationModes.AUTOMATIC_INFOS):
                    self.__act_step = States.step_automatic
                    self.__error_time = self.__rtc.hour * 3600 + self.__rtc.minute * 60 + self.__rtc.seconds



            # SETUP_YEAR, anpassen RTC Jahr
            elif self.__act_step == States.step_setup_year:
                self.__syst.change_rtc_year()

                # SETUP_YEAR verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_DATE_YEAR:
                    self.__act_step = States.step_exit

            # SETUP_MONTH, anpassen RTC Monat
            elif self.__act_step == States.step_setup_month:
                self.__syst.change_rtc_month()

                # SETUP_MONTH verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_DATE_MONTH:
                    self.__act_step = States.step_exit

            # SETUP_DAY, anpassen RTC Tag
            elif self.__act_step == States.step_setup_day:
                self.__syst.change_rtc_day()

                # SETUP_DAY verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_DATE_DAY:
                    self.__act_step = States.step_exit

            # SETUP_HOUR, anpassen RTC Stunden
            elif self.__act_step == States.step_setup_hour:
                self.__syst.change_rtc_hour()

                # SETUP_HOUR verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_TIME_HOUR:
                    self.__act_step = States.step_exit

            # SETUP_MINUTE, anpassen RTC Minuten
            elif self.__act_step == States.step_setup_minute:
                self.__syst.change_rtc_minute()

                # SETUP_MINUTE verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_TIME_MINUTE:
                    self.__act_step = States.step_exit

            # SETUP_SUNRISE, anpassen Sonnenaufgangverzögerung
            elif self.__act_step == States.step_setup_sunrise:
                self.__syst.change_sunrise_delay()

                # SETUP_SUNRISE verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_DELAY_SUNRISE:
                    self.__act_step = States.step_exit

            # SETUP_SUNSET, anpassen Sonnenuntergangverzögerung
            elif self.__act_step == States.step_setup_sunset:
                self.__syst.change_sunset_delay()

                # SETUP_SUNSET verlassen
                if self.__op.act_op_mode != OperationModes.SETUP_DELAY_SUNSET:
                    self.__act_step = States.step_exit


            # MANUAL_DOOR_OPEN
            elif self.__act_step == States.step_manual_open_door:
                # Schrittmotor ansteuern
                if self.__syst.pin_in_T3.state_on and not self.__prot.door_in_open_pos: 
                    self.__step.move(HTOR_DEF["speed"] * -1)
                else:
                    self.__step.stop()

                if (self.__op.act_op_mode != OperationModes.MANUAL_OPEN_DOOR):
                    self.__act_step = States.step_exit

            # MANUAL_DOOR_CLOSE
            elif self.__act_step == States.step_manual_close_door:
                # Schrittmotor ansteuern
                if self.__syst.pin_in_T3.state_on and not self.__prot.door_in_close_pos: 
                    self.__step.move(HTOR_DEF["speed"] * 1)
                else:
                    self.__step.stop()

                if self.__op.act_op_mode != OperationModes.MANUAL_CLOSE_DOOR:
                    self.__act_step = States.step_exit

            # MANUAL endlos nach oben / unten bewegen
            elif self.__act_step == States.step_manual_endless:
                # Schrittmotor ansteuern
                if self.__syst.pin_in_T3.state_on: # UP
                    self.__step.move(HTOR_DEF["speed_slow"] * -1)
                elif self.__syst.pin_in_T4.state_on: # DOWN
                    self.__step.move(HTOR_DEF["speed_slow"])
                else:
                    self.__step.stop()

                if self.__op.act_op_mode != OperationModes.MANUAL_ENDLESS:
                    self.__act_step = States.step_exit


            # AUTOMATIK
            elif self.__act_step == States.step_automatic:
                if self.__timer.open_door: # Tor muss öffnen
                    if not self.__prot.door_in_open_pos: # Tor noch nicht auf Endschalter, fahren nach oben
                        self.__step.move(HTOR_DEF["speed"] * -1)
                        act_time_in_s = self.__rtc.hour * 3600 + self.__rtc.minute * 60 + self.__rtc.seconds
                        if (act_time_in_s > self.__error_time +self.__prot.error_timeout):
                            self.__op.change_to_error()
                    else:
                        self.__step.stop()
                        self.__error_time = self.__rtc.hour * 3600 + self.__rtc.minute * 60 + self.__rtc.seconds
                    
                elif self.__timer.close_door: # Tor muss schliessen
                    if not self.__prot.door_in_close_pos: # Tor noch nicht auf Endschalter, fahren nach unten
                        self.__step.move(HTOR_DEF["speed"])
                        act_time_in_s = self.__rtc.hour * 3600 + self.__rtc.minute * 60 + self.__rtc.seconds
                        if (act_time_in_s > self.__error_time +self.__prot.error_timeout):
                            self.__op.change_to_error()
                    else:
                        self.__step.stop()
                        self.__error_time = self.__rtc.hour * 3600 + self.__rtc.minute * 60 + self.__rtc.seconds


                # AUTOMATIK verlassen
                if (self.__op.act_op_mode != OperationModes.AUTOMATIC and
                    self.__op.act_op_mode != OperationModes.AUTOMATIC_INFOS):
                    self.__act_step = States.step_exit


            # VERLASSEN SCHRITTKETTE, MOTOR STOPPEN
            elif self.__act_step == States.step_exit:
                # Schrittmotor stoppen
                self.__step.stop()
                self.__act_step = States.step_check_op_mode


            else:
                print("Step not defined")

            # Display anzeigen
            self.__disp.show_display(self.__op.act_op_mode)               

            # self.__disp.test_display()

            
      
