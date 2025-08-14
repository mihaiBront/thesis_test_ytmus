from dataclasses import dataclass, field
from requests.utils import default_headers
from lib.Serializable import Serializable

'''{
    "type": "function",
    "function": {
      "name": "browse_web",
      "description": "Retrieve HTML content from a live webpage. Always call this if the user's request requires information from a given URL.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "The exact URL of the page to fetch."
          }
        },
        "required": ["url"]
      }
    }
  }'''
  
@dataclass
class OllamaToolFunctionProperty(Serializable):
    type: str = field(default_factory=str)
    description: str = field(default_factory=str)
  
@dataclass
class OllamaToolFunctionParameters(Serializable):
    type: str = field(default_factory=str)
    properties: dict[str, OllamaToolFunctionProperty] = field(default_factory=OllamaToolFunctionProperty)
    required: list[str] = field(default_factory=list)
  
@dataclass
class OllamaToolFunction(Serializable):
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    parameters: OllamaToolFunctionParameters = field(default_factory=OllamaToolFunctionParameters)

@dataclass
class OllamaTool(Serializable):
    type: str = field(default_factory=str)
    function: OllamaToolFunction = field(default_factory=OllamaToolFunction)

    def _main(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def _validate_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.function.parameters.properties:
                raise ValueError(f"Invalid keyword argument: {key}")
            if value is None:
                raise ValueError(f"Value for keyword argument {key} is None")

        if any(key not in kwargs for key in self.function.parameters.required):
            raise ValueError("Missing required keyword arguments")
        return True
    
    def run(self, **kwargs):
        self._validate_kwargs(**kwargs)
        return self._main(**kwargs)
    
    def to_payload(self):
        return self.to_dict()