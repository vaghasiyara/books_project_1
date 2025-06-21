import time
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary
from prometheus_client.core import REGISTRY
from typing import Callable, Any
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Core Metrics
REQUESTS = Counter('workflow_requests_total', 'Total requests', ['endpoint', 'method'])
PROCESSING_TIME = Histogram('workflow_processing_seconds', 'Time spent processing', ['endpoint'])
ERRORS = Counter('workflow_errors_total', 'Total errors', ['endpoint', 'error_type'])
TASKS = Counter('workflow_tasks_total', 'Total tasks processed', ['task_type'])
TASK_TIME = Summary('workflow_task_processing_seconds', 'Time spent processing tasks', ['task_type'])
ACTIVE_TASKS = Gauge('workflow_active_tasks', 'Currently active tasks')
QUEUE_SIZE = Gauge('workflow_task_queue_size', 'Current task queue size')

# Database Metrics
DB_OPS = Counter('workflow_db_operations_total', 'Database operations', ['operation'])
DB_LATENCY = Histogram('workflow_db_latency_seconds', 'Database operation latency', ['operation'])

class WorkflowMetrics:
    def __init__(self, port=8000):
        self.port = port
        
    def start_exporter(self):
        """Start the Prometheus metrics server"""
        start_http_server(self.port)
        logger.info(f"Metrics server started on port {self.port}")
        
    def track_errors(self, endpoint: str):
        """Decorator to track errors for specific endpoints"""
        def decorator(f: Callable):
            @wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    ERRORS.labels(endpoint=endpoint, error_type=type(e).__name__).inc()
                    logger.error(f"Error in {endpoint}: {str(e)}")
                    raise
            return wrapper
        return decorator
        
    def monitor_task(self, task_type: str):
        """Decorator to monitor task execution"""
        def decorator(f: Callable):
            @wraps(f)
            def wrapper(*args, **kwargs):
                TASKS.labels(task_type=task_type).inc()
                ACTIVE_TASKS.inc()
                start_time = time.time()
                
                try:
                    result = f(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    TASK_TIME.labels(task_type=task_type).observe(duration)
                    ACTIVE_TASKS.dec()
            return wrapper
        return decorator
        
    def monitor_db_operation(self, operation: str):
        """Decorator to monitor database operations"""
        def decorator(f: Callable):
            @wraps(f)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = f(*args, **kwargs)
                    DB_OPS.labels(operation=operation).inc()
                    return result
                finally:
                    DB_LATENCY.labels(operation=operation).observe(time.time() - start_time)
            return wrapper
        return decorator

# Initialize default metrics
metrics = WorkflowMetrics()

def monitor_requests(f: Callable) -> Callable:
    """Decorator to monitor request processing"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        REQUESTS.labels(
            endpoint=f.__name__,
            method=getattr(args[0], 'request', None).method if args else 'unknown'
        ).inc()
        
        start_time = time.time()
        PROCESSING_TIME.labels(endpoint=f.__name__).observe(time.time() - start_time)
        return f(*args, **kwargs)
    return wrapper

def update_queue_size(size: int):
    """Update the task queue size metric"""
    QUEUE_SIZE.set(size)

if __name__ == '__main__':
    # Example usage
    metrics.start_exporter()
    
    @metrics.track_errors("example_endpoint")
    @monitor_requests
    def example_function():
        time.sleep(1)
        return "Success"
        
    @metrics.monitor_task("sample_task")
    def sample_task():
        time.sleep(0.5)
        
    # Keep the server running
    while True:
        example_function()
        sample_task()
        time.sleep(5)
