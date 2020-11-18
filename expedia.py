from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd


PATH = "your path"

driver = webdriver.Chrome(PATH)

#################

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

# dict. for data
data = {}
data.setdefault("hotel_name", [])
data.setdefault("overall_rating", [])
data.setdefault("total_review", [])
data.setdefault("location", [])
data.setdefault("cleanliness_rating", [])
data.setdefault("service_rating", [])
data.setdefault("amenities_rating", [])
data.setdefault("facilities_rating", [])
data.setdefault("total_photo", [])
data.setdefault("room_rating", [])
data.setdefault("room_size", [])
data.setdefault("number_of_amenities", [])
data.setdefault("price", [])

for element in elements:
    try:
        element.click()
        driver.switch_to.window(driver.window_handles[1])
        hotel = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//div[@data-stid='content-hotel-title']")))
    except:
        driver.switch_to.window(driver.window_handles[1])
        driver.sendKeys(Keys.F5)
        hotel = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//div[@data-stid='content-hotel-title']")))
    # hotel name

    try:
        hotel_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        data["hotel_name"].append(hotel_name.text)

    except:

        data["hotel_name"].append(None)

    # rating

    try:
            
        rating = driver.find_element_by_xpath("//h3[@class='uitk-type-heading-500 uitk-flex-item']")
        data["overall_rating"].append(rating.text)

    except:

        data["overall_rating"].append(None)

    # reviews

    try:

        reviews = driver.find_element_by_xpath("//button[@data-stid='reviews-link']")
        data["total_review"].append(reviews.text)

    except:

        data["total_review"].append(None)

    # location

    try:

        locations = driver.find_element_by_xpath("//span[@itemprop='address']")
        data["location"].append(locations.text)

    except:

        data["location"].append(None)

    # Other Ratings(cleanliness, service, amenities, facilities ratings)

    try:
        reviews = driver.find_element_by_xpath("//a[@href='#Reviews']").click()
        all_rating = []
        ratings = driver.find_elements_by_xpath("//div[@class='uitk-flex uitk-flex-column uitk-flex-item uitk-flex-basis-half_width all-y-margin-three']")
        for i in ratings:
            all_rating.append(i.find_element_by_tag_name("h3").text)

        data["cleanliness_rating"].append(all_rating[0])
        data["service_rating"].append(all_rating[1])
        data["amenities_rating"].append(all_rating[2])
        data["facilities_rating"].append(all_rating[3])

    except:

        data["cleanliness_rating"].append(None)
        data["service_rating"].append(None)
        data["amenities_rating"].append(None)
        data["facilities_rating"].append(None)

    # Total Number of Photos

    try:

        total_photos = driver.find_element_by_xpath("//button[@class='uitk-button uitk-button-small uitk-button-has-text uitk-button-overlay']")
        data["total_photo"].append(total_photos.text)

    except:

        data["total_photo"].apped(None)

    # room rating

    try:
        driver.find_element_by_xpath("//a[@href='#Offers']").click()
        time.sleep(1)
        room_ratings = driver.find_element_by_xpath("//div[@data-stid='room-score-text']")
        data["room_rating"].append(room_ratings.text)

    except:
        data["room_rating"].append(None)

    # room size

    try:

        room_sizes = driver.find_element_by_xpath("//span[@class='all-l-padding-two']")
        data["room_size"].append(room_sizes.text)

    except:
        data["room_size"].append(None)

    # price

    try:

        prices = driver.find_element_by_xpath("//span[@data-stid='content-hotel-lead-price']")
        data["price"].append(prices.text)

    except:

        data["price"].append(None)

    # Total Number of Amenities

    try:
            
        amenities = driver.find_elements_by_xpath("//li[@class='uitk-spacing uitk-layout-grid-item']")
        data["number_of_amenities"].append(len(amenities) - 1)

    except:
            
        data["number_of_amenities"].append(None)


    driver.close()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

#save as csv
df = pd.DataFrame(data=data)
compression_opts = dict(method='zip', archive_name='expedia_hotel_dataset.csv')
df.to_csv('expedia_hotel_dataset.zip', index=False,
          compression=compression_opts)
