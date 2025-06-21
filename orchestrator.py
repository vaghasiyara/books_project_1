import threading
from monitoring import metrics, update_queue_size
from queue import Queue
import time
from datetime import datetime
from utils.helpers import setup_logging

class PublicationOrchestrator:
    def __init__(self):
        self.task_queue = Queue()
        update_queue_size(0)
        self.results = {}
        self.threads = []
        self.task_history = []
        setup_logging()
        
    def add_task(self, task_type, payload):
        """Add a new task to the processing queue"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.results)+1}"
        task = {
            'id': task_id,
            'type': task_type,
            'payload': payload,
            'status': 'queued',
            'created_at': datetime.now().isoformat()
        }
        self.task_queue.put((task_id, task_type, payload))
        update_queue_size(self.task_queue.qsize())
        self.task_history.append(task)
        return task_id
        
    def worker(self):
        """Worker thread that processes tasks from the queue"""
        while True:
            task_id, task_type, payload = self.task_queue.get()
            try:
                # Update task status
                task = next(t for t in self.task_history if t['id'] == task_id)
                task['status'] = 'processing'
                task['started_at'] = datetime.now().isoformat()
                
                # Process different task types
                if task_type == "scrape":
                    from scraping.scraper import BookScraper
                    scraper = BookScraper(payload['url'])
                    result = scraper.scrape_chapter()
                    
                elif task_type == "spin":
                    from agents.writer import AIWriter
                    writer = AIWriter()
                    result = writer.spin_chapter(payload['content'])
                    
                elif task_type == "review":
                    from agents.reviewer import AIReviewer
                    reviewer = AIReviewer()
                    result = reviewer.review_chapter(payload['content'])
                    
                # Store result and update status
                self.results[task_id] = result
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                task['duration'] = (datetime.fromisoformat(task['completed_at']) - 
                                  datetime.fromisoformat(task['started_at'])).total_seconds()
                
            except Exception as e:
                task['status'] = 'failed'
                task['error'] = str(e)
                self.results[task_id] = {'error': str(e)}
            finally:
                self.task_queue.task_done()
        update_queue_size(self.task_queue.qsize())
                
    def start_workers(self, num_workers=3):
        """Start worker threads to process tasks"""
        for i in range(num_workers):
            t = threading.Thread(
                target=self.worker,
                daemon=True,
                name=f"Worker-{i+1}"
            )
            t.start()
            self.threads.append(t)
            
    def get_result(self, task_id):
        """Retrieve result for a completed task"""
        return self.results.get(task_id)
        
    def get_task_status(self, task_id):
        """Get current status of a task"""
        for task in self.task_history:
            if task['id'] == task_id:
                return task
        return None
        
    def wait_for_completion(self, timeout=None):
        """Wait for all queued tasks to complete"""
        self.task_queue.join()
        
    def shutdown(self):
        """Clean shutdown of all workers"""
        for t in self.threads:
            t.join(timeout=1)

if __name__ == '__main__':
    # Example usage
    orchestrator = PublicationOrchestrator()
    orchestrator.start_workers()
    
    # Add sample tasks
    scrape_id = orchestrator.add_task("scrape", {
        "url": "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    })
    
    spin_id = orchestrator.add_task("spin", {
        "content": "Sample chapter text to be spun"
    })
    
    # Wait for tasks to complete
    orchestrator.wait_for_completion()
    
    # Get results
    print("Scrape result:", orchestrator.get_result(scrape_id))
    print("Spin result:", orchestrator.get_result(spin_id))
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncPublicationOrchestrator:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()
        
    async def process_task(self, task_type, payload):
        if task_type == "scrape":
            from scraping.scraper import BookScraper
            scraper = BookScraper(payload['url'])
            return await self.loop.run_in_executor(self.executor, scraper.scrape_chapter)
        elif task_type == "spin":
            from agents.writer import AIWriter
            writer = AIWriter()
            return await self.loop.run_in_executor(
                self.executor, 
                writer.spin_chapter, 
                payload['content']
            )

    async def batch_process(self, tasks):
        return await asyncio.gather(*[
            self.process_task(task['type'], task['payload'])
            for task in tasks
        ])
