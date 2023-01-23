# Webscraping of rv.campingworld.com website

The script is written in Python and uses Selenium framework to automate Google Chrome browser and scrape web data.

On the high-level the process is as follows:
- The script opens a Google Chrome browser and loads the webpage with RV listings
- The data from each listing is scraped and put into separate lists
- Once the main scraping is done on all pages, the lists with data are cleaned off unnecessary characters
- The lists with clean data are transformed into a Pandas dataframe
- If there are listings with price above $300,000, the script scrapes horsepower from each listing's details page and saves it into a dictionary with index as keys and horsepower as values. Next, the dictionary is transformed into a Pandas dataframe and joined with the main dataframe on index.
- The resulting dataframe is saved as a csv file

Note: chromedriver.exe compatible to your browser is required to be in the working directory.
You can download it here:
https://chromedriver.chromium.org/
