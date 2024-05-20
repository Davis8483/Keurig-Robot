import traceback

from Kpayment import Stripe
from Knotifications import Notifications
from stripe import Product
import commentjson
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List

def getConfig() -> dict:
    "Returns the dictionary stored in config.json"

    with open("FastAPI/config.jsonc", "r") as config_file:  # Open in read mode
        config = commentjson.load(config_file)  # Load data from the opened file

    return config

# used to send error and status notifications through discord
discord_logging = Notifications(url=getConfig()["logging"]["discord_webhook_url"],
                                allowedNotifications=getConfig()["logging"]["notifications"])

payment_handler = Stripe(getConfig()["stripe"]["api_key"], discord_logging)


# initialize api
app = FastAPI(
    title="K-Bot API",
    description="Here you can find a list of methods utilized by React to interact with your Keurig Robot",
    version="1.0.0"
    )

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=origins
)

class Kpod(BaseModel):
    id: str
    name: str
    description: str = ""
    price: float
    image_url: str
    in_stock: bool

@app.get("/products/", tags=["Products"])
async def get_products() -> List[Kpod]:
    '''
    Returns a list of Kpods that are being sold by your machine
    '''

    products: List[Product] = payment_handler.getProducts(getConfig()["hardware"]["vending_slots"])

    data = []

    for index in products:
        data.append(
            Kpod(
                id=index.id,
                name=index.name,
                description=index.description or "",
                price=payment_handler.getPrice(index.default_price),
                image_url=index.images[0],
                in_stock=index.active
            )
        )

    return data

@app.put("/products/select/", tags=["Products"])
async def select_product(stripeID) -> str:
    '''
    Returns a stripe link used to purchase the specified product
    '''
    return payment_handler.getPaymentLink(stripeID)

@app.exception_handler(Exception)
async def exception_notification(request: Request, exc: Exception):
    exc_msg = traceback.format_exception(exc)

    # only return last error paragraph
    discord_logging.unexpectedError("".join(exc_msg[-5:]))

if __name__ == '__main__':
    discord_logging.initialized()
    uvicorn.run("main:app", reload=True)