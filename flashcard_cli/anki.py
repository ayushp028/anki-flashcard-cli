import requests
# Anki module for flashcard-cli
ANKI_URL = "http://localhost:8765"

# Create a new Anki deck with the given name
def create_deck(deck_name):
    payload = {"action": "createDeck", "version": 6, "params": {"deck": deck_name}}
    response = requests.post(ANKI_URL, json=payload)
    response.raise_for_status()
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
    response = requests.post(ANKI_URL, json=payload)
    response.raise_for_status()
    return response.json()

