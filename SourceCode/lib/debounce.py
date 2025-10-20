import utime
from machine import Pin

# KLASSE
# Wird verwendet, um Signale zu entprellen
class Debounce:
    
    # KONSTRUKTOR, Übergabe Pin-Nummer + Entprellzeit
    def __init__(self, hw_pin, debounce_time_ms):
        # Pin definieren + Entprellzeit definieren
        self.__hw_pin = Pin(hw_pin, Pin.IN, Pin.PULL_DOWN)
        self.__debounce_time_ms = debounce_time_ms
        
        # Status alle zurücksetzen
        self.__state_on = False
        self.__state_off = False
        self.__state_down = False
        self.__state_up = False
        
        # Privater Zeitmerker definieren
        self.__hw_pin_time_pressed = 0


    # PROPERTY
    # Permanentes Signal, falls Knopf gedrückt: Wird true sobald Entprellzeit abgelaufen  
    @property
    def state_on(self):
        return self.__state_on
    

    # PROPERTY
    # Permanentes Signal, falls Konopf losgelassen: Wird ohne Verzögerung gesetzt 
    @property
    def state_off(self):
        return self.__state_off


    # PROPERTY
    # Trigger, falls Taster gedrückt wird
    @property
    def state_down(self):
        return self.__state_down
    
    
    # PROPERTY
    # Trigger, falls Taster losgelassen wird
    @property
    def state_up(self):
        return self.__state_up

    
    # METHODE
    # Zyklisches Update, welches die Statusvariablen setzt
    def update(self):
        # Aktuelle Prozessorzeit in ms lesen 
        self.time_actual_ms = utime.ticks_ms()
        
        # Interner Zeitmarker setzen, reseten
        if (self.__hw_pin.value() == 1): # Eingang gedrückt
            if self.__hw_pin_time_pressed == 0: # Wenn interner Marker noch 0, dann Entprellzeitpunkt berechnen
                self.__hw_pin_time_pressed = self.time_actual_ms + self.__debounce_time_ms
        else: # Eingang ungedrückt
              self.__hw_pin_time_pressed = 0 # Interner Marker zurücksetzen

        # Status UP setzen
        if (self.__hw_pin_time_pressed == 0) and self.__state_on:
            self.__state_up = True 
        else:
            self.__state_up = False

        # Status DOWN setzen    
        if (self.__hw_pin_time_pressed > 0) and (self.time_actual_ms >= self.__hw_pin_time_pressed) and not self.__state_on:
            self.__state_down = True
        else:
            self.__state_down = False 

        # Status ON setzen
        if (self.__hw_pin_time_pressed > 0) and (self.time_actual_ms >= self.__hw_pin_time_pressed): 
            self.__state_on = True
        else:
            self.__state_on = False
          
        # Status OFF setzen
        self.__state_off = not self.__state_on
          

