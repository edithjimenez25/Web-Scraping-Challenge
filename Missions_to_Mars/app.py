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
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")

#################################################
# Flask Routes
#################################################
#
# Create the root route to query MongoDB and pass Mars_data into index.html template to display the data

# Main Route
@app.route("/")
def home():
    # Find data using mongodb 
    mars_info = mongo.db.collection.find_one()

    #return template and data using jinja 
    return render_template("index.html", news=mars_info)

# Create a Scrape Route to Import `scrape_mars.py` Script and call the `scrape` Function
@app.route("/scrape")
def scrape():

    #run the scrape functions
    mars_info = scrape_mars.scrape_data()

    # Delete previously stored data
    mongo.db.mars_data.drop()

    # Update Mongo database using update and upsert = true
    mongo.db.collection.update({}, mars_info, upsert=True)

    # Performing URL redirection to the home page
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)

