from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import time
import os
from langchain_groq import ChatGroq


class Conversation() :


    def __init__(self, 
                 memory : ConversationBufferMemory,
                 ux,
                 **kwargs
                 ) :
        
        self.memory = memory
        self.ux = ux
        self.system_prompt = kwargs.get("system_prompt")
        self.model_name = kwargs.get("model_name")
        self.action = kwargs.get("action")
        self.start_with_human = kwargs.get("start_with_human", False)
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])
        self.to_display_action = kwargs.get("to_display_action")

        self.retry = kwargs.get("retry", 3)
        # self.llm = ChatOpenAI(temperature=0.3, model_name=self.model_name, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.llm = self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )    


    def extract_action(self, text): 
        t = text.split("]")
        #check format of first element is [SOMETHING]
        action = t[0].strip()
        if t[0][0] == "[":
            action = t[0].strip() + "]"
        text = ""
        if len(t) == 2:
            text = t[1].strip()
        else : 
            text = " ".join(t[1:]).strip()
        return action, text.strip()
    
    
    def display_message(self, action, text):
        if action in self.to_display_action:
            self.ux.display_message(action, text)
            self.memory.chat_memory.add_ai_message(text)
        
        else : 
            print(action, text)


    def define_next_step(self, action, text):
        if action in self.action:
            next_step = self.action[action]
            if isinstance(next_step, dict) : 
                print(next_step)
                next_step = next_step[text]
        else : 
            print("in next step action")
            print(action)
            next_step = "retry"
        
        print(next_step)
        return next_step, text 
    
    
    def invoke(self, text):
        response = self.conversation.invoke({"text": text})
        action, output_text = self.extract_action(response['text'])
        return action, *self.define_next_step(action, output_text)
    
    
    def run(self, text = "contine_conversation"):

        if self.start_with_human :   
            text = self.ux.get_user_input()
            self.memory.chat_memory.add_user_message(text)

        action, next_step, output_text = self.invoke(text)

        if next_step == "retry" :
            if self.retry > 0 :
                self.retry -= 1
                action, next_step, output_text = self.invoke(text)
            else :
                raise ValueError("Too many retries")

        self.display_message(action, output_text)

        if next_step == "continue" :
            self.start_with_human = True
            return self.run()
    
        return next_step

