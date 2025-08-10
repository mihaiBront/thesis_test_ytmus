from dataclasses import dataclass, field
import ollama, llm_axe
from lib.Serializable import Serializable

import requests
import json

@dataclass
class OllamaInterface(Serializable):
    model_name: str = field(default_factory=str)
    version: str = field(default_factory=str)
    api_endpoint: str = field(default_factory=str)
    max_content_size_web: int = field(default_factory=int)
    temperature: float = field(default_factory=float)
    
    kwargs: dict = field(default_factory=dict)
    
    tools: list[str] = field(default_factory=list) 
    session = requests.Session()
    
    def load_tools(self):
        base_dir: str = "resources/LLM/ollama_tools"
        
        _tools: list[dict] = []
            
        for tool in self.tools:
            _tool_name = f"{base_dir}/{tool}.json"
            with open(_tool_name, "r") as f:
                _tools.append(json.loads(f.read()))
            
        self.kwargs["tools"] = _tools
    
    def fetch_web(self, url):
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            return resp.text[:3000]  # limit to avoid overload
        except Exception as e:
            return f"Error fetching URL: {str(e)}"
    
    def _continue_chat(self, payload):
        output = ""
        with self.session.post(self.api_endpoint.replace("/generate", "/chat"), json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    j = json.loads(line.decode('utf-8'))
                    if "message" in j and "content" in j["message"]:
                        output += j["message"]["content"]
        return [output.strip()]
    
    def predict(self, question, **kwargs):
        output = ""
        payload = {'model': self.model_name, 'prompt': question, **self.kwargs}

        with self.session.post(self.api_endpoint, json=payload, stream=True) as r:
            if r.status_code == 200:
                for line in r.iter_lines():
                    if line:
                        j = json.loads(line.decode('utf-8'))
                        output += j.get("response", "")
                        if j.get("done", True):
                            break
            else:
                print(f"Error: Received status code {r.status_code}")

        return [output.strip()]
    
    def predict_web(self, question, kwargs):
        #implement web tool here
        pass

    def __call__(self, question, **kwargs):
        return self.predict(question, **kwargs)