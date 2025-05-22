"""API executor and starter"""
import time
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

from api.auth import authenticate
from helpers import StringHelper
from logger import LOG
from utils.utils import get_conf

app = FastAPI()
last_warmup_time = time.time()


class Interaction(BaseModel):
    """Interaction Request BaseModel"""

    text: str
    context: dict
    language: str = "tr"



@app.post("/interaction/request", dependencies=[Depends(authenticate)])
async def request(interaction: Interaction, user: str = Depends(authenticate)):
    """Request to the interaction service
    Args:
        interaction: required parameter for interaction
        user: The user's ID.

    Returns: response from interaction
    """
    text = interaction.text
    context = interaction.context
    language = interaction.language
    if not language:
        LOG.error("Language parameter is required and cannot be empty !!")
        raise HTTPException(status_code=400)
    return executor(text=text, context=context, language=language, user=user)


def executor(text: str, context: dict = {}, language: str = "tr", user=None):
    """Get the result from interaction using API

    Args:
        text: requested text to get the result from interaction
        context: intent and slots
        language: text's language
        user: The user's ID.

    Returns:
        disc with interaction response.
    """

    user, groups, sub_version = str(user[1]), user[2], user[3]

    # here your interaction logic or your own logic 
    
    intent, slots, interaction_response = handle_intent_process(
        text, context, language, user, groups, sub_version
    )
   

    LOG.info(f"{intent=} | {slots=} | => {interaction_response=}")
    return {"result": {intent:intent,slots:slots,interaction_response:interaction_response}, "status": True}


def handle_intent_process(
    text: str, context: dict, language: str, user: str, groups: list, sub_version: str
) -> tuple:
    """Handle the intent processing logic.

    Args:
        text: The input text.
        context: The context containing intent and slots.
        language: The language of the text.
        user: User's ID.
        groups: User Groups.
        sub_version: Versions of APIs

    Returns:
        tuple: Tuple containing (intent, slots, interaction_response).
    """
    intent, slots = context.get("intent"), context.get("slots")
    text = StringHelper.remove_special_characters(text)
    interaction_response = "custom logic"
    # Here your logic for process intent
    return intent, slots, interaction_response


def start_api():
    """start api"""
    host = get_conf("HOST")
    port = int(get_conf("PORT"))
    uvicorn.run(app, host=host, port=port)
