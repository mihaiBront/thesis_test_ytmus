from unittest import TestCase

import trafilatura
from newspaper import Article
from bs4 import BeautifulSoup
import requests


class TestTrafilatura(TestCase):
    def test_trafilatura(self):
        url = "https://en.wikipedia.org/wiki/Monster"
        html = trafilatura.fetch_url(url)
        text = trafilatura.extract(html)
        print(text)
        
class TestNewspaper(TestCase):
    def test_newspaper(self):
        article = Article('https://www.youtube.com')
        article.download()
        article.parse()
        print(article.text)
        
class TestBeautifulSoup(TestCase):
    def test_beautifulsoup(self):
        url = "https://www.youtube.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate', 
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        print(soup.get_text())
        
        
        
        