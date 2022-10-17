
from telnetlib import EC
import time

import jse as jse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import js2py

def driver_chrome():
    CHROMEDRIVER_PATH = 'C:/Users/Deadvin/Downloads/chromedriver'
    CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CHROME_PATH

    # chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    # chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
    # chrome_prefs = {}
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    return driver

def wait_page_load(driver):
    trying = 0
    loading_block = driver.find_element_by_xpath('/html/body').get_attribute('outerHTML')
    while not '<div id="loadingBg" style="display: none;">' in loading_block:
        try:
            loading_block = driver.find_element_by_xpath('/html/body').get_attribute('outerHTML')
            break
        except:
            time.sleep(1)
            print('Loading!!!!')
        trying = trying + 1
        if trying == 10:
            break

def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

links = []
list = []
driver = driver_chrome()
driver.get("https://www.oponeo.pl/wybierz-opony/")


excel_row = [
    ['samochody osobowe', 'summer', 'CONTINENTAL', '265', '30', '21', '96', 'Y', '', 'XL'],
    ['samochody osobowe', 'summer', 'PIRELLI', '265', '35', '18', '93', 'Y', '', ''],
    ['samochody osobowe', 'winter', 'HANKOOK', '215', '50', '17', '95', 'V', '', 'XL'],
    ['samochody osobowe', 'all-season', 'KLEBER', '185', '65', '14', '86', 'T', '', ''],
    ['', 'winter', 'DUNLOP', '225', '50', '17', '94', 'H', '', ''],
    ['samochody osobowe', 'all-season', 'KLEBER', '185', '65', '14', '86', 'T', '', ''],
    ['samochody osobowe', 'all-season', '', '185', '65', '14', '', '', '', ''],
    ['samochody osobowe', 'winter', 'HANKOOK', '215', '50', '17', '95', 'V', '', ''],
    ['samochody terenowe', 'all-season', 'YOKOHAMA', '31', '10.5', '15', '109', 's', '', '']
]

def generate_link(excel_row):
    # driver.get("https://www.oponeo.pl/wybierz-opony/")
    wait = WebDriverWait(driver, 35)
    # set root url and permanent category for car tires
    root_var = 'https://www.oponeo.pl'
    tire_type = '/wybierz-opony'

    # vehicle type example output(/t=1/osobowe)
    if len(excel_row[0]) == 0:
        len_selected_vehivle_types = '/t=3/'
        vehicle_types = 'dostawcze,osobowe,4x4'
    else:
        len_selected_vehivle_types = '/t=1/'
        vehicle_types = excel_row[0].lower().replace(' ', '-').replace('+', '')
        if 'dostawcze' in vehicle_types:
            vehicle_types = 'dostawcze'
        elif 'osobowe' in vehicle_types:
            vehicle_types = 'osobowe'
        elif 'terenowe' in vehicle_types:
            vehicle_types = '4x4'

    # season type example output(/s=3/letnie)
    if len(excel_row[1]) == 0 or 'all-season' in excel_row[1]:
        len_selected_seasons_types = '/s=3/'
        seasons_types = 'letnie,zimowe,caloroczne'
    else:
        len_selected_seasons_types = '/s=1/'
        seasons_types = excel_row[1].replace(' ', '').lower()
        if 'winter' in seasons_types:
            seasons_types = 'zimowe'
        elif 'summer' in seasons_types:
            seasons_types = 'letnie'
        elif 'all_year' in seasons_types:
            seasons_types = 'caloroczne'

    # brand example output(/p=1/bridgestone)
    if len(excel_row[2]) == 0:
        len_selected_brand = ''
        vehicle_brands = ''
    else:
        len_selected_brand = '/p=1/'
        vehicle_brands = excel_row[2].lower().replace(' ', '-').replace('+', '')

    # tire size example output(/r=1/225-60-r16)
    if len(excel_row[3]) == 0 and len(excel_row[4]) == 0 and len(excel_row[5]) == 0:
        complete_tire_size = ''
    else:
        tire_parameter_1 = '/r=1/'
        tire_size_2 = excel_row[3]  # '/225'
        tire_size_3 = excel_row[4]  # '/60'
        tire_size_4 = excel_row[5]  # '/16'
        complete_tire_size = f'{tire_parameter_1}{tire_size_2}-{tire_size_3}-r{tire_size_4}'

    # vehicle capacity example output(/in=1/101-99)
    if len(excel_row[6]) == 0:
        len_selected_vehivle_capacity = ''
        vehicle_capacity = ''
    else:
        len_selected_vehivle_capacity = '/in=1/'
        vehicle_capacity = excel_row[6].replace('/', '-').replace(' ', '').lower()

    # speed example output(ip=1/h)
    if len(excel_row[7]) == 0:
        len_selected_vehivle_speed = ''
        vehicle_speed = ''
    else:
        len_selected_vehivle_speed = '/ip=1/'
        vehicle_speed = excel_row[7].lower().replace(' ', '')

    # run on flat checkbox example output(/o=1/run-flat)
    if 'run-on-flat' in excel_row[8]:
        run_flat_1 = '/o=1/'
        run_flat_2 = 'run-flat'
    else:
        run_flat_1 = ''
        run_flat_2 = ''

    link = f'{root_var}{tire_type}{len_selected_seasons_types}{seasons_types}{len_selected_vehivle_types}{vehicle_types}{len_selected_brand}{vehicle_brands}{complete_tire_size}{len_selected_vehivle_speed}{vehicle_speed}{len_selected_vehivle_capacity}{vehicle_capacity}{run_flat_1}{run_flat_2}'

    driver.get(link)
    wait_page_load(driver)
    #
    # # Wzmacniane checkbox js click example output(#&&/wEXDgUOcGN....)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'reinforced')))
    # if 'C' in excel_row[9] or 'CP' in excel_row[9] or 'RF' in excel_row[9] or 'XL' in excel_row[9]:
    #     if not 'checked="checked"' in driver.find_element_by_xpath(
    #             '/html/body/form/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').get_attribute(
    #             'outerHTML'):
    #         driver.find_element_by_xpath(
    #             '/html/body/form/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').click()
    #     # reinforced = '#&&/'
    #     # reinforced_code = 'wEXDgUOcGN....'
    # else:
    #     if 'checked="checked"' in driver.find_element_by_xpath(
    #             '/html/body/form/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').get_attribute(
    #             'outerHTML'):
    #         driver.find_element_by_xpath(
    #             '/html/body/form/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]').click()
    #         time.sleep(2)
    #     reinforced = ''
    #     reinforced_code = ''
    # # print(link)

class Tires(object):
    def __init__(self, clas, name, sub_name, parameters, price_old, price, delivery, montage, time_delivery, return_period, pay,
                 opinions, rating, medal, type, season, size, speed, weight, inne, year, warranty, eco, weather, noise, bonus, link):
        self.clas = clas,    self.price_old = price_old ,           self.time_delivery = time_delivery     ,self.rating = rating  ,self.size = size   ,self.year = year
        self.name = name,    self.price = price, self.link = link,    self.return_period = return_period    ,self.medal = medal  ,self.speed = speed  ,self.warranty = warranty
        self.sub_name = sub_name, self.delivery = delivery,          self.pay = pay, self.link = link        ,self.type = type  ,self.weight = weight  ,self.eco = eco
        self.parameters = parameters, self.montage = montage,         self.link = opinions, self.link = opinions    ,self.season = season    ,self.inne = inne  ,self.weather = weather  ,
        self.noise = noise,   self.bonus = bonus,   self.link = link,

# generate_link(excel_row[3])

for x in range(2):

    meta = driver.find_elements_by_xpath('//*[@id="_upTL"]/div/div/div/div[1]/div[2]/div/a')

    for p in meta:
        links.append(p.get_attribute('href'))

    page = driver.find_element_by_id('resultsList')
    ActionChains(driver).move_to_element(page).perform()

    if x == 0:
        next_page = '//*[@id="_ctPgrp_pi2i"]'
        page = driver.find_element_by_xpath(next_page)
    else:
        try:
            next_page = '/html/body/form/div[6]/div[8]/div/ul/li[4]/a'
            page = driver.find_element_by_xpath(next_page)
        except:
            next_page = '/html/body/form/div[5]/div[8]/div/ul/li[4]/a'
            page = driver.find_element_by_xpath(next_page)
    try:
        driver.find_element_by_class_name('button').click()
        driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
        time.sleep(2)
    except:
        pass

    trying = 0
    while True:
        try:
            page.click()
            break
        except:
            time.sleep(1)
            trying = trying + 1
            if trying == 20:
             break


for link in links:

    driver.get(link)

    # =============    NAME

    try:
        text = driver.find_element_by_class_name('class')
        print('Class:')
        print(text.text)
    except:
        pass

    text = driver.find_element_by_class_name('producer')
    print('Producer:')
    print(text.text)

    text = driver.find_element_by_class_name('model')
    print('Model:')
    print(text.text)

    text = driver.find_element_by_class_name('size')
    print('Size:')
    print(text.text)

    # =============    PRICE

    info = driver.find_element_by_class_name('priceInfo')

    print('Old Price:')
    print(between(info.text,'Wcześniej',' '))

    print('New price:')
    print(between(info.text, 'zł', 'zł').strip('\n'))


    # =============    DELIVERY

    info = driver.find_element_by_class_name('delivery')
    chunks = info.text.splitlines()

    if 'Transport' in chunks:
        print('Delivery:')
        print(chunks[chunks.index("Transport") + 1])

    if 'Możliwość montażu' in chunks:
        print('Montage:')
        print(chunks[chunks.index("Możliwość montażu") + 1])

    if 'Doręczymy we' in chunks:
        print('Delivery time:')
        print(chunks[chunks.index("Doręczymy we") + 1])

    if 'na zwrot' in chunks:
        print('Return time:')
        print(chunks[chunks.index("na zwrot") - 1])

    if 'Zakupy' in chunks:
        print('Pay on:')
        print(chunks[chunks.index("Zakupy") + 1])

    text = driver.find_element_by_class_name('stockLevel')

    print('Numbers in Stock:')
    print(between(text.get_attribute("data-tpd"),'Ponad','sztuk').strip(" "))

    # =============    TESTS
    try:
        info = driver.find_element_by_class_name('tireTests')
        print('Passed tests:')
        print(info.text)
    except:
        pass

    info = driver.find_element_by_class_name('parameters')
    chunks = info.text.splitlines()

    if 'Typ:' in chunks:
        print('Type:')
        print(chunks[chunks.index("Typ:") + 1])

    if 'Sezon:' in chunks:
        print('Season:')
        print(chunks[chunks.index("Sezon:") + 1])

    if 'Rozmiar:' in chunks:
        print('Size:')
        print(chunks[chunks.index("Rozmiar:") + 1])

    if 'Indeks prędkości:' in chunks:
        print('Speed:')
        print(chunks[chunks.index("Indeks prędkości:") + 1])

    if 'Indeks nośności:' in chunks:
        print('Waight:')
        print(chunks[chunks.index("Indeks nośności:") + 1])

    if 'Inne:' in chunks:
        print('Inne:')
        print(chunks[chunks.index("Inne:") + 1])

    if 'Rok produkcji:' in chunks:
        print('Year of production:')
        print(chunks[chunks.index("Rok produkcji:") + 1])

    if 'Gwarancja:' in chunks:
        print('Warnity:')
        print(chunks[chunks.index("Gwarancja:") + 1])

    if 'Etykieta UE:' in chunks:
        text = chunks[chunks.index("Etykieta UE:") + 1]
        parts = text.split()
        print('Economy class:')
        print(parts[0])
        print('Wet road class:')
        print(parts[1])
        print('Noise:')
        print(parts[2])

    print('-----------------------------------')

    time.sleep(1)





#
# atrs = driver.execute_script(
#          'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',text)
#


