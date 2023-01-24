from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time


def open_browser(browser, fuel_type):
    """Function that opens a browser and loads rv.campingworld.com website with motorhomes for sale page.
    Args:
        browser (Selenium webdriver object)
        fuel_type (str): One of the following: Diesel, Gas or Gas & Diesel

    """
    # declare url and open a browser
    website = 'https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=' \
              'new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,' \
              'class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype={}&sort=featured_asc' \
              '&search_mode=advanced&locations=nationwide'.format(fuel_type)

    browser.maximize_window()
    browser.get(website)

    # let the page load
    time.sleep(3)


def get_pages(browser):
    """Function that returns total number of pages with listings
    Args:
        browser (Selenium webdriver object)
    Returns:
        Number of pages (int)
    """
    # get total number of results and number of web pages
    total = browser.find_element(by=By.XPATH, value="//span[@class='count-num']")
    total_num = total.text.replace(',', '')
    total_int = int(total_num)

    # calculate the number of pages, there are 20 results per page
    num_of_pages = round((total_int / 20))

    return num_of_pages


def find_by_xpath(browser, xpath):
    """Function that finds elements by xpath.
    Args:
        browser (Selenium webdriver object)
        xpath (str): xpath string
    Returns:
        The list of web elements
        """
    # try to find elements by xpath, if the page did not load yet then wait 10 seconds, and try again
    try:
        elements = browser.find_elements(by=By.XPATH, value=xpath)
        return elements
    except (NoSuchElementException, StaleElementReferenceException):
        time.sleep(10)
        elements = browser.find_elements(by=By.XPATH, value=xpath)
        return elements


def scrape_webpage(browser):
    """Function to scrape elements from the webpage and append results to empty lists declared outside of function.
    Args:
        browser (Selenium webdriver object)
    """

    time.sleep(3)
    # search for needed data using xpath locators
    prices = find_by_xpath(browser=browser, xpath="//span[@class='price-info low-price ']")
    stocks_loc = find_by_xpath(browser=browser, xpath="//span[@class='stock-results']")
    statuses = find_by_xpath(browser=browser, xpath="//span[@class='status']")
    specs = find_by_xpath(browser=browser, xpath="//div[@class='specs']")
    urls = find_by_xpath(browser=browser, xpath="//a[@class='productTitle']")

    # bring in global variables inside a function
    global price_raw
    global stock_loc_raw
    global status_raw
    global specs_raw
    global url_list

    # iterate over web element objects, extract text and append to lists
    for i in prices:
        price_raw.append(i.text)

    for i in stocks_loc:
        stock_loc_raw.append(i.text)

    for i in statuses:
        status_raw.append(i.text)

    for i in specs:
        specs_raw.append(i.text)

    for i in urls:
        url_list.append(i.get_attribute('href'))

    # click next page if it exists
    try:
        next_page = browser.find_element(by=By.XPATH, value='//a[@class="pag-btn next"]')
        next_page.click()
        time.sleep(5)
    except NoSuchElementException:
        print('The script reached the last page')


def get_horsepower(browser, url):
    """Function to scrape horsepower of a listing.
    Args:
        browser (Selenium webdriver object)
        url (str): URL with listing details
    Returns:
        Horsepower (int) OR 'no data' string
    """
    # open a browser and load webpage
    browser.get(url)
    # search for listing details
    time.sleep(3)
    horsepower = find_by_xpath(browser=browser, xpath="//div[@class='oneSpec clearfix']")

    # initiate empty list to hold the scraped data
    holder = []

    # iterate over web element objects and extract horsepower of a listing
    for i in horsepower:
        if "horsepower" in i.text.lower():
            holder.append(i.text.replace('HORSEPOWER\n', ''))

    # if horsepower is not provided then return no data string
    if ''.join(holder) == "":
        return 'no data'
    else:
        return ''.join(holder)


def clean_results(price_list, status_list, stock_loc_list, specs_list):
    """Function to clean the scraped data.
    Args:
        price_list, status_list, stock_loc_list, specs_list: lists with previously scraped data
    Returns:
        clean_status, clean_length, clean_sleeps, clean_price, stock_list, location_list: lists with clean data
    """

    # initiate empty lists that will hold clean data
    length_list = []
    sleeps_list = []
    clean_length = []
    clean_sleeps = []
    clean_price = []
    stock_list = []
    location_list = []

    # remove empty strings from lists
    price_list_no_blanks = list(filter(None, price_list))
    stock_loc_list_no_blanks = list(filter(None, stock_loc_list))
    clean_status = list(filter(None, status_list))

    # iterate over elements in specs_list and extract length
    for el in specs_list:
        if 'length' in el.lower():
            length_list.append(el)

    for el in specs_list:
        if 'sleeps' in el.lower():
            sleeps_list.append(el)

    # clean length, sleeps, price and stock_loc lists, append the results to new lists
    for el in length_list:
        clean_length.append(el.replace('Length (ft)\n', ''))

    for el in sleeps_list:
        clean_sleeps.append(el.replace('Sleeps\n', ''))

    for el in price_list_no_blanks:
        new_el = el.replace('$', '').replace(',', '')
        clean_price.append(new_el)

    for el in stock_loc_list_no_blanks:
        if 'stock #' in el.lower():
            stock_list.append(el.replace('Stock #', '').strip())
        else:
            location_list.append(el)

    return clean_status, clean_length, clean_sleeps, clean_price, stock_list, location_list


# start measuring execution time
start_time = time.time()

# declare empty lists that will be used to hold the scraped data
price_raw = []
stock_loc_raw = []
status_raw = []
specs_raw = []
url_list = []

# initiate Chrome web driver object
path = 'chromedriver.exe'
driver = webdriver.Chrome(path)

# open website with diesel listings
open_browser(browser=driver, fuel_type='diesel')

# get total number of pages
num_of_pages = get_pages(browser=driver)

print('scraping data...')

# run the scrape webpage function on each page
page = 1
while page <= num_of_pages:
    print("scraping page nr {} out of {}...".format(page, num_of_pages))
    scrape_webpage(browser=driver)
    page += 1


print('cleaning scraped data...')

# clean scraped data and put it into lists
status_list, length_list, sleeps_list, price_list, stock_list, location_list = clean_results(price_list=price_raw,
                                                                                             status_list=status_raw,
                                                                                             stock_loc_list=stock_loc_raw,
                                                                                             specs_list=specs_raw)

# convert lists into a dataframe
df = pd.DataFrame(list(zip(stock_list, status_list, price_list, sleeps_list, length_list, location_list, url_list)),
               columns=['Stock #', 'Status', 'Price', 'Sleeps', 'Length', 'Location', 'URL'])


# filter out listings above 300k
df['Price'] = df['Price'].astype(int)
df_over_300 = df[df['Price'] > 300000]

# if there are listings above 300k then scrape horsepower data
if not df_over_300.empty:

    print('collecting horsepower...')

    # initiate empty dictionary that will hold stock # and horsepower
    horsepower_dict = {}

    # iterate over urls of listings above 300k and get horsepower
    for index, row in df_over_300.iterrows():
        url = row["URL"]
        i = index

        # get horsepower data
        horsepower = get_horsepower(browser=driver, url=url)

        # append scraped data to the dictionary
        horsepower_dict[i] = horsepower

    print('finishing up...')

    # convert dictionary into a df
    new_df = pd.DataFrame.from_dict(horsepower_dict, orient='index')
    new_df.columns = ['Horsepower']

    # join newly created df with the old one on index
    joined = df.join(new_df)

    # drop url column
    joined.drop('URL', axis=1, inplace=True)

    # save the output to csv
    joined.to_csv("output.csv", index=False)

else:
    print('finishing up...')

    # drop url column
    df.drop('URL', axis=1, inplace=True)

    # save the output to csv
    df.to_csv("output.csv", index=False)

# close the browser
driver.quit()

# calculate execution time in minutes
elapsed_time = (time.time() - start_time) / 60

print("The script execution time is: {} minutes".format(round(elapsed_time, 2)))

