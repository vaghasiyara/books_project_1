# agents/reviewer.py
import google.generativeai as genai
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class AIReviewer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        
    def review_chapter(self, spun_text, original_text=None):
        prompt = f"""
        Review this rewritten chapter for:
        1. Consistency with original meaning
        2. Flow and readability
        3. Creative enhancements
        4. Grammar and style
        
        Provide detailed feedback and suggest improvements. Here's the text:
        
        {spun_text}
        """
        
        if original_text:
            prompt += f"\n\nOriginal text for reference:\n{original_text}"
            
        response = self.model.generate_content(prompt)
        return response.text