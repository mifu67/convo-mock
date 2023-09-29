import json
import os
import openai

from dotenv import load_dotenv
from typing import List

MODEL = "gpt-3.5-turbo"
NUM_TOPICS = 6
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def append_line(line: str, messages: List[dict]) -> None:
    split_line = line.split(": ")
    if split_line[0] == "ERIKA":
        messages.append({"role": "user", "content": split_line[1]})
    else:
        messages.append({"role": "assistant", "content": split_line[1]})

def main():
    intro_file = "intro-erika-julian.txt"
    outro_file = "outro-erika-julian.txt"
    # begin with Erika and Julian's introductory conversation
    f = open(intro_file, 'r')
    for line in f:
        print(line.strip())
        input()
    f.close()
    
    initial_messages_f = open('initial-messages.json')
    initial_messages = json.load(initial_messages_f)
    initial_messages_f.close()

    responses_f = open('responses.json')
    responses = json.load(responses_f)
    responses_f.close()

    num_topics_explored = 0
    messages = initial_messages
    explored_topics_set = set()
    print("Type 'end conversation' to end the conversation.")

    # I probably need to clean this up at some point
    # to do tomorrow: consolidate all system messages, stop the model from making things up, work on line delivery, implement hints
    while True:
        if num_topics_explored == NUM_TOPICS:
            break

        user_input = input("ERIKA: ")
        if user_input == "end conversation":
            break
        print("")
        messages.append({"role": "user", "content": user_input})
        response_raw = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0,
        )
        response = response_raw["choices"][0]["message"]["content"]
        # tag is first 30 characters
        tag = response[:30]
        if tag == "Conversation topic 1 triggered":
            explored_topics_set.add(1)
            num_topics_explored += 1
            for line in responses["1"]["text"]:
                print(line)
                input()
            messages += responses["1"]["messages"]
        elif tag == "Conversation topic 2 triggered":
            explored_topics_set.add(2)
            num_topics_explored += 1
            for line in responses["2"]["text"]:
                print(line)
                input()
            messages += responses["2"]["messages"]
        elif tag == "Conversation topic 3 triggered":
            explored_topics_set.add(3)
            num_topics_explored += 1
            for line in responses["3"]["text"]:
                print(line)
                input()
            messages += responses["3"]["messages"]
        elif tag == "Conversation topic 4 triggered":
            explored_topics_set.add(4)
            num_topics_explored += 1
            if not (3 in explored_topics_set):
                confused_line = "JULIAN: What? Oh, did August also tell you yesterday that he had to do something at midnight?"
                print(confused_line)
                messages.append({"role": "assistant", "content": confused_line})
            for line in responses["4"]["text"]:
                print(line)
                input()
            messages += responses["4"]["messages"]
        elif tag == "Conversation topic 5 triggered":
            explored_topics_set.add(5)
            num_topics_explored += 1
            if not (3 in explored_topics_set or 2 in explored_topics_set):
                confused_line = "JULIAN: How did you know about that?"
                print(confused_line)
                messages.append({"role": "assistant", "content": confused_line})
            for line in responses["5"]["text"]:
                print(line)
                input()
            messages += responses["5"]["messages"]
        elif tag == "Conversation topic 6 triggered":
            explored_topics_set.add(6)
            # this is a bonus question that doesn't count towards conversation topics
            for line in responses["6"]["text"]:
                print(line)
                input()
            messages += responses["6"]["messages"]
        elif tag == "Conversation topic 7 triggered":
            explored_topics_set.add(7)
            num_topics_explored += 1
            for line in responses["7"]["text"]:
                print(line)
                input()
            messages += responses["7"]["messages"]
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