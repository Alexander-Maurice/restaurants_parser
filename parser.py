
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

with webdriver.Chrome() as browser:
    browser.get('https://www.restoclub.ru/msk/search/restorany-moskvy-s-zhivoj-muzykoj/18')

    # Собираем массив страниц, которые нужно открыть
    elements = browser.find_elements(By.CLASS_NAME, 'search-place-title__name')

    # Открываем страницы
    for elem in elements:
        elem.click()
        time.sleep(2)

    # Собираем дескрипторы вкладок в переменную
    handles = browser.window_handles

    # Открываем кажду вкладку, кроме стартовой
    for i in range(1, len(handles)):
        browser.switch_to.window(handles[i])
        time.sleep(5)
        try:
            # Находим название организации, телефон и адресс
            name = browser.find_element(By.CLASS_NAME, 'place-title__header').text
            browser.find_element(By.CLASS_NAME, 'place__phone').click()
            phone = browser.find_element(By.CLASS_NAME, 'place-phone__number')
            calling_phone = phone.get_attribute('content')
            adress = browser.find_element(By.CLASS_NAME, 't-dotted').text
        except NoSuchElementException: 
            pass

        # Записываем собранные данные в файл
        file = open('restaurants.txt', 'a')
        file.write('\n')
        file.write(name)
        file.write('\n')

        # Обрабатываем исключение, когда телефон не вписан напрямую, а указан в модальном окне
        try:
            # Cначала пробуем просто записать номер
            file.write(calling_phone)
        except NameError:
            # Определяем блок на сайте, которое должно быть видно в браузере для взаимодействия с ним
            target = browser.find_element(By.CLASS_NAME, 'place__aside')
            ActionChains(browser).move_to_element(target).perform() # Прокручиваем до блока
            time.sleep(3)
            browser.find_element(By.CLASS_NAME, 'place-phone__number').click() #Кликаем на элемент, чтоб было видно телефон полностью
            time.sleep(3)
            try:
                phone = browser.find_element(By.XPATH, '//div[@class="place-phone__popup"]/div/div/ul/li[1]/a') # находим телефон в модальном окне
                calling_phone = phone.get_attribute('href') # по атрибуту получаем телефон
            except NoSuchElementException:
                phone = browser.find_element(By.XPATH, '//div[@class="place-phone"]/a')
                calling_phone = phone.get_attribute('href')
                file.write(calling_phone)
        else:
            pass   
        file.write('\n')
        try:
            file.write(adress)
        except:
            pass
        file.write('\n')
        file.write('____________________\n')
        file.write('____________________\n')
        file.close()
        time.sleep(5)

# На сайте сложная система с номерами телефонов, поэтому пришлось работать с вложенными блоками
# try except
