import unittest
import os
from unittest.mock import patch, MagicMock
from database.chroma_manager import ChromaManager
from scraping.scraper import BookScraper

class TestScraper(unittest.TestCase):
    @patch('scraping.scraper.sync_playwright')
    def test_scrape_chapter(self, mock_playwright):
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.inner_text.return_value = "Sample content"
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        
        scraper = BookScraper("http://example.com")
        result = scraper.scrape_chapter()
        self.assertIn('content', result)

class TestChromaDB(unittest.TestCase):
    def setUp(self):
        # Clear any existing test data
        if os.path.exists(".chromadb"):
            import shutil
            shutil.rmtree(".chromadb")
            
    def test_save_and_retrieve(self):
        db = ChromaManager()
        test_id = "test123"
        test_content = "test content"
        
        # Save and verify
        db.save_version(test_content, {"test": True}, test_id)
        result = db.get_version(test_id)
        
        # Check the structure and content
        self.assertIn('documents', result)
        self.assertIn('metadatas', result)
        self.assertEqual(len(result['documents']), 1)
        self.assertEqual(result['documents'][0], test_content)
        self.assertEqual(result['metadatas'][0]['test'], True)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(".chromadb"):
            import shutil
            shutil.rmtree(".chromadb")

if __name__ == '__main__':
    unittest.main()
