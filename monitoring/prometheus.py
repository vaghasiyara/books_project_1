from prometheus_fastapi_instrumentator import Instrumentator

def setup_prometheus(app):
    """Configure Prometheus metrics for FastAPI"""
    Instrumentator().instrument(app).expose(app)
