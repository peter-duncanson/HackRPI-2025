emotions_lexicon = {
    "Happiness": [
        "Joy", "Elation", "Contentment", "Cheerfulness", "Delight",
        "Amusement", "Bliss", "Euphoria", "Exhilaration", "Glee",
        "Mirth", "Pleasure", "Satisfaction", "Serenity", "Triumph",
        "Optimism", "Zest", "Jubilation", "Ecstasy", "Gaiety"
    ],
    "Sadness": [
        "Grief", "Sorrow", "Dejection", "Despair", "Melancholy",
        "Misery", "Woe", "Heartbreak", "Disappointment", "Dismay",
        "Gloomy", "Lonesome", "Mournful", "Regret", "Remorse",
        "Pity", "Depression", "Resignation", "Somberness", "Wistfulness"
    ],
    "Anger": [
        "Rage", "Fury", "Wrath", "Irritation", "Annoyance",
        "Frustration", "Indignation", "Resentment", "Outrage", "Exasperation",
        "Hostility", "Bitterness", "Vexation", "Aggravation", "Spleen",
        "Ire", "Belligerence", "Displeasure", "Enraged", "Seething"
    ],
    "Fear": [
        "Terror", "Fright", "Anxiety", "Apprehension", "Dread",
        "Panic", "Alarm", "Horror", "Nervousness", "Trepidation",
        "Worry", "Intimidation", "Vulnerability", "Unease", "Phobia",
        "Suspense", "Cowardice", "Hesitation", "Foreboding", "Scared"
    ],
    "Surprise": [
        "Astonishment", "Amazement", "Wonder", "Shock", "Bewilderment",
        "Awe", "Disbelief", "Revelation", "Unexpectedness", "Stunned",
        "Flabbergasted", "Perplexity", "Startled", "Confused"
    ],
    "Disgust": [
        "Revulsion", "Loathing", "Repulsion", "Aversion", "Contempt",
        "Disdain", "Abhorrence", "Nauseated", "Squeamishness", "Detestation",
        "Repugnance", "Sickened", "Offended", "Scorn"
    ],
    "Love": [
        "Affection", "Fondness", "Adoration", "Devotion", "Passion",
        "Tenderness", "Warmth", "Caring", "Empathy", "Compassion",
        "Attachment", "Infatuation", "Liking", "Benevolence", "Cherish"
    ],
    "Calmness": [
        "Serenity", "Tranquility", "Peace", "Relaxation", "Placidness",
        "Composure", "Equanimity", "Stillness", "Relief", "Harmony",
        "Collectedness", "Patience", "Poise", "Soothing", "Untroubled"
    ],
    "Excitement": [
        "Enthusiasm", "Eagerness", "Thrill", "Anticipation", "Exhilaration",
        "Vivacity", "Zest", "Fervor", "Animation", "Elated",
        "Keenness", "Agitation (positive sense)", "Frenzy (positive sense)"
    ],
    "Anxiety": [
        "Worry", "Apprehension", "Nervousness", "Dread", "Unease",
        "Tension", "Stress", "Agitation", "Perturbation", "Foreboding",
        "Restlessness", "Concern", "Distress", "Fretting", "Panicked"
    ],
    "Shame": [
        "Guilt", "Embarrassment", "Humiliation", "Mortification", "Remorse",
        "Regret", "Self-reproach", "Indignity", "Disgrace", "Blush",
        "Abasement", "Contrition"
    ],
    "Pride": [
        "Accomplishment", "Satisfaction", "Dignity", "Self-respect", "Triumph",
        "Confidence", "Self-esteem", "Arrogance (negative connotation)", "Smugness",
        "Vanity", "Exultation", "Hubris"
    ],
    "Confusion": [
        "Perplexity", "Bewilderment", "Disorientation", "Mystification", "Muddled",
        "Dazed", "Uncertainty", "Puzzlement", "Incomprehension", "Bafflement",
        "Obfuscation"
    ],
    "Boredom": [
        "Tedium", "Ennui", "Apathy", "Disinterest", "Weariness",
        "Monotony", "Flatness", "Listlessness", "Indifference", "Jaded",
        "Lethargy"
    ],
    "Hope": [
        "Optimism", "Expectation", "Aspiration", "Belief", "Promise",
        "Encouragement", "Anticipation", "Faith", "Wishfulness", "Longing",
        "Confidence"
    ],
    "Awe": [
        "Wonder", "Reverence", "Admiration", "Veneration", "Respect",
        "Amazement", "Sublimity", "Speechless", "Overwhelmed"
    ],
    "Gratitude": [
        "Thankfulness", "Appreciation", "Recognition", "Indebtedness", "Obligation (positive)",
        "Grace", "Blessing", "Joy (from being grateful)"
    ]
}

# --- How to use this dictionary ---

if __name__ == "__main__":
    print("--- General Emotion Lexicon ---")

    # Get specific words for a general emotion
    print("\nSpecific words for 'Happiness':")
    for word in emotions_lexicon["Happiness"]:
        print(f"- {word}")

    print("\nSpecific words for 'Fear':")
    print(emotions_lexicon["Fear"])

    # Iterate through all general emotions and their specific words
    print("\n--- All Emotions and Their Specifics ---")
    for general_emotion, specific_words in emotions_lexicon.items():
        print(f"\n{general_emotion}:")
        print(f"  {', '.join(specific_words)}")

    # Check if a specific word exists under a general emotion
    if "Joy" in emotions_lexicon["Happiness"]:
        print("\n'Joy' is a specific word for 'Happiness'.")

    if "Scared" in emotions_lexicon["Fear"]:
        print("'Scared' is a specific word for 'Fear'.")

    if "Happy" in emotions_lexicon["Happiness"]:
        print("'Happy' is a specific word for 'Happiness'.") # This will print as "Happy" itself is a specific
    else:
        print("Note: 'Happy' itself is not explicitly listed as a specific under 'Happiness' in this lexicon, though it's the root.")
