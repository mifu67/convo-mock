import json
import os
import openai

from dotenv import load_dotenv
from typing import List

MODEL = "gpt-3.5-turbo"
NUM_TOPICS = 6
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

RESPONSES_F = open('responses.json')
RESPONSES = json.load(RESPONSES_F)
RESPONSES_F.close()

def check_for_question(input: str, messages: List[dict]) -> bool:
    messages.append({"role": "user", "content": input})
    response_raw = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0,
        )
    response = response_raw["choices"][0]["message"]["content"]
    messages.pop()
    return response == "Y"

def process_tag(index, contains_question, explored_topics_set, 
                response, messages, num_topics_explored) -> int:
    if contains_question:
        explored_topics_set.add(index)
        if index != 6:
            num_topics_explored += 1
        for line in RESPONSES[str(index)]["text"]:
            print(line)
            input()
        messages += RESPONSES[str(index)]["messages"]
    else:
        print(response[32:])
        messages.append({"role": "assistant", "content": response[30:]})
    return num_topics_explored
    
def main():
    intro_file = "intro-erika-julian.txt"
    outro_file = "outro-erika-julian.txt"
    # begin with Erika and Julian's introductory conversation
    f = open(intro_file, 'r')
    for line in f:
        if line[0] == "#":  
            print(line[1:].strip())
        else:
            print(line.strip())
            # input()
    f.close()
    
    initial_messages_f = open('initial-messages.json')
    initial_messages = json.load(initial_messages_f)
    initial_messages_f.close()

    check_q_messages_f = open('check-q-messages.json')
    check_q_messages = json.load(check_q_messages_f)
    check_q_messages_f.close()

    num_topics_explored = 0
    messages = initial_messages
    explored_topics_set = set()

    # I probably need to clean this up at some point
    # To do: implement hints and debug dialogue tree direction. Use LLM RESPONSES for previously explored topics.
    while True:
        if num_topics_explored == NUM_TOPICS:
            break

        user_input = input("ERIKA: ")
        if user_input == "end conversation":
            break
        while not user_input:
            user_input = input("ERIKA: ")
        contains_question = check_for_question(user_input, check_q_messages)
        print("")
        messages.append({"role": "user", "content": user_input})
        response_raw = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0,
        )
        response = response_raw["choices"][0]["message"]["content"]
        print(response)
        # tag is first 30 characters
        tag = response[:30]
        
        if tag == "Conversation topic 1 triggered":
            num_topics_explored = process_tag(1, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 2 triggered":
            num_topics_explored = process_tag(2, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 3 triggered":
            num_topics_explored = process_tag(3, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 4 triggered":
            if (not (3 in explored_topics_set) and contains_question):
                confused_line = "JULIAN: What? Oh, did August also tell you yesterday that he had to do something at midnight?"
                print(confused_line)
                messages.append({"role": "assistant", "content": confused_line})
            num_topics_explored = process_tag(4, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 5 triggered":
            explored_topics_set.add(5)
            num_topics_explored += 1
            if (not (3 in explored_topics_set or 2 in explored_topics_set) and contains_question):
                confused_line = "JULIAN: How did you know about that?"
                print(confused_line)
                messages.append({"role": "assistant", "content": confused_line})
            num_topics_explored = process_tag(5, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 6 triggered":
            num_topics_explored = process_tag(6, contains_question, explored_topics_set, response, messages, num_topics_explored)
        elif tag == "Conversation topic 7 triggered":
            num_topics_explored = process_tag(7, contains_question, explored_topics_set, response, messages, num_topics_explored)
        else:
            print("JULIAN: " + response)
        messages.append({"role": "assistant", "content": response})
    
    f = open(outro_file, 'r')
    for line in f:
        print(line.strip())
        input()
    f.close()
if __name__ == "__main__":
    main()