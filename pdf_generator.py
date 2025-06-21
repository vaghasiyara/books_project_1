from fpdf import FPDF
from typing import List

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
    def generate(self, content: List[str], filename: str):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        
        for paragraph in content:
            self.pdf.multi_cell(0, 10, paragraph)
            
        self.pdf.output(filename)
