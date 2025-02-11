import datetime
import os
import certifi

from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

# app factory helps to create only one app
def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())

    app.db = client.microblog

    # methods are arguments
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            # form is dictionary
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    @app.route("/recent")
    def recent():
        return render_template("recent.html")

    @app.route("/calendar")
    def calendar():
        return render_template("calendar.html")

    return app
