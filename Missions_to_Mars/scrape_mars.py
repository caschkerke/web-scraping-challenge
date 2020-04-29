#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


# In[2]:


def init_browser():
    
    executable_path = {"executable_path": "geckodriver"}
    return Browser("firefox", **executable_path, headless=True)


# In[3]:


def scrape():
    
    browser = init_browser()
    mars_info = {}
   
    # Scraping latest news article regarding mars
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    mars_info["news_title"] = soup.find("div", class_="content_title").get_text()
    mars_info["news_text"] = soup.find("div", class_="article_teaser_body").get_text()
    
    # Scraping latest featured image data
    site_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(site_url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")

    image_url = soup.footer.a["data-fancybox-href"]
    url2 = "https://www.jpl.nasa.gov"
    
    featured_image_url = url2 + image_url
    mars_info["featured_img_url"] = featured_image_url
    
    # Scraping mars facts
    url3 = "https://space-facts.com/mars/"
    
    facts_df = pd.read_html(url3)
    mars_df = facts_df[0]
    mars_df.rename(columns={0: "Characteristics", 1: "Values"}, inplace=True)
    
    mars_html = mars_df.to_html()
    mars_html = mars_html.replace("\n", "")
    mars_info["mars_html"] = mars_html
    
    # Scraping hemisphere data 
    url_cerb = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    url_schi = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    url_syrt = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    url_vall = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"

    hemisphere_image_urls = []
    titles = []
    urls = [url_cerb, url_schi, url_syrt, url_vall]
    
    for url in urls:
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
        img_src = soup.find("img", class_="wide-image")["src"]
        img_link = "https://astrogeology.usgs.gov" + img_src
        title = soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(img_link)
        titles.append(title)
        
    hemispheres = {"title": titles, "img_url": hemisphere_image_urls}
    mars_info["hemispheres"] = hemispheres
    
    return mars_info


# In[4]:


scrape()


# In[ ]:


# Created and tested individual functions below before combining them within a completed scrape() function above


# In[5]:


# Scraping latest news article regarding mars

# def scrape_news():
    
#     browser = init_browser()
#     news = {}
    
#     url = "https://mars.nasa.gov/news/"
#     browser.visit(url)
#     time.sleep(1)
    
#     html = browser.html
#     soup = bs(html, "html.parser")
    
#     news['title'] = soup.find("div", class_="content_title").get_text()
#     news['para'] = soup.find("div", class_="article_teaser_body").get_text()

#     browser.quit()
    
#     return news


# In[6]:


# Scraping latest featured image data

# def scrape_image():
    
#     browser = init_browser()
    
#     site_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#     browser.visit(site_url)
#     time.sleep(1)
    
#     html = browser.html
#     soup = bs(html, "html.parser")

#     image_url = soup.footer.a["data-fancybox-href"]
#     url = "https://www.jpl.nasa.gov"
    
#     featured_image_url = url + image_url
    
#     browser.quit()
    
#     return featured_image_url


# In[7]:


# Scraping for latest tweet about weather

# def scrape_weather():
    
#     browser = init_browser()

#     url = "https://twitter.com/marswxreport?lang=en"
#     browser.visit(url)
#     time.sleep(1)

#     html = browser.html
#     soup = bs(html, "html.parser")

# # trying different parser?
#     soup = bs(html, "html5lib")

# #     trying to find the stored tweet at least within main
#     main = soup.body.main

# # checking all div and span
#     spans = main.find_all("span")  
#     divs = main.find_all("div") 

# # tweet text stored within an article tag when inspecting the site directly, attempting to access/find tag
#     article = main.section.article

# # found the tweet within inspector, trying to find it directly
#      mars_weather = soup.main.section.article.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

# # can't find article tag?? trying span 
#     mars_weather = soup.find_all("span")

# # trying to loop through what should be the html tag for tweets
#     tweets = soup.find_all("div", class_="js-tweet-text-container")
#     mars_weather = []

#     for tweet in tweets:
#         defining returns as what is supposed to be the class assignment for tweets
#         returns = tweet.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
#         mars_weather.append(returns)
        
#         return mars_weather
# # nothing found..

# # looping through all divs to check for article/correct span tags
#     for div in divs:
#           print(divs.prettify())

# # looping through spans again to make sure i didnt miss any
    
#     for span in spans:
#           print(span.prettify())

# # still no tweet text..


# # even base (soup) doesn't contain any article tags?????
#     print(soup)

# # I have no clue what to try at this point. API?? don't know how else I can find the tweet..


# In[8]:


# Scraping mars facts

# def scrape_facts():

#     url = "https://space-facts.com/mars/"
    
#     facts_df = pd.read_html(url)
#     mars_df = facts_df[0]
#     mars_df.rename(columns={0: "Characteristics", 1: "Values"}, inplace=True)
    
#     mars_html = mars_df.to_html()
#     mars_html = mars_html.replace("\n", "")
    
#     return mars_html


# In[9]:


# Scraping hemisphere data 

# def scrape_hemis():
    
#     browser = init_browser()
    
#     url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#     url_cerb = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
#     url_schi = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
#     url_syrt = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
#     url_vall = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"

#     hemisphere_image_urls = []
#     titles = []
#     urls = [url_cerb, url_schi, url_syrt, url_vall]
    
#     for url in urls:
#         browser.visit(url)
#         html = browser.html
#         soup = bs(html, "html.parser")
#         img_src = soup.find("img", class_="wide-image")["src"]
#         img_link = "https://astrogeology.usgs.gov" + img_src
#         title = soup.find("h2", class_="title").get_text()
#         hemisphere_image_urls.append(img_link)
#         titles.append(title)
        
#     hemispheres = {"title": titles, "img_url": hemisphere_image_urls}
    
#     return hemispheres


# In[ ]:




