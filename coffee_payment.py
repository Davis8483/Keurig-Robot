import stripe
import qrcode
import time
import json

class Stripe():
    def __init__(self, apiKey:str) -> None:
        '''
        Parameters:
            api_key - Your stripe api key, https://dashboard.stripe.com/apikeys
        '''
        stripe.api_key = apiKey

    def getProducts(self, numSlots: int) -> list[stripe.Product]:
        '''
        Returns a list of products pulled from stripe.
        All products must have the metadata of "vending_slot" to be set to an int.
        If the specified vending slot is not found, a new placholder product will be created.

        Parameters:
            numSlots - The number of products to be fetched to populate your machines kpod slots
        '''
        
        products = []

        # populate machines vending slots with items
        for slot in range(numSlots):

            # cycle through products until a slot canidate is found
            for product in stripe.Product.list().data:
                if "vending_slot" in product.metadata.keys() and product.metadata["vending_slot"] == str(slot):
                    products.append(product)
                    break

            # slot was not filled, populate with a new product
            if (len(products) - 1) < slot:
                product = stripe.Product.create(name=f"Slot {slot} Placeholder",
                                                active=False,
                                                metadata={"vending_slot":slot})
                products.append(product)
                
        return products

if __name__ == '__main__':

    with open("config.json", "r") as config_file:  # Open in read mode
        api_key = json.load(config_file)["stripe"]["api_key"]  # Load data from the opened file

    payment_handler = Stripe(api_key)

    for product in payment_handler.getProducts(5):
        print(product.name)