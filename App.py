#################################################
## Step 2 - MongoDB and Flask Application
#################################################
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# Store the return value in Mongo as a Python dictionary.
# Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements.
#
#################################################
# MongoDB and Flask Application
#################################################

# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask Setup
#################################################
# Create an instance for flask app
app = Flask(__name__)


#################################################
# PyMongo Connection Setup
#################################################
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#################################################
# Flask Routes
#################################################

# Create the root route to query MongoDB and pass Mars_data into index.html template to display the data
# Main Route
@app.route("/")

def home():
    # Find data using mongodb 
    mars_data = mongo.db.colletion.find_one()
    
    #return using jinja template
    return render_template("index.html", data=mars_data)

# Create a Scrape Route to Import `scrape_mars.py` Script and call the `scrape` Function
# Scrape Route
@app.route("/scrape")
def scrape():
    #scrape the website
    mars_space = scrape_mars.scrape_info()
    # Remove store data
    mongo.db.collection.update({}, mars_space, upsert=True)
    # Performing URL redirection to the home page
    return redirect("/")

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)