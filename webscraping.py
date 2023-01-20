from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


fuel_type = 'diesel'

# initiate the chrome driver and declare the url
website = 'https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=' \
          'new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,' \
          'class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype={}&sort=featured_asc' \
          '&search_mode=advanced&locations=nationwide'.format(fuel_type)

path = 'chromedriver.exe'
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(website)

time.sleep(2)

# get total number of results
total = driver.find_element(by=By.XPATH, value="//span[@class='count-num']")
total_num = total.text.replace(',', '')
total_int = int(total_num)

price_list = []
stock_list = []
status_list = []
specs_list = []
lenght_list = []
sleeps_list = []

prices = driver.find_elements(by=By.XPATH, value="//span[@class='price-info low-price ']")
stocks = driver.find_elements(by=By.XPATH, value="//span[@class='stock-results']")
statuses = driver.find_elements(by=By.XPATH, value="//span[@class='status']")
specs = driver.find_elements(by=By.XPATH, value="//div[@class='specs']")

# iterate over web element objects, extract text and append to lists
for i in prices:
    price_list.append(i.text)

for i in stocks:
    stock_list.append(i.text)

for i in statuses:
    status_list.append(i.text)

for i in specs:
    specs_list.append(i.text)

# remove empty strings from lists
price_list = list(filter(None, price_list))
status_list = list(filter(None, status_list))
stock_list = list(filter(None, stock_list))


# iterate over elements in specs_list and extract length
for el in specs_list:
    if 'length' in el.lower():
        lenght_list.append(el)

for el in specs_list:
    if 'sleeps' in el.lower():
        sleeps_list.append(el)





# # clicking through the accept cookies button
# cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
# cookies_button.click()
#
# time.sleep(2)
#
# # get total number of results
# total = driver.find_element(by=By.XPATH, value='//strong[@data-cy="search.listing-panel.label.ads-number"]')
# total_num = re.findall(r'\d+', total.text)
#
#
# # calculate the number of pages
# num_of_pages = round(int(total_num[0]) / 72)
#
# # initiate lists to store data
# location = []
# prices = []
# m2_price = []
# rooms = []
# m2 = []
# urls = []
#
# # define main function
# def scrape():
#
#     # scroll down the webpage to get all results
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(1)
#     # listings = driver.find_elements(by=By.XPATH, value='//div[@data-cy="search.listing"]')
#     # li_obj = listings[1].find_elements(by=By.TAG_NAME, value='article')
#
#     loc = driver.find_elements(by=By.XPATH, value='//p[@class="css-80g06k es62z2j12"]')
#     details = driver.find_elements(by=By.XPATH, value='//span[@class="css-s8wpzb eclomwz2"]')
#     links = driver.find_elements(by=By.XPATH, value='//a[@data-cy="listing-item-link"]')
#
#     # create a list of locations
#     for t in loc:
#         location.append(t.text)
#
#     # create a list of listing details
#     x = 0
#     while x < len(details):
#         prices.append(details[x].text)
#         m2_price.append(details[x+1].text)
#         rooms.append(details[x + 2].text)
#         m2.append(details[x + 3].text)
#         x += 4
#
#     for l in links:
#         urls.append(l.get_attribute('href'))
#
#     # click on the next button
#     next_button = driver.find_element(by=By.XPATH, value='//button[@data-cy="pagination.next-page"]')
#     next_button.click()
#
#     time.sleep(5)
#
#
#
# # run the function on each page
# i = 1
# while i < num_of_pages:
#     scrape()
#     i += 1
#
#
# #convert the lists into a dataframe
# df = pd.DataFrame(list(zip(location, prices, m2_price, m2, rooms, urls)),
#                columns =['Location', 'Price', 'Price per m2', 'Size M2', 'Rooms', 'URL'])
#
# # save the output to xlsx
# df.to_excel("data.xlsx", index=False)

# close the browser
#driver.quit()
