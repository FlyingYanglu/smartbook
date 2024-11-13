from smartbook.booking.prompts import (
    BOOKER_ROLE,
    BOOKER_SYSTEM_MSG,
    ROOM_RANKING_PROMPT,
    ROOM_RANKING_EXAMPLE,
)
from smartbook.role import Role
from smartbook.utils import extract_json_from_string
import os
import json
import time

class Booker(Role):
    bot_id="booker"
    
    def __init__(self, model, **kwargs):
        super().__init__(model, **kwargs)
        # self.context_token_length = self.model.token_length(self.format_context("",main_character=""))
        self.role = "booker"
    

    def Book(self, data_fetcher, user_request):

        data = data_fetcher.query_data()

        








