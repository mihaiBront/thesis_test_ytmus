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

class TestOllamaInterface(TestCase):
    