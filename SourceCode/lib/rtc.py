from machine import RTC
from lib.config import LOCATION_DEF


# KLASSE
# Real Time Clock setzen, lesen, weitere Zeitfunktionen
class Rtc:
    
    # KONSTRUKTOR
    def __init__(self):
        # Konfiguration UTC Offset für Standort
        self.__cfg_utc_offset = LOCATION_DEF["utc_offset"] # UTC Offset 

        # Lokale Zeitvariable deklarieren
        self.date_time_array = [None, None, None, None, None, None]  # Arraygrösse 6  [0]=Jahr, [1]=Monat, [2]=Tag, [3]=Stunde, [4]=Minute, [5]=Sekunden

        # Real Time Clock Objekt
        self.__rtc = RTC()


   # METHODE
   # Zyklisches Update, welches die Uhrzeit aktualisiert
    def update(self):
        self.__read_time_date_from_rtc()


    # PROPERTY
    # DATE, Rückgabe aktuelles Jahr
    @property
    def year(self):
        if self.__rtc_is_ok():
            return self.date_time_array[0]
        else:
            return -1
    # PROPERTY
    # DATE, setzen Jahr
    @year.setter
    def year(self, value):
        #self.date_time_array[0] = value
        #self.__update_rtc()
        self.__change_RTC(year=value)


    # PROPERTY
    # DATE, Rückgabe aktueller Monat
    @property
    def month(self):
        if self.__rtc_is_ok():
            return self.date_time_array[1]
        else:
            return -1
    # PROPERTY
    # DATE, setzen Monat
    @month.setter
    def month(self, value):
        #self.date_time_array[1] = value
        #self.__update_rtc()
        self.__change_RTC(month=value)


    # PROPERTY
    # DATE, Rückgabe aktueller Tag
    @property
    def day(self):
        if self.__rtc_is_ok():
            return self.date_time_array[2]
        else:
            return -1
    # PROPERTY
    # DATE, setzen Tag
    @day.setter
    def day(self, value):
        #self.date_time_array[2] = value
        #self.__update_rtc()
        self.__change_RTC(day=value)


    # PROPERTY
    # DATE, Rückgabe Zeit als String, Stunden, Minuten und Sekunden
    @property
    def date(self):
        if self.__rtc_is_ok():
            return "{:02d}.{:02d}.{:04d}".format(self.date_time_array[2], self.date_time_array[1], self.date_time_array[0])


    # PROPERTY
    # TIME, Rückgabe aktuelle Stunden
    @property
    def hour(self):
        if self.__rtc_is_ok():
            return self.date_time_array[3]
        else:
            return -1
    # PROPERTY
    # TIME, setzen Stunden
    @hour.setter
    def hour(self, value):
        #self.date_time_array[3] = value
        #self.__update_rtc()
        self.__change_RTC(hour=value)
        

    # PROPERTY
    # TIME, Rückgabe aktuelle Minuten
    @property
    def minute(self):
        if self.__rtc_is_ok():
            return self.date_time_array[4]
        else:
            return -1
    # PROPERTY
    # TIME, setzen Minuten
    @minute.setter
    def minute(self, value):
        #self.date_time_array[4] = value
        #self.__update_rtc()
        self.__change_RTC(minute=value)


    # PROPERTY
    # TIME, Rückgabe aktuelle Sekunden
    @property
    def seconds(self):
        if self.__rtc_is_ok():
            return self.date_time_array[5]
        else:
            return -1
    # PROPTERY
    # TIME, setzen Sekunden
    @seconds.setter
    def seconds(self, value):
        self.date_time_array[5] = value
        self.__update_rtc()


    # PROPERTY
    # TIME, Rückgabe Zeit als String, Stunden, Minuten und Sekunden
    @property
    def time(self):
        if self.__rtc_is_ok():
            return "{:02d}:{:02d}:{:02d}".format(self.date_time_array[3], self.date_time_array[4], self.date_time_array[5])


    # PROPERTY
    # TIME, Rückgabe Zeit als String, Stunden und Minuten
    @property
    def time_short(self):
        if self.__rtc_is_ok():
            return "{:02d}:{:02d}".format(self.date_time_array[3], self.date_time_array[4])


    # METHODE
    # Berechnen wieviele Tage ein Jahr hat
    def days_per_year(self, year=None):
        calc_year = year
        if (
            calc_year is None and
            self.date_time_array[0] is not None
            ):
                calc_year = self.date_time_array[0] # Wenn das Jahr nicht als Parameter mitgegeben wird und die RTC definiert ist, dann Systemjahr übernehmen
        
        if self.__is_leap_year(calc_year):
            return 366.0
        else:
            return 365.0


    # METHODE
    # Berechnen Datum als fortlaufende Tagesanzahl zurückgibt
    def day_of_year(self, year=None, month=None, day=None):
        # Falls Datum als Parameter mitgegeben wird
        if (
            year is not None and
            month is not None and
            day is not None
            ):        
                calc_year = year
                calc_month = month
                calc_day = day
                return self.__day_of_year(calc_year, calc_month, calc_day)

        # Systemzeit
        elif self.__rtc_is_ok():
            calc_year = self.date_time_array[0]
            calc_month = self.date_time_array[1]
            calc_day = self.date_time_array[2]
            return self.__day_of_year(calc_year, calc_month, calc_day)

        else:
            return 0


    # METHODE
    # Berechnen UTC-Offset anhand vom Datum
    def utc_offset(self, year, month, day):
        if self.__is_summer_time(year, month, day):
            return self.__cfg_utc_offset + 1
        else:
            return self.__cfg_utc_offset


    # METHODE
    # Aktuelles Datum und Uhrzeit von RTC lesen (Rückgabe als Liste) und in lokales Array speichern
    def __read_time_date_from_rtc(self):
        dt = self.__rtc.datetime()
        self.date_time_array = [dt[0], dt[1], dt[2], dt[4], dt[5], dt[6]]


    # METHODE
    # Überprüft, ob Datum und Uhrzeit definiert sind
    def __rtc_is_ok(self):
        if (
            self.date_time_array[0] is not None and
            self.date_time_array[1] is not None and
            self.date_time_array[2] is not None and
            self.date_time_array[3] is not None and
            self.date_time_array[4] is not None and
            self.date_time_array[5] is not None
            ):        
                return True
        else:
            return False

    # METHODE
    # Überprufen ob es sich um ein Schaltjahr handelt
    # Schaltjahr, wenn :4 teilbar
    # Kein Schaltjahr, wenn :100 teilbar
    # Schaltjahr, wenn :400 teilbar
    def __is_leap_year(self, year=None):
        if year is None:
            return False
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

      
    # METHODE
    # Berechnen Datum als fortlaufende Tagesanzahl berechnet
    def __day_of_year(self, year, month, day):
        days_per_month = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        
        if self.__is_leap_year(year) and month > 2:
            return days_per_month[month-1] + day + 1
        else:
            return days_per_month[month-1] + day

    
    # METHODE
    # Berechnen Wochentag zu einem belibigen Datum ab 1583 berechnet (nach Zellers Kongruenz)
    # 0=Sa, 1=So, 2=Mo, 3=Di, 4=Mi, 5=Do, 6=Fr
    def __weekday(self, year, month, day):
        calc_month = month
        calc_year = year
        if month < 3:
            calc_month += 12
            calc_year -= 1
        k = calc_year % 100
        j = calc_year // 100
        return (day + (13 * (calc_month + 1)) // 5 + k + k // 4 + j // 4 + 5 * j) % 7


    # METHODE
    # Berechnet zu einem Datum, ob Sommer oder Winterzeit ist
    # Sommerzeit beginnt am letzten Sonntag im März und endet am letzten Sonntag im Oktober
    def __is_summer_time(self, year, month, day):
        if month < 3 or month > 10:
            return False
        elif month > 3 and month < 10:
            return True
        elif month == 3:
            for last_sunday in range(31, 24, -1):  # von 31 bis 25 (einschließlich)
                if self.__weekday(year, month, last_sunday) == 1:
                    break  # Schleife verlassen            
            return (day >= last_sunday)
        elif month == 10:
            for last_sunday in range(31, 24, -1):  # von 31 bis 25 (einschließlich)
                if self.__weekday(year, month, last_sunday) == 1:
                    break  # Schleife verlassen            
            return (day < last_sunday)


    # METHODE
    # Aktuelles Datum und Uhrzeit setzen
    def __change_RTC(self, year = None, month = None, day = None, hour = None, minute = None):
        yr, mo, dy, wd, hr, mi, se, us = self.__rtc.datetime()
        
        if year is not None:
            yr = year
        if month is not None:
            mo = month
        if day is not None:
            dy = day
        if hour is not None:
            hr = hour
        if minute is not None:
            mi = minute

        # Standard für weekday (wird durch rtc berechnet, falls 0), sekunden und mikrosekunden
        wd = 0
        se = 0
        us = 0

        # Neue Uhrzeit setzen
        self.__rtc.datetime((yr, mo, dy, wd, hr, mi, se, us))



