# Scraper module for flashcard-cli
import requests
from bs4 import BeautifulSoup

# Scrape the content of the given URL and return the BeautifulSoup object
def scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0  (compatible; flashcard-cli/1.0)"
    }

    # Make the HTTP GET request to the URL with a timeout of 30 seconds
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup 
    soup = BeautifulSoup(response.text, 'html.parser')

    #remove noise
    for tag in soup.find_all(['nav', 'footer', 'aside', 'header', 'script', 'style']):
        tag.decompose()

    main_content = soup.find('main') or soup.find('article') or soup.find('div', {"id": "main-column"}) or soup.body

    lines = [line.strip() for line in main_content.get_text(separator='\n').splitlines() if  line.strip()]
    return '\n'.join(lines)