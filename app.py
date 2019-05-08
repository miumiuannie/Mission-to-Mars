from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    data = scrape_mars.scrape_mars_news()
    mars_data.update({}, data, upsert=True)
    data = scrape_mars.scrape_mars_images()
    mars_data.update({}, data, upsert=True)
    data = scrape_mars.scrape_mars_facts()
    mars_data.update({}, data, upsert=True)
    data = scrape_mars.scrape_mars_weather()
    mars_data.update({}, data, upsert=True)
    data = scrape_mars.scrape_mars_hemispheres()
    mars_data.update({}, data, upsert=True)
    
if __name__ == "__main__": 
    app.run(debug=True)




