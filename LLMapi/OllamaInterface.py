from dataclasses import dataclass, field
from ollama import Client
from lib.Serializable import Serializable
from lib.LoggingHelper import LoggingHelper
from LLMapi.iOllamaTool import OllamaTool
from LLMapi.OllamaTools.URLParser import UrlParser

import json
import logging as log

_log = LoggingHelper.init_logger("DEBUG", "dark")

@dataclass
class OllamaInterfaceConfig(Serializable):
    system_prompt: str = field(default_factory=str)
    tools: list[str] = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)

@dataclass
class OllamaInterface(Serializable):
    model_name: str = field(default_factory=str)
    version: str = field(default_factory=str)
    api_endpoint: str = field(default_factory=str)
    config: OllamaInterfaceConfig = field(default_factory=OllamaInterfaceConfig)
    
    __tools: dict[str: OllamaTool] = field(default_factory=list)
    __chat_options: dict = field(default_factory=dict) 
    __client: Client = field(default_factory=Client)
    __chat_history: list[dict] = field(default_factory=list)
    
    def __post_init__(self):
        self.__tools = {}
        with open(self.config.system_prompt, "r") as file:
            self.config.system_prompt = file.read()
        self.__load_tools()
        self.__init_chat_options()
        self.__add_tools_payload_to_options()
        self.__client = Client(host=self.api_endpoint)
        self.__init_chat_history()

#region Private methods

    def __init_chat_options(self):
        # Use the config kwargs structure directly - it should match Ollama client expectations
        self.__chat_options = self.config.kwargs.copy()
        
    def __load_tools(self):
        for tool in self.config.tools:
            match tool:
                case "url_parser":
                    self.__tools.update({
                        "url_parser": UrlParser.from_file(
                            "LLMapi/OllamaTools/URLParser.json"
                        )
                    })
                case _:
                    continue
    
    def __add_tools_payload_to_options(self):
        self.__chat_options["tools"] = [tool.to_payload() for tool in self.__tools.values()]
        
    def __add_message(self, role: str, content: str, tool_calls=None):
        message = {
            "role": role,
            "content": content
        }
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.__chat_history.append(message)
    
    def __init_chat_history(self):
        self.__chat_history = []
        self.__add_message("system", self.config.system_prompt)
        
    def __run_tool(self, tool_call: dict):
        tool_name = tool_call['function']['name']
        arguments = tool_call['function']['arguments']
        
        # Map tool names
        tool_mapping = {
            "browse_web": "url_parser"
        }
        mapped_tool_name = tool_mapping.get(tool_name, tool_name)
        
        if mapped_tool_name not in self.__tools:
            return {"error": f"Tool {tool_name} not found"}
            
        tool = self.__tools[mapped_tool_name]
        return tool.run(**arguments)
#endregion

#region Public methods
    def chat(self, user_input: str):
        self.__add_message("user", user_input)
        response = self.__client.chat(
            model=self.model_name,
            messages=self.__chat_history,
            **self.__chat_options
        )
        if 'message' in response and 'tool_calls' in response['message']:
            tool_calls = response['message']['tool_calls']
            self.__add_message("assistant", response['message'].get('content', ''), tool_calls)
            
            # Execute each tool call
            for tool_call in tool_calls:
                tool_result = self.__run_tool(tool_call)
                
                # Add tool result to chat history
                self.__add_message("tool", json.dumps(tool_result))
            
            # Get model response with tool results
            response = self.__client.chat(
                model=self.model_name,
                messages=self.__chat_history,
                **self.__chat_options
            )
        
        # Add final assistant response to history
        if 'message' in response:
            self.__add_message("assistant", response['message']['content'])
            return response['message']['content']
        return "No response generated"
#endregion

if __name__ == "__main__":
    ollama_interface = OllamaInterface.from_file(
        "LLMapi/res/config_ollama.json"
    )
    
    log.info(ollama_interface._OllamaInterface__chat_options)
    print(ollama_interface.chat("Could you tell me what videos appear to you on https://www.youtube.com/"))
    log.info(ollama_interface._OllamaInterface__chat_history)