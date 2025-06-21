import google.generativeai as genai
from utils.config import GEMINI_API_KEY

class AIWriter:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def spin_chapter(self, original_text):
        # Implementation will go here
        pass
# agents/writer.py
import google.generativeai as genai
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class AIWriter:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        
    def spin_chapter(self, original_text):
        prompt = f"""
        Rewrite this chapter in a fresh style while preserving the original meaning and key elements.
        Add creative flourishes but maintain the core narrative. Here's the original:
        
        {original_text}
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    
    
    # Update AIWriter class with new methods
def incorporate_feedback(self, text, feedback):
    prompt = f"""
    Rewrite the following text incorporating the provided feedback.
    Keep the core meaning but improve as directed.
    
    Original Text:
    {text}
    
    Feedback:
    {feedback}
    
    Rewritten Text:
    """
    response = self.model.generate_content(prompt)
    return response.text

def batch_spin(self, chapters, style_guidelines=""):
    results = []
    for chapter in chapters:
        prompt = f"""
        Rewrite this chapter according to style guidelines:
        {style_guidelines}
        
        Original Chapter:
        {chapter}
        """
        results.append(self.model.generate_content(prompt).text)
    return results