#scraping for location

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.expedia.com/Hotel-Search?adults=2&d1=2020-10-28&d2=2020-10-29&destination=Turkey&endDate=2020-10-29&latLong=39.09573098839464%2C34.8485632020327&regionId=183&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2020-10-28&theme=&useRewards=false&userIntent")
time.sleep(5)


# scroll down

x = len(driver.find_elements_by_xpath(
    "//button[@data-stid='show-more-results']"))
driver.find_element_by_xpath("//button[@data-stid='show-more-results']").send_keys(Keys.END)
while (x > 0):
    try:
        a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-stid='show-more-results']")))
    except:
        print("Loading took too much time!")
        break
    actions = ActionChains(driver)
    actions.move_to_element(a).perform()
    time.sleep(5)
    actions.move_to_element(a).perform()
    a.click()
    time.sleep(5)
    x = len(driver.find_elements_by_xpath(
        "//button[@data-stid='show-more-results']"))

#get elements
try:
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//li[@data-stid='property-listing']"))
    )

except Exception as e:
    print(e)
    driver.quit()
    
#dict. for data
data = {}    
data.setdefault("hotel_name", [])
data.setdefault("longitude_latitude", [])

for element in elements:
    try:
        element.click()
        driver.switch_to.window(driver.window_handles[1])
        hotel = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//div[@data-stid='content-hotel-title']")))
    except:
        driver.refresh()
        hotel = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//div[@data-stid='content-hotel-title']")))    
    #hotel name    
    try:
        hotel_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        data["hotel_name"].append(hotel_name.text)

    except:

        data["hotel_name"].append(None)
        
    #langitude, longitude    
    try:
        lang_long = driver.find_element_by_xpath("//figure[@class='uitk-image uitk-rounded-border-top uitk-rounded-border-bottom map__image image-loader image-loader--lazy image-loader__no-scrim']")
        data["longitude_latitude"].append(lang_long.get_attribute('style'))
    except:
        data["longitude_latitude"].append(None) 
        
    

    driver.close()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

#save as csv
df = pd.DataFrame(data=data)
compression_opts = dict(method='zip', archive_name='expedia_hotel_locations.csv')
df.to_csv('expedia_hotel_location_dataset.zip', index=False,
          compression=compression_opts)









