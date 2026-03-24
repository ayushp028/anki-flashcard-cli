import argparse
import os
from dotenv import load_dotenv

from flashcard_cli import scraper, generator, anki

def main():
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not set. Copy .env.example to .env and add your API key.")
        exit(1)

    parser = argparse.ArgumentParser(description="Generate Anki flashcards from a URL")
    parser.add_argument("url", help="URL to generate flashcards from")
    parser.add_argument("deck", help="Anki deck name")
    parser.add_argument("--count", type=int, default=20, help="Number of flashcards to generate (default: 20)")
    args = parser.parse_args()

    print(f"Scraping {args.url}...")
    content = scraper.scrape(args.url)

    print(f"Generating {args.count} flashcards...")
    flashcards = generator.generate(content, args.deck, args.count)

    print(f"Adding {len(flashcards)} cards to deck '{args.deck}'...")
    anki.create_deck(args.deck)
    anki.add_cards(flashcards, args.deck)

    print(f"Done! {len(flashcards)} flashcards added to '{args.deck}'.")

if __name__ == "__main__":
    main()
