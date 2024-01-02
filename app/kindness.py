from app.config import kind_phrases
from app.conversation_splitter import Interaction
import re

def calculate_kindness(interactions:list[Interaction]):
    for interaction in interactions:
        interaction.proband_kindness = calculate_rel_kindness(interaction.proband_text)
        interaction.bot_kindness = calculate_rel_kindness(interaction.chat_bot_text)

    return interactions

    

def calculate_rel_kindness(text: str):
    text = text.replace("\n", " ")
    
    text = text.lower()
    kind_phrases_used = 0
    for phrase in kind_phrases:
        count = text.count(phrase.lower())
        kind_phrases_used += count

    total_numb_words = count_words(text)

    result = round(kind_phrases_used / total_numb_words * 100, ndigits=3)

    return result

def count_words(text):
    # Split the text into words using a regular expression
    words = re.findall(r'\b\w+\b', text)

    # Return the count of words
    return len(words)