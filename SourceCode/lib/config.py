# Motordefinition
STEPPER_DEF = {
    "dir": "D7",
    "step": "D6",
    "enable": "D0", #LOW=Enable, HIGH=Disable
    "reset": "D4",
    "sleep": "D5",
    "micro_m1": "D1",
    "micro_m2": "D2",
    "micro_m3": "D3",
    "num_of_steps": 200,
    "pos_tolerance": 5
}

# Displaydefinition
DISPLAY_DEF = {
    "i2c": 2,
    "address": 0x27,
    "num_lines": 2,
    "num_columns": 16
}

# Betriebsartdefinition
OPERATION_DEF = {
    "pin_s1": "D16",
    "pin_s2": "D17",
    "pin_s3": "D18",
    "pin_s4": "D19",
    "debounce_time_ms": 100
}

# Ueberwachung
PROTECTION_DEF = {
    "pin_sensor_top": "D14",
    "pin_sensor_bot": "D15",
    "debounce_time_ms": 100,
    "error_timeout": 30
}

# Huehnertordefinition
HTOR_DEF = {
    "speed": 200,
    "speed_slow": 100
}

# Localtion (xxx)
LOCATION_DEF = {
    "latitude": 48.01, # vor Upload auf Github verändert
    "longitude": 8.12, # vor Upload auf Github verändert
    "utc_offset": 1
}


# Startmodus: Automatic
START_OPMODE_AUTOMATIC = True

# Projektinformationen
PROJECT_NAME = "Huehner-Tor"
PROJECT_AUTHOR  = "LS"
