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
# Connwct to PyMongo to work with mongo database (MongoDB)
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
### Create a Dictionary to archive the data to be imported into Mongo
mars_data = {}

### NASA Mars News 
def mars_news():
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
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        
        # Scrape the Latest News Title and assign the text to a variable
        # Retrieve the latest element that contains news title 
        news_title = soup.find("div", class_="content_title").text
        # Scrape the Latest News Paragraph and assign the text to a variable
        # Retrieve the latest element that contains news_paragraph 
        news_paragraph = soup.find('div', class_='article_teaser_body').text

        # Add dictionary to archive data from Nasa Mars News
        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = news_paragraph
        # Return Mars news (title and paragraph)
        return mars_data
    # quit the browser
    finally:
        browser.quit()

##############################################################################################
### JPL Mars Space Images - Featured Image 
def featured_image():
    try:
        # Initialize the browser
        browser = init_browser()        
        # Visit the URL Mars Space JPL  (Jet Propulsion Laboratory) Site and find the images UR:through splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        time.sleep(5)
        # Create a beautiful soup object
        # HTML Object 
        html_image = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')
        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        jpl_url = 'https://www.jpl.nasa.gov'

        # Concatenate website jpl_url with scrapped route for the featured_image_url and obtain the complete link
        featured_image_url = jpl_url + featured_image_url
        # display the featured image
        featured_image_url 
        # Add dictionary to entry the JPL Mars Space Images - Featured Image
        mars_data['featured_image_url'] = featured_image_url 
        # Return featured image
        return mars_data
    # quit the browser
    finally:
        browser.quit()

##############################################################################################
### Mars Weather (Twitter)
def weather_tweet():
    try:
        # Initialize the browser
        browser = init_browser()        
        # Visit the URL Mars Weather Twitter through splinter module
        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(twitter_url)
        time.sleep(1)

        # Create a beautiful soup object and parse results html
        # HTML Object
        mars_weather_html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(mars_weather_html, 'html.parser')

        # Find all elements that contain tweets on mars weather html
        mars_weather = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[0].text

        # return the latest_tweets
        for tweet in mars_weather: 
            weather_tweet = tweet.text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass
        # Add dictionary to archive data from Mars Weather Twitter
        mars_data['weather_tweet'] = weather_tweet

        # return the twitter scrape information
        return mars_data
    # quit the browser
    finally:
        browser.quit()    

##############################################################################################
### Mars Facts
# Visit the Mars Facts webpage (https://space-facts.com/mars/) and use Pandas to scrape the table 
# containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

def space_facts():
    # Visit the URL https://space-facts.com/mars/ and scrape the table containing facts  
    space_facts_url = 'http://space-facts.com/mars/'

    # Use Panda's to scrape the url
    mars_facts = pd.read_html(space_facts_url)

    # Find the Mars facts in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    #Create HTML code for the Mars Facts Table
    mars_facts_table = mars_df.to_html()
    
    # Add dictionary to archive data from Mars Facts webpage
    mars_data['mars_facts'] = mars_facts_table

    # Print the html code
    return mars_data

##############################################################################################
### Mars Hemispheres 

def hemispheres():
    try:
        # Initialize the browser
        browser = init_browser()        
        # Visit hemispheres website through splinter module
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        # HTML Object
        html_hemispheres = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')
        
        # Obtain all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')
        
        # Create empty list for hemisphere urls
        hemisphere_image_urls = []
        # Store the main_url 
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        # Loop through the items 
        for i in items:
            # Store title
            title = i.find('h3').text

            # Navegating to the full images website, Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full images website 
            browser.visit(hemispheres_main_url + partial_img_url)

            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html  

            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')

            # Retrieve full image
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the data retrieved into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
        # Add dictionary to archive data from Mars Hemispheres
        mars_data['hemisphere_image_urls'] = hemisphere_image_urls
        
        # Return mars_data dictionary with hemisphere_image_urls with title and image url
        return mars_data
    
    # quit the browser
    finally:
        browser.quit()