from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app)



@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars_info=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_info = scrape_mars.scrape()
    mars.update({}, mars_info, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)