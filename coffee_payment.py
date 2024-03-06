import stripe
import qrcode
import time

qrcode.make

class Stripe():
    def __init__(self, api_key:str) -> None:
        '''
        Parameters:
            api_key - Your stripe api key, https://dashboard.stripe.com/apikeys
        '''
        stripe.api_key = api_key
