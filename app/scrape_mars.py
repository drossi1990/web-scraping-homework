import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime as dt
import urllib.request
from selenium import webdriver

def scrape_all():
    #starting browser
    browser = Browser("chrome", executable_path="../chromedriver", headless=True)
    MarsNews_title, MarsNews_paragraph = mars_news_pull(browser)
    #dict to contain scraped values
    marsdata = {
        "MarsNews_title": MarsNews_title,
        "MarsNews_paragraph": MarsNews_paragraph,
        "image_link": image_link(browser),
        "facts": get_mars_facts(),
        "hemispheres": hemisphere(browser),
        "date_time": dt.datetime.now()   
        }

    browser.quit()
    return marsdata

def mars_news_pull(browser):
    marsnewsurl = "https://mars.nasa.gov/news"
    browser.visit(marsnewsurl)
    time.wait(1)
    html=browser.html
    news_soup = bs(html, 'html.parser')

#Retrieve current title and article teaser from NASA Mars news url
    try:
        MarsNews_title = news_soup.find("div", class_="bottom_gradient").text
        MarsNews_paragraph = news_soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None

    return MarsNews_title, MarsNews_paragraph

def image_link(browser):

#note NASA space images no longer has a featured image, in contrast to when this was assigned
#navigates to JPLs daily image page, selects first image, and then copies the SRC of that image for later use
    jpl_url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    browser.visit(jpl_url)
    time.sleep(1)
    elems = browser.find_by_tag("a")
    link = elems[6]['href']
    browser.visit(link)
    time.sleep(1)
    elems = browser.find_by_tag("img")
    time.sleep(1)
    try:
        image_link = elems[2]['src']
    except AttributeError:
        return None

    return image_link

def get_mars_facts():

    #Mars facts, reading table
    mars_facts_url = "https://space-facts.com/mars/"
    try:
        mars_table = pd.read_html(mars_facts_url)
    except BaseException:
        return None

    mars_df = mars_table[0]
    mars_df.columns = ["Characteristics", "Value"]
    mars_df.set_index(["Characteristics"])

    return mars_df.to_html(classes="table table-striped")

def hemisphere(browser):

    #Mars Hemisphere

    url = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.visit(url)

    #loops through links 
    hemisphere_image_urls = []
    for link in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[link].click()
        Sample = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = Sample['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return(hemisphere_image_urls)



