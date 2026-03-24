import requests

# Anki module for flashcard-cli
ANKI_URL = "http://localhost:8765"


# Create a new Anki deck with the given name
def create_deck(deck_name):
    payload = {"action": "createDeck", "version": 6, "params": {"deck": deck_name}}
    try:
        response = requests.post(ANKI_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Anki. Make sure Anki is open with AnkiConnect installed.")
        exit(1)
    return response.json()


# Add flashcards to the specified Anki deck
def add_cards(flashcards, deck_name):
    notes = []
    for flashcard in flashcards:
        note = {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": flashcard["question"],
                "Back": flashcard["answer"]
            },
        }
        notes.append(note)
    payload = {"action": "addNotes", "version": 6, "params": {"notes": notes}}
    try:
        response = requests.post(ANKI_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Anki. Make sure Anki is open with AnkiConnect installed.")
        exit(1)
    return response.json()
