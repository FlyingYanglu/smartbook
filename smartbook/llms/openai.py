from openai import OpenAI
from smartbook.llms.base import BaseLLM
from smartbook.utils import load_config
from smartbook.configs import CONFIG

class GPT(BaseLLM):
    def __init__(self, **kwargs):
        self.api_key = CONFIG["openai"]["api_key"]
        self.engine = kwargs.get("engine", "text-davinci-003")
        self.openai = OpenAI(self.api_key)
