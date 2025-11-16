import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
if GOOGLE_API_KEY and GOOGLE_API_KEY != "YOUR_API_KEY_GOES_HERE":
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found. API call will be skipped.")
    GOOGLE_API_KEY = None

WORDS_DICT = {
    "negative": {
        "academic": [
            "difficult", "hard", "problem", "tough", "struggle", "pressure",
            "difficulty", "distractions", "struggled", "slack"
        ],
        "actions": [
            "risk", "fired", "dont", "broke", "outed", "miss", "removed",
            "hurt", "kicked", "deleted"
        ],
        "items": ["mice", "bomb", "tilted", "fungus", "rats", "rodent"],
        "other": [
            "bad", "less", "issues", "harder", "down", "lost", "stress",
            "worst", "terrible", "missing"
        ],
        "people": [
            "nobody", "aiders", "panhandlers", "commies", "inconsiderate",
            "offenders", "obody"
        ],
        "places": [
            "overcrowding", "crowded", "dump", "cramped", "prison", "cell"
        ],
        "resources": ["tuition", "housing", "debt", "loan", "loans"],
        "social": [
            "alone", "dry", "bored", "pissed", "upsetting", "downvoted",
            "embarrassing", "drunken", "aggressive", "rude"
        ]
    },
    "neutral": {
        "academic": [
            "semester", "class", "program", "college", "classes", "course",
            "research", "questions", "project", "rch"
        ],
        "actions": [
            "have", "going", "want", "say", "change", "took", "make",
            "work", "made", "used"
        ],
        "items": [
            "hat", "tickets", "money", "food", "software", "bike", "bed",
            "data", "mail", "packages"
        ],
        "other": [
            "more", "from", "out", "how", "also", "should", "what", "now",
            "first", "way"
        ],
        "people": [
            "students", "people", "team", "student", "band", "roy",
            "professor", "someone", "coach", "him"
        ],
        "places": [
            "nion", "school", "rpi", "room", "campus", "larkson", "home",
            "house", "place", "office"
        ],
        "resources": [
            "system", "email", "services", "parking", "credit", "info",
            "advice", "government", "anner", "wikipedia"
        ],
        "social": [
            "game", "hockey", "games", "hey", "group", "lunch", "lol",
            "rivalry", "football", "sports"
        ]
    },
    "positive": {
        "academic": [
            "goal", "high", "learning", "understanding", "lead",
            "understand", "learn", "easy", "championship", "accepted"
        ],
        "actions": [
            "recommend", "help", "working", "fix", "fixed", "win",
            "improve", "fixing", "support", "scored"
        ],
        "items": [
            "mores", "chilli", "burgers", "list", "distractions", "medications",
            "meds", "sentences", "comment", "adderall", "zoloft"
        ],
        "other": [
            "good", "right", "free", "experience", "better", "great",
            "easier", "able", "interested", "love"
        ],
        "people": [
            "friends", "tutors", "friend", "master", "tutors", "bff",
            "star", "tars", "stars", "mentor"
        ],
        "places": [
            "rpi", "college", "hospital", "office", "school", "world",
            "building", "site", "center", "mailroom"
        ],
        "resources": [
            "aid", "tutoring", "power", "scholarship", "successcenter",
            "opportunities", "counseling", "recommendations", "tips",
            "resource"
        ],
        "social": [
            "pep", "hanks", "community", "fun", "hangout", "confidential",
            "spirit", "willing", "together", "bonfire"
        ]
    }
}

commands_mapping = {
    1: '.', 2: '-', 3: '.-', 4: '-.', 5: '..', 6: '--',
    7: '.--', 8: '..-', 9: '...', 10: '---'
}

commands = {
    '.': '1', '-': '2', '.-': '3', '-.': '4', '..': '5', '--': '6',
    '.--': '7', '..-': '8', '...': '9', '---': '10'
}


def interpret_morse_output(concepts_list):
    """
    Uses Gemini to turn a list of user-selected concept words into a
    natural, human-readable sentence.
    """
    if not GOOGLE_API_KEY:
        return "API Key not configured. Please check .env file."
    if not concepts_list:
        return "No concepts selected to interpret."

    prompt = f"""
    You are a supportive communication assistant.
    The user has provided a list of abstract concepts:
    {json.dumps(concepts_list)}

    These words may feel like fragments of a thought or emotion.
    Your task is to infer the intended meaning and express it as a
    single, natural, human-friendly sentence.

    Rules:
    - Preserve the user's emotional tone.
    - Add connecting words if needed.
    - Do NOT mention that this came from concept words.
    - Output ONLY the finished sentence, nothing else.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        final_sentence = response.text.strip().strip('"')
        return final_sentence

    except Exception as e:
        print(f"Error calling Gemini API in interpret_morse_output: {e}")
        return "Error: Could not connect to Gemini."

def get_gemini_hint(word):
    """
    Ask Gemini AI for 3 progressively easier hints for a word.
    Returns a list of strings.
    """
    if not GOOGLE_API_KEY:
        return ["API Key not configured.", "Please check .env file.", "The word is: " + word]
        
    prompt = f"""
    Generate exactly 3 hints for the word "{word}".
    The hints should get progressively easier.
    Do not use the word "{word}" in your response.
    Format the response as a simple JSON list of 3 strings.
    
    Example:
    Input: "python"
    Output:
    [
        "It's a type of large, non-venomous snake.",
        "It's also a very popular programming language.",
        "This language is named after a British comedy troupe."
    ]
    """
    
    try:
        json_schema = {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
        config = genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=json_schema
        )
        model = genai.GenerativeModel("gemini-2.5-flash", generation_config=config)
        
        response = model.generate_content(prompt)
        
        hints = json.loads(response.text)
        
        if isinstance(hints, list) and len(hints) >= 3:
            return hints[:3]
        else:
            raise Exception("AI did not return a list of 3 strings.")

    except Exception as e:
        print(f"Error calling Gemini API in get_gemini_hint: {e}")
        return [
            f"The word starts with '{word[0]}'.",
            f"The word has {len(word)} letters.",
            f"The word is: {word}"
        ]