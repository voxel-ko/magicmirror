from flask import Flask, render_template, redirect, request
from . import weather_data, calendar_data

def create_app():
    app = Flask(__name__)

    # remove cache
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.route("/old")
    def old():
        return render_template("old.html")

    @app.route("/")
    def root():
        return render_template("index.html")

    @app.route("/api/weather_data", methods=["GET"])
    def api_weather_data():
        return weather_data.get_weather_data(logger=app.logger, ttl_hash=weather_data.get_ttl_hash())

    @app.route("/api/week_data", methods=["GET"])
    def api_week_data():
        return calendar_data.get_week()

    return app