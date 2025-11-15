import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = 'words_dict.json'
OUTPUT_FILE = 'rpi_message_system_v3.json'
BATCH_SIZE = 100
CATEGORIES = [
    'academic', 'social', 'people', 'places',
    'items', 'resources', 'actions', 'other'
]


SCHEMA = {
  "type": "OBJECT",
  "properties": {
    "positive": {
      "type": "OBJECT",
      "description": "Words with a positive sentiment.",
      "properties": {
        "academic": { "type": "ARRAY", "items": { "type": "STRING" } },
        "social": { "type": "ARRAY", "items": { "type": "STRING" } },
        "people": { "type": "ARRAY", "items": { "type": "STRING" } },
        "places": { "type": "ARRAY", "items": { "type": "STRING" } },
        "items": { "type": "ARRAY", "items": { "type": "STRING" } },
        "resources": { "type": "ARRAY", "items": { "type": "STRING" } },
        "actions": { "type": "ARRAY", "items": { "type": "STRING" } },
        "other": { "type": "ARRAY", "items": { "type": "STRING" } }
      }
    },
    "negative": {
      "type": "OBJECT",
      "description": "Words with a negative sentiment.",
      "properties": {
        "academic": { "type": "ARRAY", "items": { "type": "STRING" } },
        "social": { "type": "ARRAY", "items": { "type": "STRING" } },
        "people": { "type": "ARRAY", "items": { "type": "STRING" } },
        "places": { "type": "ARRAY", "items": { "type": "STRING" } },
        "items": { "type": "ARRAY", "items": { "type": "STRING" } },
        "resources": { "type": "ARRAY", "items": { "type": "STRING" } },
        "actions": { "type": "ARRAY", "items": { "type": "STRING" } },
        "other": { "type": "ARRAY", "items": { "type": "STRING" } }
      }
    },
    "neutral": {
      "type": "OBJECT",
      "description": "Words with a neutral sentiment.",
      "properties": {
        "academic": { "type": "ARRAY", "items": { "type": "STRING" } },
        "social": { "type": "ARRAY", "items": { "type": "STRING" } },
        "people": { "type": "ARRAY", "items": { "type": "STRING" } },
        "places": { "type": "ARRAY", "items": { "type": "STRING" } },
        "items": { "type": "ARRAY", "items": { "type": "STRING" } },
        "resources": { "type": "ARRAY", "items": { "type": "STRING" } },
        "actions": { "type": "ARRAY", "items": { "type": "STRING" } },
        "other": { "type": "ARRAY", "items": { "type": "STRING" } }
      }
    }
  }
}

# --- FIX 1: Pass the API key to configure() ---
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_API_KEY_GOES_HERE":
    print("Error: GEMINI_API_KEY not found or not set in .env file.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY) # <-- Pass the key here

generation_config = genai.GenerationConfig(
    response_mime_type='application/json',
    response_schema=SCHEMA
)

system_prompt = f"""
You are an expert data analyst. Your task is to categorize a list of 
words from the RPI (Rensselaer Polytechnic Institute) subreddit.

First, determine the sentiment of the word (positive, negative, or neutral).
Second, determine its conceptual category: {json.dumps(CATEGORIES)}
each category within each sentiment can have a maximum of 10 values!!!!!
Return a single JSON object that matches the requested schema,
sorting each word into its correct sentiment and conceptual category.
"""

print("Initializing Gemini model...")
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config=generation_config,
    system_instruction=system_prompt
)


def load_words(filename):
    """Loads the words from the JSON file created by your counter script."""
    print(f"Loading words from {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            word_counts = json.load(f)
            return list(word_counts.keys())
    except FileNotFoundError:
        print(f"Error: Input file not found: {filename}")
        print("Please run your word_counter.py script first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file.")
        return None

def get_gemini_categorization(word_batch):
    """
    Calls the Gemini API (using the Python SDK) to categorize a batch of words.
    """
    # --- FIX 2: Corrected prompt ---
    user_prompt = f"""
    Here is a list of words to categorize:
    {json.dumps(word_batch)}
    
    Return your answer *only* as a JSON object matching the schema.
    """
    
    max_retries = 5
    delay = 1
    for i in range(max_retries):
        try:
            response = model.generate_content(user_prompt)
            return json.loads(response.text) 
        except Exception as e:
            print(f"  > API Error: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2
            
    print(f"  > API call failed after {max_retries} retries.")
    return None

# --- FIX 3: Added the deep_merge function ---
def deep_merge(dict1, dict2):
    """
    Merges the lists from dict2 into dict1 for our specific
    nested structure: {sentiment: {category: [words]}}
    """
    for sentiment, categories in dict2.items():
        if sentiment in dict1:
            for category, words in categories.items():
                if category in dict1[sentiment]:
                    dict1[sentiment][category].extend(words)
                else:
                    # Handle if AI returns a category not in our list
                    print(f"Warning: AI returned unexpected category '{category}'")
                    dict1[sentiment][category] = words
        else:
            # Handle if AI returns a sentiment not in our list
            print(f"Warning: AI returned unexpected sentiment '{sentiment}'")
            dict1[sentiment] = categories
    return dict1

def main():
    words = load_words(INPUT_FILE)
    if not words:
        return

    # --- FIX 4: Initialize the full, nested dictionary ---
    final_categories = {
        "positive": {cat: [] for cat in CATEGORIES},
        "negative": {cat: [] for cat in CATEGORIES},
        "neutral":  {cat: [] for cat in CATEGORIES}
    }
    
    for i in range(0, len(words), BATCH_SIZE):
        batch = words[i:i + BATCH_SIZE]
        print(f"\n--- Processing batch {i//BATCH_SIZE + 1} / {len(words)//BATCH_SIZE + 1} ---")
        
        # This will be a nested dictionary, e.g., {"positive": {"academic": [...]}}
        batch_result = get_gemini_categorization(batch) 
        
        # --- FIX 5: Use deep_merge, not the flat-list logic ---
        if batch_result:
            final_categories = deep_merge(final_categories, batch_result)
            print(f"  > Batch processed and merged successfully. Sleeping for 1 second...")
        else:
            print(f"  > Failed to process batch. Skipping.")
        
        time.sleep(1)

    print(f"\nAll batches processed. Saving to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_categories, f, indent=4, sort_keys=True)
        print("Done. Your RPI Message System V3 (Sentiment + Category) is ready!")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()