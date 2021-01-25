# Import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape():
    # Website to be scraped
    url = 'https://mars.nasa.gov/news/'

   # Retrieves page to be scraped with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    news_articles = BeautifulSoup(response.text, 'html.parser')

    # Extracts the titles for all articles
    titles = news_articles.find_all('div', class_ = 'content_title')

    # Extracts descriptions all articles
    articles = news_articles.find_all('div', class_ = 'rollover_description_inner')
    
    # Append titles and their descriptions to list
    news_title=[]
    news_p=[]
    for title in titles:
        news_title.append(title.text.strip())
        
    for article in articles:
        news_p.append(article.text.strip()) 
 
    # Open chrome browser to use for scraping
    executable_path = {'executable_path':'C:\\Users\\dbayn\\Anaconda3\\webdrivers\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
   
    # Website to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Open chrome browser to use for scraping
    browser.visit(url)

    # Retrieves page with the requests module
    response=requests.get(browser.url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_image = BeautifulSoup(response.text, 'html.parser')

    #Scrape through page for featured image url
    featured_image_url = soup_image.find('article', class_= "carousel_item")
    featured_image_url='https://www.jpl.nasa.gov'+featured_image_url.find('a')['data-fancybox-href']
    #featured_image_url

    # Extract tabes from space-facts website
    url="https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_facts=tables[0].to_html(header=False, index=False)

    # Website to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Open website in chromedriver
    browser.visit(url)

    # Retrieve page with the requests module
    response=requests.get(browser.url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup_hemisphere = BeautifulSoup(response.text, 'html.parser')

    #List of data for hemisphere links
    hemisphere_links=soup_hemisphere.find_all('div', class_='item')

    # Create list of dictionaries containing mars image urls and titles 
    hemisphere_image_urls=[]
    for anchor in hemisphere_links:
        title=anchor.find('a').text
        browser.click_link_by_partial_text(title)
        html = browser.html
        link = BeautifulSoup(html, 'html.parser')
        link=link.find('li').find('a')['href']
        dictionary={'title':title,
                'image_url':link}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    
    hemisphere_image_urls

    # Appends all lists and scraped data to one dictionary 
    mars_dict_all={
        'news_titles': news_title,
        'news_articles': news_p,
        'featured_image': featured_image_url,
        'mars_facts': mars_facts,
        'mars_weather': 'Input Weather Here',
        'mars_hemispheres': hemisphere_image_urls
    }
    
    # Close chromedriver
    browser.quit()

    # Return dictionary
    return mars_dict_all
