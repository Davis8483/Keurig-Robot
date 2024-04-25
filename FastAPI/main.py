import subprocess
import sys
import os
import time
import urllib.request
import traceback

from coffee_payment import Stripe
from coffee_notifications import Notifications
from stripe import Product
import commentjson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# initialize api
app = FastAPI()

origins = [
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

def getConfig() -> dict:
    "Returns the dictionary stored in config.json"

    with open("config.jsonc", "r") as config_file:  # Open in read mode
        config = commentjson.load(config_file)  # Load data from the opened file

    return config

def getAssetPath(name:str) -> str:
    '''
    Returns the path of a specified asset stored in config.json

    Parameters:
        `name`: The name of the asset in config.json
    '''

    return getConfig()["ui"]["assets"][name]["path"]

# used to send error and status notifications through discord
discord_logging = Notifications(url=getConfig()["logging"]["discord_webhook_url"],
                                allowedNotifications=getConfig()["logging"]["notifications"])
