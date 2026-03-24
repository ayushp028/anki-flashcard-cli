# anki-flashcard-cli

A CLI tool that automatically generates Anki flashcards from any URL using Google Gemini AI. Point it at a documentation page, article, or tutorial — and it creates a ready-to-study Anki deck in seconds.

## Features

- Scrapes and cleans web content from any URL
- Uses Google Gemini to generate high-quality question/answer flashcards
- Automatically creates decks and adds cards via AnkiConnect
- Configurable card count per run
- Graceful error handling for missing API keys, unreachable URLs, and Anki not running

## Requirements

- Python 3.8+
- [Anki](https://apps.ankiweb.net/) with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

## Installation

```bash
git clone https://github.com/ayushp028/anki-flashcard-cli.git
cd anki-flashcard-cli
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Make sure Anki is open with AnkiConnect running, then:

```bash
python -m flashcard_cli.main <url> <deck_name> [--count N]
```

### Examples

```bash
# Generate 20 flashcards (default) from a Python docs page
python -m flashcard_cli.main https://docs.python.org/3/tutorial/classes.html "Python Classes"

# Generate 30 flashcards into a custom deck
python -m flashcard_cli.main https://docs.python.org/3/tutorial/classes.html "Python Classes" --count 30
```

## How It Works

1. **Scrape** — Fetches the page and strips noise (nav, footer, scripts) to extract clean content
2. **Generate** — Sends the content to Gemini with a prompt to produce `N` question/answer pairs
3. **Import** — Creates the Anki deck (if it doesn't exist) and adds all cards via the AnkiConnect API

## Project Structure

```
flashcard_cli/
├── main.py        # CLI entry point and argument parsing
├── scraper.py     # Web scraping and content extraction
├── generator.py   # Gemini API integration and flashcard generation
└── anki.py        # AnkiConnect API client
```

## Error Handling

The CLI handles common failure cases with clear messages:

| Scenario | Error Message |
|---|---|
| Missing `GEMINI_API_KEY` | Prompts user to set up `.env` before doing anything |
| Unreachable URL | Reports connection error and exits cleanly |
| HTTP error (4xx/5xx) | Prints the HTTP status error and exits |
| Request timeout | Reports timeout and exits cleanly |
| Anki not open | Tells user to open Anki with AnkiConnect installed |

Implemented using Python's built-in [`try/except`](https://docs.python.org/3/tutorial/errors.html) and [requests exception hierarchy](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions). Environment variable validation is done with [`os.getenv`](https://docs.python.org/3/library/os.html#os.getenv).

The `GEMINI_API_KEY` is validated in `main.py` before any other code runs. The Gemini client is configured inside the `generate` function rather than at module import time, so the API key is only accessed after it has been confirmed to exist. See [Python module import system](https://docs.python.org/3/reference/import.html) for more on module-level vs function-level execution.

## Tech Stack

| Library | Docs | Usage |
|---|---|---|
| google-generativeai | [Gemini API Python SDK](https://ai.google.dev/gemini-api/docs/quickstart?lang=python) | Flashcard generation via Gemini |
| BeautifulSoup4 | [BS4 Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | HTML parsing and content extraction |
| requests | [Requests Docs](https://docs.python-requests.org/en/latest/) | HTTP client for scraping and AnkiConnect |
| python-dotenv | [python-dotenv Docs](https://saurabh-kumar.com/python-dotenv/) | Loading API keys from `.env` |
| AnkiConnect | [AnkiConnect API Reference](https://foosoft.net/projects/anki-connect/) | Adding cards and decks to Anki |
| argparse | [argparse Docs](https://docs.python.org/3/library/argparse.html) | CLI argument parsing |
