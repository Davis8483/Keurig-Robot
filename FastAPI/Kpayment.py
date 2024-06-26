import stripe
import commentjson
from Knotifications import Notifications

class Stripe():
    def __init__(self, apiKey:str, logging:Notifications) -> None:
        '''
        Parameters:
            `api_key`: Your stripe api key, https://dashboard.stripe.com/apikeys
        '''
        self.logging = logging
        stripe.api_key = apiKey

    def getPaymentLink(self, productID: str) -> str:
        '''
        Creates a payment link for the specified product using the default price.
        If a default price does not exist then one will be created for $0.00

        Parameters:
            `productID`: The stripe product to generate a payment link for
        '''
        # disable last payment link before creating a new one
        self.disableLastPaymentLink()

        # grab product from id
        product = stripe.Product.retrieve(productID)
        
        # create a new payment link
        self.payment_link = stripe.PaymentLink.create(restrictions={"completed_sessions": {"limit": 1}},
                                         line_items=[{"price": f"{product.default_price}", "quantity": 1}],
                                         allow_promotion_codes=True)
        
        return self.payment_link.url
        
    def disableLastPaymentLink(self) -> None:
        '''
        Disables the last payment link that was created using `getPaymentLink()`
        '''

        # check if a payment link has been created yet
        if hasattr(self, "payment_link"):
            # disable the payment link
            stripe.PaymentLink.modify(self.payment_link.id,
                                      active=False)
        
    def isPaymentComplete(self) -> bool:
        '''
        Returns a boolean indicating if the payment has been completed
        '''
                
        # retrieve the last 10 events
        for event in stripe.Event.list(limit=20):

            # check if event originates from the payment link
            if event.type=="checkout.session.completed" and event.data.object.payment_link==self.payment_link.id:
                return True
            
        return False
    
    def getPrice(self, priceID: str) -> float:
        priceCents = stripe.Price.retrieve(priceID).unit_amount
        return float(priceCents/100 or 0)
    
    def getProducts(self, numSlots: int) -> list[stripe.Product]:
        '''
        Returns a list of products pulled from stripe.
        All products must have the metadata of `vending_slot` to be set to an int.
        If the specified vending slot is not found, a new placholder product will be created.

        Parameters:
            `numSlots`: The number of products to be fetched to populate your machines kpod slots
        '''
        
        products_list: list[stripe.Product] = []

        # populate machines vending slots with items
        for slot in range(numSlots):

            # cycle through products until a slot canidate is found
            for product in stripe.Product.list().data:
                if "vending_slot" in product.metadata.keys() and product.metadata["vending_slot"] == str(slot):

                    # check if item has a default price, if not set one
                    if product.default_price == None:
                        # create a placeholder price of $0.00
                        price = stripe.Price.create(product=product.id,
                                                    unit_amount=0,
                                                    currency="usd")
                        
                        # set default as the placeholder
                        stripe.Product.modify(product.id,
                                            default_price=price.id)
                        
                        self.logging.priceCreated(product=product.name,
                                                  slot=slot,
                                                  price=0)
                        
                    products_list.append(product)
                    break

            # slot was not filled, populate with a new product
            if (len(products_list) - 1) < slot:
                product = stripe.Product.create(name=f"Slot {slot} Placeholder",
                                                active=False,
                                                metadata={"vending_slot":slot},
                                                default_price_data={"currency": "usd", "unit_amount": 0})
                self.logging.productCreated(slot)
                products_list.append(product)
                
        return products_list

if __name__ == '__main__':

    with open("config.jsonc", "r") as config_file:  # Open in read mode
        api_key = commentjson.load(config_file)["stripe"]["api_key"]  # Load data from the opened file

    payment_handler = Stripe(api_key)

    for product in payment_handler.getProducts(5):
        print(product.name)