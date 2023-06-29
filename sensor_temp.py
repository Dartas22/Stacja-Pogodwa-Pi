import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_id = '28-3c01a8166556'
device_file = base_dir + device_id + '/w1_slave'

def read_temp_raw():
    """
    pobiera dane z pliku, w ktorym jest temperatura

    Returns:
        list(str): lista, w ktorej drugi argument zawiera informacje o tempereturze
    """

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    return lines

def read_temp():
    """
    zwraca wartosc temperatury odczytana z termometru

    Returns:
        float: temperatura w stopniach celciusza z dokladnoscia do trzech miejsc po przecinku
    """

    lines = read_temp_raw()
    temp_str = lines[1][-6:-1]
    temp_c = float(temp_str) / 1000

    return temp_c
