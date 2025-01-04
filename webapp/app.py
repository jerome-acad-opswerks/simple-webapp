from flask import Flask
from flask import render_template
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)

@app.route("/")
def main():
    return render_template("index.html")
