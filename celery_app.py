from celery import Celery
from pdf_generator import PDFGenerator

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@celery.task
def generate_pdf_task(content, filename):
    pdf_gen = PDFGenerator()
    pdf_gen.generate(content, filename)
    return filename
