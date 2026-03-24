import os
from google import genai


def generate(content, deck_name, count=20):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""You are an expert at creating Anki flashcards for studying technical content.

Based on the following content about "{deck_name}", create exactly {count} high-quality Anki flashcards.

Requirements:
- Each card should test a specific, important concept
- Questions should be clear and unambiguous
- Answers should be concise but complete
- Output format: one card per line as: Question\tAnswer
- Output ONLY the {count} tab-separated pairs, no numbering or extra text

Content:
{content}

Generate exactly {count} flashcards now:"""

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    flashcards = []
    for line in response.text.strip().splitlines():
        line = line.strip()
        if "\t" in line:
            parts = line.split("\t", 1)
            if len(parts) == 2 and parts[0] and parts[1]:
                flashcards.append({
                    "question": parts[0].strip(),
                    "answer": parts[1].strip()
                })

    return flashcards
