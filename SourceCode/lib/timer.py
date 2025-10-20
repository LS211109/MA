# KLASSE
# Wird verwendet, um den Sollzustand des Tors zu definieren
# Tor muss öffnen, wenn aktualle Zeit >= Sonnenaufgang + Konfigurationsoffet
# Tor muss schliessen, wenn aktualle Zeit >= Sonnenuntergang + Konfigurationsoffet
class Timer:

    # KONSTRUKTOR: Timer
    def __init__(self):
        # Variable Tor öffnen
        self.__calc_sunrise_m = 0
        self.__calc_sunrise_delay = 0
        self.__sunrise_h = 0
        self.__sunrise_m = 0
        self.__open_door = False	# Befehl öffnen, falls True
        
        # Variable Tor schliessen
        self.__calc_sunset_m = 0
        self.__calc_sunset_delay = 0
        self.__sunset_h = 0
        self.__sunset_m = 0
        self.__close_door = False	# Befehl schliessen, falls True
        
        # Merker
        self.__calc_update_m = -1


    # PROPERTY
    # Torzeit öffnen als String hh:mm
    @property
    def open_door_time(self):
        return f"{self.__sunrise_h:02d}:{self.__sunrise_m:02d}" 


    # PROPERTY
    # TOR-Befehl öffnen
    @property
    def open_door(self):
        return self.__open_door


    # PROPERTY
    # Torzeit schliessen alse String hh:mm
    @property
    def close_door_time(self):
        return f"{self.__sunset_h:02d}:{self.__sunset_m:02d}" 


    # PROPERTY
    # TOR-Befehl schliessen
    @property
    def close_door(self):
        return self.__close_door


    # METHODE
    # Objektreferenzen setzen, Zugriff auf andere Klassenobjekte
    def set_references(self, syst, rtc, sun):
        self.__syst = syst
        self.__rtc = rtc
        self.__sun = sun


   # METHODE
   # Zyklisches Update, welches den Sollzustand vom Tor berechnet, nur wenn Sonnenaufgang oder Untergang gewechselt hat
    def update(self):
        if (self.__calc_update_m != self.__rtc.minute or
            self.__calc_sunrise_m != self.__sun.sunrise_m or
            self.__calc_sunset_m != self.__sun.sunset_m or
            self.__calc_sunrise_delay != self.__syst.sunrise_delay or
            self.__calc_sunset_delay != self.__syst.sunset_delay):
            
            # Speichern, wann die Berechnung durchgeführt wurde
            self.__calc_update_m = self.__rtc.minute
            self.__calc_sunrise_m = self.__sun.sunrise_m
            self.__calc_sunset_m = self.__sun.sunset_m
            self.__calc_sunrise_delay = self.__syst.sunrise_delay
            self.__calc_sunset_delay = self.__syst.sunset_delay
            
            # Sonnenaufgang mit Berücksichtigung Benutzerverzögerung
            self.__sunrise_h, self.__sunrise_m = self.__add_timeoffset(self.__sun.sunrise_h, self.__sun.sunrise_m, self.__syst.sunrise_delay) 

            # Sonnenuntergang mit Berücksichtigung Benutzerverzögerung
            self.__sunset_h, self.__sunset_m = self.__add_timeoffset(self.__sun.sunset_h, self.__sun.sunset_m, self.__syst.sunset_delay) 

            # Überprufen ob Tor geöffnet oder geschlossen werden muss (alles in Minuten umgewandelt)
            open_time = self.__sunrise_h * 60 + self.__sunrise_m # Minuten ab Mitternacht
            close_time = self.__sunset_h * 60 + self.__sunset_m # Minuten ab Mitternacht
            act_time = self.__rtc.hour * 60 + self.__rtc.minute
            self.__open_door = (act_time >= open_time) and (act_time < close_time)
            self.__close_door = not self.__open_door


    # METHODE
    # Zu einer Zeit Minuten addieren und überprüfen, dass die Zeit korrekt ist
    def __add_timeoffset(self, hour, minute, minute_offset):
        h = hour
        m = minute + minute_offset
        # Überprüfen, dass Minuten nicht kleiner 0 oder grösser als 59 sind
        while m < 0 or m >= 60:
            if m < 0:
                m += 60
                h -= 1
            elif m >= 60:
                m -= 60
                h += 1
        return h, m
        
        
        
        
        

