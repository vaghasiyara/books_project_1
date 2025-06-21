from typing import Dict, Tuple
from bs4 import BeautifulSoup
import re

class ContentValidator:
    @staticmethod
    def validate_html(html: str) -> Tuple[bool, Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        results = {
            'images': len(soup.find_all('img')),
            'links': len(soup.find_all('a')),
            'sections': len(soup.find_all(['h1', 'h2', 'h3']))
        }
        return True, results

    @staticmethod
    def validate_text(text: str) -> Tuple[bool, Dict]:
        stats = {
            'length': len(text),
            'paragraphs': len(re.split(r'\n\s*\n', text)),
            'avg_sentence_length': sum(len(s.split()) for s in re.split(r'[.!?]', text)) / 
                                 max(1, len(re.split(r'[.!?]', text)))
        }
        return True, stats
