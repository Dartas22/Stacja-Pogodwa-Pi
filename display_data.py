import sensor_temp
import find_temp_linux

from cProfile import run
import threading

import time
import board
import digitalio
import RPi.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

#Konfiguracja wyswietlacza
#Definiowaie reset pinu
oled_reset = digitalio.DigitalInOut(board.D4)

#Paramatry wyświetlacza
WIDTH = 128
HEIGHT = 64
BORDER = 5

#Wykorzystywane do I2C
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

#Wyczyść wyswietlacz
oled.fill(0)
oled.show()

#Stworz pusty obraz
image = Image.new("1", (oled.width, oled.height))

#Obiekt na ktorym mozna rysowac
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

#Do wyswietlania samej temperetury
font1 = ImageFont.truetype(font='./PixelOperator.ttf', size=50)
#Do wyswietladnia loadingu
font2 = ImageFont.truetype(font='./PixelOperator.ttf', size=20)

#Ustawianie pinow na przyciski
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Zmienna wykorzystywana do sprawdzenia czy funkcja ftl_main() dalej dziala
running = False

def txt_to_L(day=0):
    """
    Funkcja zwraca liste z parametrami [temperatura, wiatr, wilgotnosc, dzien, opady]

    Args:
        day (int, optional): Numer pliku txt z danymi, od 0 do 7 (dayX.txt). Domyślnie 0.

    Returns:
        list(str): piecio-elementowa lista z danymi pogody
    """

    with open('./days_data/day' + str(day) + '.txt') as f:
        lines = f.readlines()

    for i in range(len(lines)-1):
        lines[i] = lines[i][:-1]

    return lines


def ret_day(day):
    """
    Funkcja podmienia polskie znaki oraz usuwa przecinek i godzine jeśli akurat występuja

    Args:
        day (str): numer pliku txt (4 linijka)

    Returns:
        str: sama nazwa dnia be zposlkich znakow
    """
    if day[:2] == 'po':
        return 'poniedzialek'
    elif day[:2] == 'pi':
        return 'piatek'
    elif day[0] == 'ś':
        return 'sroda'

    for i in range(len(day)):
        if day[i] == ',':
            return day[:i]

    return day

def print_data(dayn=0):
    """
    Funkcja wyswietla pierwszy ekran na ktorym znajduja sie dane o pogodzie z pliku txt.

    Args:
        dayn (int, optional): Numer pliku txt, z ktorego program ma wyswietlac dane. Domyslnie 0.
    """

    txt_data = txt_to_L(dayn)
    #Zamalowuje ekran na czarno, zeby go wyczyscic
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    day = ret_day(txt_data[3])
    temp_out = txt_data[0]
    wind = txt_data[1]
    humidity = txt_data[2]
    temp_in = round(sensor_temp.read_temp(), 1)
    precipitation = txt_data[4]

    draw.text((0, 0), 'Dzien: ' + day, font=font, fill=255)
    draw.text((0, 12), 'Temp out/in: ' + temp_out  + "/" + str(int(temp_in)) + "'C", font=font, fill=255)
    draw.text((0, 24), 'Wiatr: ' + wind, font=font, fill=255)
    draw.text((0, 36), 'Wilgotnosc: ' + humidity, font=font, fill=255)
    draw.text((0, 48), 'Opady: ' + precipitation, font=font, fill=255)

    oled.image(image)
    oled.show()

def print_temp():
    """
    Funkcja wyswietla drugi ekran, na ktorym znajduje sie sama temperatura odczytywana z termometru.
    Funkcja korzysta z pliku snesor_temp.py.
    """

    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    temp_in = round(sensor_temp.read_temp(), 1)
    draw.text((5, 5), str(temp_in) + "'C", font=font1, fill=255)

    oled.image(image)
    oled.show()

def loading_screen(i=0):
    """Funkcja dziala podczas aktualizowania danych w plikach txt i wyswietla ekran ladowania.

    Args:
        i (int, optional): Iterator po liscie loading. Domyslnie 0.
    """

    loading = ['/', '|', '\\', '-']
    global running

    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    draw.text((15, 0), 'Aktualizowanie', font=font2, fill=255)
    draw.text((40, 18), 'danych', font=font2, fill=255)
    draw.text((65, 36), loading[i], font=font2, fill=255)

    oled.image(image)
    oled.show()

    if not running:
        i += 1
        if i > 3:
            i = 0
        loading_screen(i)

    else:
        #zmiana running z powrotem na False, zeby funkcja mogla zadzialac przy nastepnej aktualizacji
        running = False


def display_out(screen, dayn):
    """
    Funkcja decyduje jaki ekran wyswietlac

    Args:
        screen (int): informacja o ekranie, ktory ma wyswietlac
        dayn (int): numer pliku txt, z ktorego ma ewentualnie wyswietlac dane
    """

    if screen == 1:
        print_data(dayn)

    elif screen == -1:
        print_temp()


def ftl_main():
    """
    Funkcja uruchamia aktualizacje danych w plikach txt (funkcja main() w find_temp_linux.py). Na koniec ustawia running na True, zeby zatrzymac funkcje loading_screen().
    """

    find_temp_linux.main()

    global running
    running = True


if __name__ == '__main__':

    day_num = 0 #numer pliku txt, z ktorego zczytywane sa dane
    screen = 1 #numer ekranu, ktory ma byc wyswietlany

    while True:
        button = GPIO.input(26) #lewy przycisk
        button1 = GPIO.input(20) #prawy przycisk

        if button == 1 and button1 == 1:
            time.sleep(1)

            threading.Thread(target = loading_screen).start()
            ftl_main()

            day_num = 0
            screen = 1

        elif button == 1:
            time.sleep(1)

            day_num += 1
            if day_num >= 8:
                day_num = 0

        elif button1 == 1:
            time.sleep(1)
            screen *= -1


        display_out(screen, day_num)
