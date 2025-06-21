# main.py
from scraping.scraper import BookScraper
from agents.writer import AIWriter
from agents.reviewer import AIReviewer
from agents.editor import HumanEditor
from database.chroma_manager import ChromaManager
import time

def main():
    # Initialize components
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    scraper = BookScraper(url)
    writer = AIWriter()
    reviewer = AIReviewer()
    editor = HumanEditor()
    db = ChromaManager()
    
    # Step 1: Scrape original content
    print("Scraping original chapter...")
    scraped_data = scraper.scrape_chapter()
    original_text = scraped_data['content']
    
    # Step 2: AI spin
    print("\nAI writing spinning chapter...")
    spun_text = writer.spin_chapter(original_text)
    
    # Step 3: AI review
    print("\nAI reviewing spun chapter...")
    ai_review = reviewer.review_chapter(spun_text, original_text)
    
    # Human-in-the-loop iterations
    approved = False
    iterations = 0
    current_version = spun_text
    
    while not approved and iterations < 5:  # Max 5 iterations
        iterations += 1
        print(f"\n=== Iteration {iterations} ===")
        
        # Get human feedback
        feedback = editor.get_feedback(current_version, ai_review)
        
        # Incorporate feedback
        revised_text = writer.incorporate_feedback(current_version, feedback)
        ai_review = reviewer.review_chapter(revised_text, original_text)
        
        current_version = revised_text
        
        # Check for final approval
        approved = editor.final_approval(current_version)
    
    if approved:
        # Save final version
        metadata = {
            "source_url": url,
            "screenshot_path": scraped_data['screenshot_path'],
            "iterations": iterations,
            "timestamp": time.time()
        }
        db.save_version(current_version, metadata, "final")
        print("\nChapter finalized and saved to database!")
    else:
        print("\nMaximum iterations reached without approval.")

if __name__ == "__main__":
    main()