from langchain.memory import ConversationBufferMemory
from conversation import Conversation
from chatbot import Chatbot
from voice_bot_copy import voice_bot
from post_function_calling import PostFunctionCalling


class Call : 

    def __init__(self, config, phone_number : str, ux : str) -> None:
        self.config = config
        self.phone_number = phone_number
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.call_variable = {}
        self.ux = ux
        self.config = config
        

    def run(self , current_key : str = "start") -> str:
        current_object = self.config[current_key]
        current_type = current_object["type"]
        print(current_object.keys())
        if current_type == "conversation" :
            print(current_object.keys())
            conversation = Conversation(self.memory, self.ux, **current_object)
            next_key = conversation.run()
            print(next_key)
            self.run(next_key)

        elif current_type == "post_function_calling" :
            function_calling = PostFunctionCalling(self.call_variable, self.memory, **current_object)
            function_calling.run()
        
        elif current_type == "conversation" :
            print("conversation")


if __name__ == "__main__" :
    ux = Chatbot()
    call = Call(voice_bot, "1234567890", ux)
    call.run()


        
        