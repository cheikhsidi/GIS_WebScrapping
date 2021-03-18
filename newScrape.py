#Importing the dependencies
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
# from selenium import webdriver
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

count = 0
n = 0
def scrape():
    browser = init_browser()
    count = 0
    n = 0
    # mars = []
    names = []
    addresses = []
    data = {}
    for i in range(1,489):
        # News URL
        # if i < 12:
        #     url = "https://www.bigscreenbiz.com/directory/43-movie-theatre/53-independent-theatres"
        # else :
        try:

            url = f"https://www.bigscreenbiz.com/directory/43-movie-theatre/53-independent-theatres/page-{i}.html"
            browser.visit(url)
            html = browser.html
            soup = bs(html, "html.parser")
            # print(soup)
            listing = soup.find("div", id_="inside")
            # print(listing)
            listing = browser.find_by_css('.listing-summary')
            pages = browser.find_by_css('.pages-links')[0].find_by_tag("a")
            print(len(pages))
            # print(len(listing))
            for element in listing:

                # "div", class_="listing-summary").text
                address = element.find_by_css(".address").text
                name = element.find_by_css("h3").text
                names.append(name)
                addresses.append(address)
            n = n+1
        except :
            count = count+1

    # Close the browser after scraping
    browser.quit()
    data['Theater_name'] = names
    data['Address'] = addresses
    # print(data)
    df = pd.DataFrame(data)
    df.to_excel('bigscreenbiz.xlsx')
    return df

scrape()
