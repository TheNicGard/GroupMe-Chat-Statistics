#!/usr/bin/python3
import datetime
import json

class Texter:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.text_count = 0
        self.word_count = 0
        self.like_count = 0

def scan_message(m, texters, text_number, word_number, print_messages):
    m_name = m.get("name")
    m_text = m.get("text")
    m_created_at = m.get("created_at")
    m_favorited_by = m.get("favorited_by")
    m_sender_id = m.get("sender_id")
            
    if m_name and m_text and m_created_at and m_sender_id:
        for t in texters:
            if t.id in m_favorited_by:
                t.like_count += 1
                        
        for t in texters:
            if t.id == m_sender_id:
                t.text_count += 1
                t.word_count += len(m_text.split())
                break
                    
        text_number += 1
        word_number += len(m_text.split())
        if print_messages:
            print(m_name + ": \"" + m_text + "\" at " + datetime.datetime.fromtimestamp(m_created_at).strftime('%Y-%m-%d %H:%M:%S'))

    return text_number, word_number
    
def read_messages():
    with open("message.json", "r") as read_file:
        data = json.load(read_file)

        person_a = Texter("Person A", "101")
        person_b = Texter("Person B", "102")

        print_messages = True
        reverse_order = True
        
        texters = [person_a, person_b]
        
        text_number = 0
        word_number = 0

        if reverse_order:
            for m in data:
                text_number, word_number = scan_message(m, texters, text_number, word_number, print_messages)
        else:
            for m in reversed(data):
                text_number, word_number = scan_message(m, texters, text_number, word_number, print_messages)
                
        print("There were a total of " + str(text_number) + " messages.")
        print("There were a total of " + str(word_number) + " words typed.")

        print("")

        for t in texters:
            print(t.name + " made " + str(t.text_count) + " messages (" + ("{:02.1f}").format(t.text_count / text_number * 100) + "%).")
            print(t.name + " texted " + str(t.word_count) + " words (" + ("{:02.1f}").format(t.word_count / word_number * 100) + "%).")
            print("")

        for t in texters:
            print(t.name + " liked " + str(t.like_count) + " messages.")

read_messages()
