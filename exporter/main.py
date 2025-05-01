from prometheus_client import generate_latest, CollectorRegistry
from flask import Response, Flask
from exporter.collector import Collector
from exporter.constants import Config

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    collector = Collector(registry, Config.TRACKER_ADDRESS)
    collector.collect()

    return Response(generate_latest(registry), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9036)