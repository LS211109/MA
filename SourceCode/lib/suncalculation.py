import math
from lib.config import LOCATION_DEF

# KLASSE
# Berechnung Sonnenaufgang und Untergang für den Hühnertorstandort (Gerolfingen)
class Suncalculation:
    
    # KONSTRUKTOR: Suncalculation
    def __init__(self):
        # Konfiguration lesen und in lokale Variablen speichern
        self.__cfg_latitude = LOCATION_DEF["latitude"] # Breitengrad
        self.__cfg_longitude = LOCATION_DEF["longitude"] # Längengrad
        
        # Merker, wann die letzte Sonnenaufgang/Untergang- Berechnung durchgeführt wurde
        self.__calc_day = 0
        
        # Aktueller Sonnenaufgang/Untergang
        self.__sunrise_h = 0
        self.__sunrise_m = 0
        self.__sunset_h = 0
        self.__sunset_m = 0


    # PROPERTY
    # Sunrise, Rückgabe aktuelle Stunden
    @property
    def sunrise_h(self):
        return self.__sunrise_h


    # PROPERTY
    # Sunrise, Rückgabe aktuelle Minuten
    @property
    def sunrise_m(self):
        return self.__sunrise_m


    # PROPERTY
    # Sunset, Rückgabe aktuelle Stunden
    @property
    def sunset_h(self):
        return self.__sunset_h


    # PROPERTY
    # Sunset, Rückgabe aktuelle Stunden
    @property
    def sunset_m(self):
        return self.__sunset_m


    # METHODE
    # Objektreferenzen setzen, Zugriff auf andere Klassenobjekte
    def set_references(self, rtc):
        self.__rtc = rtc
        
        
   # METHODE
   # Zyklisches Update, welches den Sonnenaufgang und Untergang berechnet,
   # falls sich der TAG geändert hat
    def update(self):
        if (self.__calc_day != self.__rtc.day):
            # Berechnungstag merken
            self.__calc_day = self.__rtc.day

            #Aktuelles Datum 
            year = self.__rtc.year
            month = self.__rtc.month
            day = self.__rtc.day

            # Sonnenaufgang berechnen
            self.__sunrise_h, self.__sunrise_m = self.__calc_sunrise(year, month, day)
            
            # Sonnenuntergang berechnen
            self.__sunset_h, self.__sunset_m = self.__calc_sunset(year, month, day)


    # METHODE
    # Hilfsberechnung, Umrechnung Grad zu Rad
    def __deg_to_rad(self, deg):
        return deg * math.pi / 180


    # METHODE
    # Hilfsberechnung, Umrechnung Rad zu Grad
    def __rad_to_deg(self, rad):
        return rad * 180 / math.pi    
    

    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Fraktionales Jahr gamma
    def __fractional_year(self, year, month, day, hour):
        day_of_year = self.__rtc.day_of_year(year, month, day)
        days_per_year = self.__rtc.days_per_year(year)
        return 2 * math.pi / days_per_year * (day_of_year - 1 + (hour - 12) / 24) 


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Zeitgleichung (Minuten)
    def __equation_of_time(self, gamma):
        return 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Sonnen-Deklination (Winkel im Bogenmass)
    def __solar_declination_angle(self, gamma):
        return (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Zeitoffset (Minuten)
    def __time_offset(self, eqtime, utc_offset):
        return eqtime + 4 * self.__cfg_longitude - 60 * utc_offset


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Stundenwinkel (Grad)
    def __hour_angle(self, decl):
        lat_rad = self.__deg_to_rad(self.__cfg_latitude)
        zenith_rad = self.__deg_to_rad(90.833) # Atmosphärische Refraktion und Sonnenradius berücksichtigt
        cos_ha = math.cos(zenith_rad) / (math.cos(lat_rad) * math.cos(decl)) - math.tan(lat_rad) * math.tan(decl)
        ha = self.__rad_to_deg(math.acos(cos_ha))
        return ha


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Berechnung Sonnenaufgang in Minuten UTC, Rückgabe als Tupel Stunden:Minuten (angepasst an lokale Uhrzeit)
    def __calc_sunrise(self, year, month, day):
        # UTC Offset für Datum
        utc_offset = self.__rtc.utc_offset(year, month, day)
        
        # Berechnung Sonnenaufgang in Minuten, UTC Zeit
        gamma = self.__fractional_year(year, month, day, 6)  # Referenz 06:00 Uhr
        eqtime = self.__equation_of_time(gamma)
        decl = self.__solar_declination_angle(gamma)
        time_offset = self.__time_offset(eqtime, utc_offset)
        ha = self.__hour_angle(decl)
        sunrise = 720 - 4 * (self.__cfg_longitude + ha) - eqtime
        
        # Umwnadlung in Stunden, Minuten lokale Zeit
        return self.__min_to_hm(sunrise, utc_offset)


    # METHODE, nach NOAA (NOAA = National Oceanic and Atmospheric Administration)
    # Berechnung Sonnenuntergang in Minuten  UTC, Rückgabe als Tupel Stunden:Minuten (angepasst an lokale Uhrzeit)
    def __calc_sunset(self, year, month, day):
        # UTC Offset für Datum
        utc_offset = self.__rtc.utc_offset(year, month, day)

        # Berechnung Sonnenuntergang in Minuten, UTC Zeit
        gamma = self.__fractional_year(year, month, day, 18)  # Referenz 18:00 Uhr
        eqtime = self.__equation_of_time(gamma)
        decl = self.__solar_declination_angle(gamma)
        time_offset = self.__time_offset(eqtime, utc_offset)
        ha = self.__hour_angle(decl)
        sunset = 720 - 4 * (self.__cfg_longitude - ha) - eqtime
        
        # Umwnadlung in Stunden, Minuten lokale Zeit
        return self.__min_to_hm(sunset, utc_offset)


    # METHODE
    # Umrechnung in Stunden und Minuten
    def __min_to_hm(self, minutes, utc_offset):
        h = minutes // 60 # Ganzzahlige Division (abgerundet)
        m = minutes - h * 60
        h += utc_offset
        return int(h), int(m)


        


