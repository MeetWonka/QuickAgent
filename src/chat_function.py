# Import necessary modules
from os import getenv
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import openai
import time
import logging
import os
import json
import traceback
from openai import AsyncOpenAI
import openai


class ChatFunction():
    """
    Class to handle generating json formated responses using OpenAI's ChatCompletion API,.
    """

    def __init__(self, prompt_template, **kwargs):
        """
        Initialize ChatFunction instance.

        Args:
            - prompt_template (tab): Langchain prompt template.
            - kwargs: Additional keyword arguments for configuring the OpenAI API.
        """
        # Set default model and deployment_id if not provided
        if "model" not in kwargs and "deployment_id" not in kwargs :
            kwargs["model"] = "gpt-3.5-turbo-0613"      
        self.client = AsyncOpenAI()
        self.kwargs = kwargs
        self.prompt_template = prompt_template


    def _format_prompt(self, input):
        """
        Format chat prompt messages.

        Args:
            - input (dict): Input messages to be formatted.

        Returns:
            - list: Formatted messages.
        """
        s = self.prompt_template.format_messages(**input)
        ss = []
        for i in s:
            if isinstance(i, SystemMessage):
                ss.append({"role": "system", "content": i.content})
            elif isinstance(i, HumanMessage):
                ss.append({"role": "user", "content": i.content})
            elif isinstance(i, AIMessage):
                ss.append({"role": "assistant", "content": i.content})
        return ss
    

    async def generate(self, function_schema=[], no_error=False, retry=2, config = {}, **kwargs):
        """
        Generate response using OpenAI ChatCompletion API.

        Args:
            - function_schema (dict): Schema for the chat function.
            - no_error (bool): Flag to suppress errors and return "ERROR" instead.
            - retry (int): Number of retries in case of error.
            - kwargs: The function template argument needed to fill the template prompt. 

        Returns:
            - dict: Response from the ChatCompletion API.
        """
        try:
            
            if retry < 0:
                raise ValueError("Too many retries")
            
            if len(function_schema) == 0:
                raise ValueError("No function schema")
            
            response = await self.client.chat.completions.create(
                **self.kwargs,
                messages=self._format_prompt(kwargs),
                functions=function_schema,
                function_call={"name": function_schema[0]["name"]}
            ) 
            args = json.loads(response.choices[0].message.function_call.arguments)
            return args
        
        # Handle RateLimitError
# except openai.error.RateLimitError as e:
        #     print("Rate Limit Error, retrying in {} seconds".format(4*(5-retry+1)))
        #     logging.info("Rate Limit Error, retrying in {} seconds".format(4*(5-retry+1)))
        #     time.sleep(4*(5-retry+1))
        #     self.generate(function_schema, no_error, retry=retry-1, **kwargs)

        # # Handle ServiceUnavailableError
        # except openai.error.ServiceUnavailableError as e:
        #     logging.info("Service Unavailable Error, retrying in {} seconds".format(4*(5-retry+1)))
        #     print("Rate Limit Error, retrying in {} seconds".format(4*(5-retry+1)))
        #     time.sleep(4*(5-retry+1))
        #     self.generate(function_schema, no_error, retry=retry-1, **kwargs)
        #     raise openai.error.RateLimitError("Unstable Error: " + str(e)) from e
        
        # Handle other exceptions
        except Exception as e:
            print(traceback.format_exc())
            # If no_error flag is set, return "ERROR" without raising exception
            if no_error:
                logging.error(e)
                logging.error(traceback.format_exc())
                print(e)
                return "ERROR"
            else:
                # If retry count is exhausted, log error to SQL database and return "ERROR"
                if retry == 0:
                    self.sql.insert(f"error_function_call_{function_schema[0]['name']}", 
                                    f"INPUT \n\n {kwargs} \n\n ERROR \n\n {traceback.format_exc()}", 
                                    config = config)
                    return "ERROR"
                # Retry with reduced retry count
                return await self.generate(function_schema, no_error, retry=retry-1, **kwargs)



if "__main__" == __name__ : 
    import asyncio
    async def run_chat():
        chat = ChatFunction(CLASSIFIER_PROMPT, model="GPT-4")
        result = await chat.generate(get_function_array("fr"), input="Comment changer de chaudière ?")
        print(result)
    
    asyncio.run(run_chat())
