#################################################
## MongoDB and Flask Application
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
    mars_data = mongo.db.mars_data.find_one()

    #return template and data using jinja 
    return render_template("index.html", mars_data=mars_data)

# Create a Scrape Route to Import `scrape_mars.py` Script and call the `scrape` Function
@app.route("/scrape")
def scrape():
    #run the scrape functions
    mars_data = scrape_mars.mars_news()
    mars_data = scrape_mars.featured_image()
    mars_data = scrape_mars.weather_tweet()
    mars_data = scrape_mars.space_facts()
    mars_data = scrape_mars.hemispheres()

    # Update Mongo database using update and upsert = true
    mars_data = mongo.db.mars_data
    mars_data.update({}, mars_data, upsert=True)

    # Performing URL redirection to the home page
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)

