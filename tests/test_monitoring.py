import unittest
from unittest.mock import patch
from monitoring import WorkflowMetrics, TASKS

class TestMonitoring(unittest.TestCase):
    def setUp(self):
        self.metrics = WorkflowMetrics(port=8001)
        
    @patch('monitoring.start_http_server')
    def test_start_exporter(self, mock_start):
        self.metrics.start_exporter()
        mock_start.assert_called_once_with(8001)
        
    def test_track_errors(self):
        @self.metrics.track_errors("test_endpoint")
        def failing_function():
            raise ValueError("Test error")
            
        with self.assertRaises(ValueError):
            failing_function()
            
    def test_monitor_task(self):
        @self.metrics.monitor_task("test_task")
        def sample_task():
            return "done"
            
        result = sample_task()
        self.assertEqual(result, "done")
        # Check the task counter was incremented
        self.assertGreater(TASKS.labels("test_task")._value.get(), 0)

if __name__ == '__main__':
    unittest.main()
