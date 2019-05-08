from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape_mars_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find(class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    return mars_data

def scrape_mars_images():
    browser = init_browser()
    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)    

    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')

    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image_url

    mars_data['featured_image_url'] = featured_image_url 

    return mars_data

def scrape_mars_weather():

    try:
        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        html_image = browser.html
        soup = BeautifulSoup(html_image, 'html.parser')

        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
        if latest_tweets:
            latest_tweet = latest_tweets[0]
        else:
            latest_tweet = None
    except:
        print('Got exception')

    mars_data['latest_tweets'] = latest_tweet

    return mars_data

def scrape_mars_facts():
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Description','Value']
    mars_facts_df.set_index('Description', inplace=True)
    mars_results = mars_facts_df.to_html()
    mars_data['mars_facts'] = mars_results

    return mars_data

def scrape_mars_hemispheres():
    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_image = browser.html
        soup = BeautifulSoup(html_image, 'html.parser')

        items = soup.find_all('div', class_='item')

        hemisphere_image_urls = []
        hemispheres_main_url = 'https://astrogeology.usgs.gov'
        
        for item in items: 
            title = item.find('h3').text
            partial_img_url = item.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    except:
        print('Got exception')

    return mars_data