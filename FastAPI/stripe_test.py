import stripe
import qrcode
import time
import commentjson


with open("config.jsonc", "r") as config_file:  # Open in read mode
  stripe.api_key = commentjson.load(config_file)["stripe"]["api_key"]  # Load data from the opened file

product = stripe.Product.list().data[0]

# checkout = stripe.checkout.Session.create(
#   success_url="https://stripe.com",
#   line_items=[{"quantity": 1, "price": f"{product.default_price}"}],
#   mode="payment"
# )

link = stripe.PaymentLink.create(
    restrictions={"completed_sessions": {"limit": 1}},
    line_items=[{"price": f"{product.default_price}", "quantity": 1}]
)

print(link.url)
qr = qrcode.make(link.url)
qr.save("test.png")

while True:
    
    # retrieve the last 10 events
    for event in stripe.Event.list(limit=10):

      # check if event originates from the payment link
      if event.type=="checkout.session.completed" and event.data.object.payment_link==link.id:
        print("payment successful")
    
    time.sleep(1)