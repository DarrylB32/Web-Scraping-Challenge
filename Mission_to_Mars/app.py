# Import dependencies
from flask import Flask, render_template, redirect
import mars_scrape as ms
import pymongo


# Create an instance of our Flask app.
app = Flask(__name__)
# Pass connection to the pymongo instance.
client = pymongo.MongoClient()

# Connect to the mission_to_mars database. Will create one if not already available.
db = client.mission_to_mars

# Will create a scarped data collection. Will create one if not already available.
scraped_data_col = db.scraped_data

@app.route("/")
def index():
    return render_template("index.html", scraped_data=list(scraped_data_col.find())[-1])

@app.route("/scrape")
def scraper():
    scraped_data = scraped_data_col
    new_data = ms.scrape() #Execute mars_scrape.scrape() function
    scraped_data.insert_one(new_data)
    return redirect("/", code=302) 

if __name__ == "__main__":
    app.run(debug=True)