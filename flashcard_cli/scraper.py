import requests
from bs4 import BeautifulSoup

# Scraper module for flashcard-cli


def scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; flashcard-cli/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}. Check the URL and your internet connection.")
        exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        exit(1)
    except requests.exceptions.Timeout:
        print(f"Error: Request to {url} timed out.")
        exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove noise
    for tag in soup.find_all(['nav', 'footer', 'aside', 'header', 'script', 'style']):
        tag.decompose()

    main_content = soup.find('main') or soup.find('article') or soup.find('div', {"id": "main-column"}) or soup.body

    lines = [line.strip() for line in main_content.get_text(separator='\n').splitlines() if line.strip()]
    return '\n'.join(lines)
