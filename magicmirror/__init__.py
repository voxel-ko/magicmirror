import os.path

from flask import Flask, render_template, redirect, request, url_for
from . import weather_data, calendar_data

def create_app():
    app = Flask(__name__)

    # remove cache
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.route("/")
    def root():
        return render_template("index.html")

    @app.route("/api/weather_data", methods=["GET"])
    def api_weather_data():
        return weather_data.get_weather_data(logger=app.logger, ttl_hash=weather_data.get_ttl_hash())

    @app.route("/api/week_days", methods=["GET"])
    def api_week_days():
        return calendar_data.get_week()

    @app.route("/api/week_events", methods=["GET"])
    def api_week_events():
        with open(os.path.join(app.root_path, "basic.ics"), "r") as file:
            file_data = file.read()

        return calendar_data.events_around_date(calendar_data.read_calendar(file_data), 3, 3)

    @app.route("/api/upcoming_events", methods=["GET"])
    def api_upcoming_events():
        with open(os.path.join(app.root_path, "basic.ics"), "r") as file:
            file_data = file.read()

        return calendar_data.upcoming_events(calendar_data.read_calendar(file_data), 365, 3)

    return app