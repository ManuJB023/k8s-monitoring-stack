from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# --- Metrics ---
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'HTTP request latency',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]
)

ACTIVE_USERS = Gauge(
    'app_active_users',
    'Simulated number of active users'
)

JOBS_PROCESSED = Counter(
    'app_jobs_processed_total',
    'Total background jobs processed',
    ['status']
)

@app.route('/')
def index():
    start = time.time()
    # Simulate variable latency (like a wellsite sensor query)
    time.sleep(random.uniform(0.01, 0.3))
    ACTIVE_USERS.set(random.randint(1, 50))
    JOBS_PROCESSED.labels(status='success').inc()
    duration = time.time() - start
    REQUEST_LATENCY.labels(endpoint='/').observe(duration)
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    return 'OK', 200

@app.route('/error')
def error():
    REQUEST_COUNT.labels(method='GET', endpoint='/error', status='500').inc()
    JOBS_PROCESSED.labels(status='failed').inc()
    return 'Internal Server Error', 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
