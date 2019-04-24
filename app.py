from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars



app = Flask(__name__)

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

@app.route("/")
def homepage():
   mars_data = mongo.db.mars_data.find_one()

   return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

   mars_data = mongo.db.mars_data

   mars_info = scrape_mars.scrape_news()
   mars_info = scrape_mars.scrape_image()
   mars_info = scrape_mars.scrape_weather()
   mars_info = scrape_mars.scrape_facts()
   mars_info = scrape_mars.scrape_hemispheres()

   mars_data.update({}, mars_info, upsert=True)

   return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)

