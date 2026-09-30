from flask import Flask, render_template

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

    return app