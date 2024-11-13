from smartbook.booking.prompts import (
    BOOKER_ROLE,
    BOOKER_SYSTEM_MSG,
    ROOM_RANKING_PROMPT,
    ROOM_RANKING_EXAMPLE,
)
from smartbook.role import Role
from smartbook.utils import extract_json_from_string
from smartbook.data import Data
import os
import json
import time

class Booker(Role):
    bot_id="room_booker"
    
    def __init__(self, model, **kwargs):
        super().__init__(model, **kwargs)
        # self.context_token_length = self.model.token_length(self.format_context("",main_character=""))
        self.role = "booker"
    

    def book(self, data_fetcher: Data, user_request):

        data = data_fetcher.collect_data()

        prompt = ROOM_RANKING_PROMPT.format(user_request=user_request, room_data=data, example=ROOM_RANKING_EXAMPLE)
        
        new_chat = True

        response = self.model(prompt, new_chat=new_chat, bot_id=self.bot_id, system_msg=BOOKER_ROLE + BOOKER_SYSTEM_MSG)

        room_rank_json = extract_json_from_string(response)
        return room_rank_json


        








