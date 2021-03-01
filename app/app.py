#----------------------------Companion Flask+Mongo DB App----------------------------
#dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

#setup
app = Flask(__name__)
#connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#routes
#mongodb query + passing mars data into HTML template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)
#route to import scrape_mars script + calling the scrape_all() function
@app.route("/scrape")
def scrapping():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data,upsert=True)
    return "Scrape Success"
    
if __name__ == "__main__":
    app.run()