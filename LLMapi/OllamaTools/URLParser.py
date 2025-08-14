from LLMapi.iOllamaTool import OllamaTool
from dataclasses import dataclass
from newspaper import Article

@dataclass
class UrlParser(OllamaTool):
    def _main(self, **kwargs):
        try:
            article = Article(kwargs['url'])
            article.download()
            article.parse()
            return {
                "title": article.title,
                "text": article.text,
                "url": kwargs['url']
            }
        except Exception as e:
            return {"error": f"Failed to parse URL: {str(e)}", "url": kwargs['url']}