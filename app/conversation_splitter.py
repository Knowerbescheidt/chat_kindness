import re
from app.utils import Probanden_file
from dataclasses import dataclass
from app.config import sentences_to_split_before, kind_phrases
from typing import Optional
import copy


@dataclass
class Interaction:
    proband:str
    chat_bot:str
    full_chat:str 
    proband_text:str
    chat_bot_text:str
    bot_kindness:Optional[float]=0
    proband_kindness:Optional[float]=0

    
def texts_to_interaction(pb_files:list[Probanden_file])->list[Interaction]:
    total_interactions = []

    for pb_file in pb_files:
        
        if not all(sentence in pb_file.text for sentence in sentences_to_split_before):
            logging.warning("problem with this text")

        interactions_grouped = split_to_interactions(pb_file)
        for item in interactions_grouped:
            total_interactions.append(item)
    return total_interactions
            
def split_to_interactions(pb_file:Probanden_file)->list[Interaction]:
    split_by = [sentence for sentence in sentences_to_split_before if sentence in pb_file.text[30:]]

    first_question = find_first_substring(pb_file.text, substrings=split_by)

    split_by.remove(first_question)
    split_by.insert(0, first_question)

    first_interaction, intro2, rest23  = pb_file.text.partition(split_by[0]) 
    second_interaction, intro3, rest3  = (intro2+rest23).partition(split_by[1]) 
    third_interaction = intro3 + rest3

    chats = [first_interaction,second_interaction,third_interaction]

    interactions = chats_to_interactions(chats, pb_file.proband)

    return interactions

def chats_to_interactions(chats:list[str], proband)->list[Interaction]:
    interactions = []
    for chat in chats:
        chat_bot_name = extract_chat_bot_name(chat)
        proband_messages = extract_proband_messages(chat)
        chat_bot_text = get_chat_bot_text(chat, proband_messages)
        proband_text = " ".join(proband_messages)

        interaction = Interaction(proband=proband,
                                  chat_bot=chat_bot_name, 
                                  full_chat=chat, 
                                  proband_text=proband_text, 
                                  chat_bot_text=chat_bot_text)
        interactions.append(interaction)
    return interactions


def find_first_substring(string, substrings):
    first_substring = None
    first_position = float('inf')

    for sub in substrings:
        position = string.find(sub)
        if position != -1 and position < first_position:
            first_position = position
            first_substring = sub

    return first_substring

def extract_chat_bot_name(chat:str)->str:
    if "KIM" in chat:
        return "KIM"
    elif "I.D.A" in chat:
        return "I.D.A"
    elif "Anna" in chat:   
        return "Anna"
    else:
        raise Exception("No chatbot name found in the chat %s", chat)

def extract_proband_messages(chat:str) -> list[str]:
    pattern = r"Proband:(.*?)(?=\n\n)"
    proband_messages = re.findall(pattern, chat, re.DOTALL)
    stripped_messages = [msg.strip() for msg in proband_messages]

    pattern = r"Proband:"
    proband_matches = re.findall(pattern, chat, re.DOTALL)

    if len(proband_matches) != len(stripped_messages):
        raise Exception("Extraction of proband texts did not work")
    
    return stripped_messages


def get_chat_bot_text(chat:str, proband_messages:list[str])->str:
    
    to_remove = copy.deepcopy(proband_messages)
    to_remove.append("Proband:")

    to_remove_sorted = sorted(to_remove, key=len, reverse=True)
    
    for substring in to_remove_sorted:
        chat = chat.replace(substring, "")

    return chat


