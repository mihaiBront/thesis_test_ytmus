# Test suite import 
from unittest import TestCase

# Tested libs imports
from LLMapi.OllamaInterface import OllamaInterface
from LLMapi.OllamaTool import OllamaTool

# Other imports
import os
from lib.LoggingHelper import LoggingHelper
import logging as log

_log = LoggingHelper.init_logger("DEBUG", "dark")

class TestOllamaTool(TestCase):
    def test_deserialize_tool(self):
        print(os.listdir())
        
        #arrange/act
        tool = OllamaTool.from_file("resources/LLM/ollama_tools/web_browse.json")
        
        #assert
        self.assertIsNotNone(tool)
        self.assertEqual(tool.type, "function")
        
        log.info(tool)
        
class TestOllamaInterface(TestCase):
    def test_instantiate_interface(self):
        o_if = OllamaInterface.from_file("resources/LLM/config_ollama.json")
        log.info(o_if)
        
        self.assertIsNotNone(o_if)
        self.assertEqual(o_if.model_name, "mistral")
        
        o_if.load_tools()
        log.info(o_if)
        
        self.assertTrue("tools" in o_if.kwargs)
        self.assertGreater(len(o_if.kwargs["tools"]), 0)
        
    
    def test_simple_prompt(self):
        o_if: OllamaInterface = OllamaInterface.from_file("resources/LLM/config_ollama.json")
        mess = o_if.predict("Hi, how are you doing today?")
        
        print(mess)
        
        self.assertNotEqual(mess, "")
        
    def test_web_browse_tool(self):
        o_if: OllamaInterface = OllamaInterface.from_file("resources/LLM/config_ollama.json")
        
        link: str = "https://www.youtube.com/watch?v=J0DzXAx9qjI?"
        title: str = "The Importance of Real Things"
        
        mess = o_if.predict_web(f"Could you tell me the title of a youtube video from this link: {link}")
        self.assertTrue(title.lower() in mess[0].lower(),  f"Returned string does not contain the title of the video ({title})")