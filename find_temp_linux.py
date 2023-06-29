from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''Wszystkie operacje są wykonywane na prognozie pogody w google z hasłem wyszukiwania: "pogoda zabrze"'''

def accept_cookie(driver):
    '''Zgodzenie się na cookie'''

    try:
        driver.find_element_by_id('L2AGLb').click()
    except:
        pass

def day_to_txt(n, driver):
    """Zapisuje w pliku dayN.txt dane o pogodzie z prognozy google.

    Args:
        n (int): od 0 do 7 numer pliku txt
        driver (webdriver): na nim wykonywane sa wszystkie operacje w przegladarce
    """

    temp = driver.find_element_by_id('wob_tm').text + '\n'
    wind = driver.find_element_by_id('wob_ws').text + '\n'
    humidity = driver.find_element_by_id('wob_hm').text + '\n'
    day = driver.find_element_by_id('wob_dts').text + '\n'
    precipitation = driver.find_element_by_id('wob_pp').text

    txt = open('./days_data/day' + str(n) + '.txt', 'w')
    data = [temp, wind, humidity, day, precipitation]
    txt.writelines(data)
    txt.close()

def choose_day(n, driver):
    '''
    Zmiana dnia na który wyświetla się prognoza pogody

    Args:
        n (int): numer dnia z zakresu [1, 8]
    '''
    day_cell = driver.find_element_by_xpath('//*[@id="wob_dp"]/div[' + str(n) + ']').click()

def main():
    """
    Funkcja odpala przeglądarke i zczytuje wszystkie potrzebne dane.
    """

    driver = webdriver.Chrome()
    driver.get('https://www.google.com/search?client=opera-gx&q=pogoda+zabrze&sourceid=opera&ie=UTF-8&oe=UTF-8%27')
    driver.refresh()
    accept_cookie(driver)
    sleep(0.3)

    for i in range(8):
        day_to_txt(i, driver)
        if i < 7:
            choose_day(i + 2, driver)
    driver.quit()
