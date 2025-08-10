from dataclasses import dataclass, field
from requests.utils import default_headers
from lib.Serializable import Serializable

@dataclass
class OllamaToolFunctionParameters(Serializable):
    type: str = field(default_factory=str)
    properties: dict[str, dict] = field(default_factory=dict)
    required: list[str] = field(default_factory=list)


@dataclass
class OllamaToolFunction(Serializable):
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    parameters: OllamaToolFunctionParameters = \
        field(default_factory=OllamaToolFunctionParameters)


@dataclass
class OllamaTool(Serializable):
    type: str = field(default_factory=str)
    function: OllamaToolFunction = \
        field(default_factory=OllamaToolFunction)