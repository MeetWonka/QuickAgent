from openai import OpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import json

class PostFunctionCalling :

    def __init__(self, call_variable, memory, **kwargs) -> None:
        self.call_variable = call_variable
        self.memory = memory
        self.system_prompt = kwargs.get("system_prompt")
        self.model_name = kwargs.get("model_name")
        self.function_schema = kwargs.get("function_calling_prompt")
        self.to_call_variable = kwargs.get("save_to_call_variable")
        self.is_save_to_call_variable = kwargs.get("save_to_call_variable", True)
        self.name = kwargs.get("function_calling_name", "function_calling")
        self.replacement_value = kwargs.get("replacement_value", {})
        self.action = kwargs.get("action")
        self.client = OpenAI()

    
    def _format_prompt(self, messages):
        """
        Format chat prompt messages.

        Args:
            - input (dict): Input messages to be formatted.

        Returns:
            - list: Formatted messages.
        """
        
        ss = [{"role": "system", "content": self.system_prompt}]
        for i in messages:
            if isinstance(i, SystemMessage):
                ss.append({"role": "system", "content": i.content})
            elif isinstance(i, HumanMessage):
                ss.append({"role": "user", "content": i.content})
            elif isinstance(i, AIMessage):
                ss.append({"role": "assistant", "content": i.content})
        return ss
    

    def build_message(self):
        memory_message = self.memory.load_memory_variables({"memory_key" : ""})
        print(memory_message)
        memory_message_list = self._format_prompt(memory_message['chat_history'])
        print(memory_message_list)
        return memory_message_list
    
    
    def build_function_schema(self): 
        function_schema = [{
            "name": self.name,
            "parameters": {
                "type": "object",
                "properties": {
                    **self.function_schema
                },
            "required" : list(self.function_schema.keys())
            }
        }]
        return function_schema
    

    def save_to_call_variable(self, args):
        if self.is_save_to_call_variable:
            for key, value in args.items():
                if key in self.replacement_value:
                    value = self.replacement_value[key].get(value, value)
                self.call_variable[key] = value           

    
    def run(self):
        messages = self.build_message()
        print(messages)
        print('running post function calling')
        function_schema = self.build_function_schema()
        print(function_schema)

        response = self.client.chat.completions.create(
            model = self.model_name,
            messages=messages,
            functions=function_schema,
            function_call={"name": function_schema[0]["name"]}
        )
        args = json.loads(response.choices[0].message.function_call.arguments)
        self.save_to_call_variable(args)
        print(args)
        return self.action["[DEFAULT]"]
        
        