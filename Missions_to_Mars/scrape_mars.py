#################################################\n",
# Jupyter Notebook Conversion to Python Script\n",
#################################################\n",

# Step 2 - MongoDB and Flask Application
# Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` 
# with a function called `scrape` that will execute all of your scraping code from above 
# and return one Python dictionary containing all of the scraped data.

# Make Dependencies available
# Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time
import pymongo

##############################################################################################
# Connect to PyMongo to work with mongo database (MongoDB)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
##############################################################################################
### Mac Users 
# Choose the executable path to driver 
#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)
 
### Windows Users
# Choose the executable path to driver 
# Initiate the browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

##############################################################################################
## Scrape data from Mars ##
def scrape_data():
    # create a dictionary to store the data scrapped
    data_returned_dict = {}
### NASA Mars News
    try:
        # Initialize the browser
        browser = init_browser()
        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Allow the url to load
        time.sleep(1)

        # Create a beautiful soup object and scrape the page into the soup
        html = browser.html
        soup = bs(html, 'html.parser')

        # Scrape the Latest News Title and assign the text to a variable
        news = soup.find_all("div", class_="list_text")
        mars_news = []
        # Get the first news
        for story in news:
            title = story.find("div", class_="content_title").text
            paragraph = story.find('div', class_='article_teaser_body').text
            mars_news.append({'title': title, 'paragraph': paragraph})
       
        # return data scrapped in the dictionary
        data_returned_dict['title'] = mars_news[0]['title']
        data_returned_dict['paragraph'] = mars_news[0]['paragraph']
    
    # quit the browser
    finally:
        browser.quit()
        

##############################################################################################
### JPL Mars Space Images - Featured Image 
###
    try:
        # Initialize the browser
        browser = init_browser()  

        # Visit the URL Mars Space JPL  (Jet Propulsion Laboratory) Site and find the images UR:through splinter module
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)
        time.sleep(5)

        # Create a beautiful soup object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

        # Retrieve background-image url from style tag 
        image = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        jpl_url = 'https://www.jpl.nasa.gov'

        # Concatenate website jpl_url with scrapped route for the featured_image_url and obtain the complete link
        featured_image_url = jpl_url + image

        # return data scrapped in the dictionary
        data_returned_dict['featuredImage'] = featured_image_url
   
    # quit the browser
    finally:
        browser.quit()

##############################################################################################
### Mars Weather (Twitter)
#
    try:
        # Initialize the browser
        browser = init_browser()        
        # Visit the URL Mars Weather Twitter through splinter module
        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(twitter_url)
        time.sleep(1)

        # Create a beautiful soup object and parse results html
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

        # Find all elements that contain tweets on mars weather
        latest_tweets = soup.find_all('div', class_='InSight')

        # return the latest_tweets
        weatherTweet = "Error!"
        for tweet in latest_tweets: 
            weatherTweet = tweet.find_all('span').text
            if 'Sol' and 'pressure' in weatherTweet:
                print(weatherTweet)
                break
            else: 
                pass
        
        # return data scrapped in the dictionary
        data_returned_dict['weather'] = weatherTweet

        # quit the browser
    finally:
        browser.quit()    

##############################################################################################
### Mars Facts
# Visit the Mars Facts webpage (https://space-facts.com/mars/) and use Pandas to scrape the table 
# containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

    # Visit the URL https://space-facts.com/mars/ and scrape the table containing facts  
    space_facts_url = 'http://space-facts.com/mars/'

    # Use Panda's to scrape the url
    mars_facts = pd.read_html(space_facts_url)

    # Find the Mars facts in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns 'Description' and 'Value'
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    #Create HTML code for the Mars Facts Table
    facts = mars_df.to_html()

    # return data scrapped in the dictionary
    data_returned_dict['facts'] = facts

##############################################################################################
### Mars Hemispheres 
##
    try:
        # Initialize the browser
        browser = init_browser()

        # Visit hemispheres website through splinter module
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # Create a beautiful soup object and parse results html
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        
        # Obtain all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')
        
        # Create empty list for hemisphere image urls (hiu)
        hiu = []        

        # Store the main_url 
        main_url = 'https://astrogeology.usgs.gov'

        # Loop through the items 
        for i in items:
            # Store title
            title = i.find('h3').text

            # Navegating to the full images website, Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full images website 
            browser.visit(main_url + partial_img_url)

            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html  

            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')

            # Retrieve full image
            img_url = main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the data retrieved into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        # return data scrapped in the dictionary
        data_returned_dict['hemisphere'] = hiu
        
        # quit the browser
    finally:
        browser.quit()

    mars_info = {
        'title' : title,
        'paragraph': paragraph,
        'featuredImage': featured_image_url,
        'Weather': weatherTweet,
        'marsFacts': facts,
        'hemisphereImages': hiu
    }

    return mars_info

