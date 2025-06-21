from celery_app import generate_pdf_task
from fastapi import BackgroundTasks
import uuid

class TaskRunner:
    async def run_pdf_generation(self, content: list):
        task_id = str(uuid.uuid4())
        generate_pdf_task.apply_async(
            args=[content, f"output_{task_id}.pdf"],
            task_id=task_id
        )
        return task_id
