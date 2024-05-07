from conversation import Conversation

class Chatbot:

    def __init__(self):
        pass

    def get_user_input(self):
        message = input("Enter your input: ")
        return message

    def display_message(self, action, output):
        print(f"[{action}]")
        print(f"[AI] : {output}")
