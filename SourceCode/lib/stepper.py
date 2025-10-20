import utime 
from machine import Pin 
from lib.config import STEPPER_DEF


# KLASSE
# Ansteuern vom Schrittmotor
class Stepper:
    
    # KONSTRUKTOR
    def __init__ (self): 
        # Pins definieren
        self.__pin_out_direction = Pin(STEPPER_DEF["dir"], Pin.OUT)
        self.__pin_out_step = Pin(STEPPER_DEF["step"], Pin.OUT)
        self.__pin_out_enable = Pin(STEPPER_DEF["enable"], Pin.OUT)
        self.__pin_out_reset = Pin(STEPPER_DEF["reset"], Pin.OUT)
        self.__pin_out_sleep = Pin(STEPPER_DEF["sleep"], Pin.OUT)
        self.__pin_out_M1 = Pin(STEPPER_DEF["micro_m1"], Pin.OUT)
        self.__pin_out_M2 = Pin(STEPPER_DEF["micro_m2"], Pin.OUT)
        self.__pin_out_M3 = Pin(STEPPER_DEF["micro_m3"], Pin.OUT)
    
        # Variablen definieren
        self.__cfg_num_of_steps = STEPPER_DEF["num_of_steps"] # Schritte pro Umdrehung
        self.__cfg_pos_tolerance = STEPPER_DEF["pos_tolerance"] # Toleranz für Zielposition
        self.__act_pos = 0
        self.__next_time_for_step_us = 0 # Nächster Zeitpunkt bei dem der Ausgang STEP gesetzt wird

        #Reset auf False
        self.__pin_out_reset.value(True)
        
        
    # PROPERTY
    # Aktuelle Schrittmotorposition
    @property
    def act_pos(self):
        return self.__act_pos


    # METHODE
    # Motor stoppen, Ausgänge deaktivieren 
    def stop(self):
        self.__pin_out_step.value(False)
        self.__pin_out_enable.value(True)
        self.__pin_out_sleep.value(False)
    
    
    # METHODE
    # Motor endloss bewegen, mit einer definierten Geschwindigkeit
    def move(self, steps_per_seconds):
        self.__set_outputs(steps_per_seconds)
    
     
    # METHODE
    # Berechnen Pulslänge für den Ausgang STEP
    def __calc_speed_delta(self, steps_per_seconds):
        delta = abs(1/steps_per_seconds) * 0.5 * 1000000 / 8	# / 8 wegen 1/8 Schritten 
        return delta
            
    
    # METHODE
    # Motoransteuerung (MicroSteps, Dir, Step)
    def __set_outputs(self, steps_per_seconds):
        self.__pin_out_enable.value(False)
        self.__pin_out_sleep.value(True)
        if (steps_per_seconds > 0):
            self.__pin_out_direction.value(True)
        else:
            self.__pin_out_direction.value(False)
        
        #lauste: M1, M2, M3 anhand Geschwindigkeit setzen
        #aktuell: 1/8 Schritte
        self.__pin_out_M1.value(True)
        self.__pin_out_M2.value(True)
        self.__pin_out_M3.value(False)
        
        if (utime.ticks_us() >= self.__next_time_for_step_us):
            self.__next_time_for_step_us = utime.ticks_us() + self.__calc_speed_delta(steps_per_seconds)
            if (self.__pin_out_step.value() == 0):
              self.__pin_out_step.value(True)
              self.__count_steps(steps_per_seconds)
            else:
              self.__pin_out_step.value(False)


    # METHODE
    # Aktuelle Position zählen (Anzahl Schritte)
    def __count_steps(self, steps_per_seconds):
        # Position zählen
        if (steps_per_seconds > 0):
            self.__act_pos = self.__act_pos + 1
        else:
            self.__act_pos = self.__act_pos - 1
            
    


    
    
    
    
    
    
    
    
    

    
 
