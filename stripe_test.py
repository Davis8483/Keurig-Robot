
import stripe
import time

stripe.api_key = "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"

product = stripe.Product.list().data[0]
print(product)

checkout = stripe.checkout.Session.create(
  success_url="https://example.com/success",
  line_items=[{"quantity": 1, "price": f"{product.default_price}"}],
  mode="payment"
)

print(checkout.url)

while True:
    # update checkout session from api
    checkout = stripe.checkout.Session.retrieve(id=checkout.id)

    # check status of the checkout
    print(checkout.payment_status)
    
    time.sleep(1)