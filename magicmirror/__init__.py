import os.path

from flask import Flask, render_template, jsonify

from . import weather_data, calendar_data, config


def create_app():
    app = Flask(__name__)

    config.init(app.root_path)

    @app.route("/")
    def root():
        return render_template("index.html")

    @app.route("/api/weather_data", methods=["GET"])
    def api_weather_data():
        return weather_data.get_weather_data(logger=app.logger)

    @app.route("/api/week_days", methods=["GET"])
    def api_week_days():
        return calendar_data.get_week_data()

    @app.route("/api/week_events", methods=["GET"])
    def api_week_events():
        calendar = calendar_data.read_calendar()
        events = calendar.events

        return calendar_data.events_around_date(events, 3, 3)

    @app.route("/api/upcoming_events", methods=["GET"])
    def api_upcoming_events():
        calendar = calendar_data.read_calendar()
        events = calendar.events

        return calendar_data.upcoming_events(events, 365, 3)

    @app.route("/api/config", methods=["GET"])
    def api_config():
        return jsonify(config.config.__dict__)

    return app
