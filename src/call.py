from langchain.memory import ConversationBufferMemory
from conversation import Conversation
from chatbot import Chatbot
from voice_bot_copy import voice_bot
from post_function_calling import PostFunctionCalling
from from_request import FromRequest
import pickle


class Call : 

    def __init__(self, config, phone_number : str, ux : str, memory_path : str = None) -> None:
        self.config = config
        self.phone_number = phone_number
        if memory_path is not None:
            with open(memory_path, 'rb') as file:
                self.memory = pickle.load(file)
        else:
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.call_variable = {}
        self.ux = ux
        self.config = config

    
    def save_memory_to_file(self, path : str) -> None:
        with open(path, 'wb') as file:
            pickle.dump(self.memory, file)

    def read_memory_from_file(self, path : str) -> None:
        with open(path, 'rb') as file:
            self.memory = pickle.load(file)
        

    def run(self , current_key : str = "start", saving = False) -> str:
        current_object = self.config[current_key]
        current_type = current_object["type"]
        if "save_memory_for_testing" in current_object and saving:
            print("in save memory")
            self.save_memory_to_file(current_object["save_memory_for_testing"])


        if current_type == "conversation" :
            print(current_object.keys())
            conversation = Conversation(self.memory, self.ux, **current_object)
            if current_key == "start" :
                next_key = conversation.run("[START CONVERSATION WITH WELCOME MESSAGE]")
            else :
                next_key = conversation.run()
            print(next_key)
            self.run(next_key, saving)

        elif current_type == "post_function_calling" :
            function_calling = PostFunctionCalling(self.call_variable, self.memory, **current_object)
            next_key = function_calling.run()
            self.run(next_key, saving)
        
        elif current_type == "request" :
            request = FromRequest(self.call_variable, **current_object)
            next_key = request.run()
            self.run(next_key, saving)
            


if __name__ == "__main__" :
    ux = Chatbot()
    call = Call(voice_bot, "1234567890", ux)
    call.run()


        
        