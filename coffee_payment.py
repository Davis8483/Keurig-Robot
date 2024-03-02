from venmo_api import Client
from venmo_api import PaymentStatus
import qrcode
import time

class Venmo():
    PAYMENT_BELOW_REQUEST = "Below Request"
    PAYMENT_ACCEPTED = "Accepted"

    def __init__(self, username:str, password:str) -> None:
        self.username = username

        # request an access token from venmo, will require sms authentication
        access_token = Client.get_access_token(username=self.username,
                                               password=password)
        
        # initialize venmo api
        self.venmo = Client(access_token=access_token)

    def payment_qr(self, amount:float, note:str="") -> qrcode.image:
        '''
        Returns a qr code that brings up a payment form to the venmo user

        amount: the amount you want auto filled in the payment request
        note: the note to auto fill on the payment request
        '''

        self.payment_amount = amount

        # a new qr code being generated implies a new payment
        # so clear all previous requests
        self.clear_payments()

        # generate qr code
        venmo_qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )

        note = note.replace(" ", "+")
        venmo_qr.add_data(f"https://venmo.com/payment-link?txn=pay&recipients={self.username}&amount={self.payment_amount}&note={note}")
        venmo_qr.make(fit=True)

        img = venmo_qr.make_image(fill_color="black", back_color="white")

        return img
    
    def wait_for_payment(self, interupt:bool) -> type:
        '''
        Wait until payment is recieved
        Returns either PAYMENT_BELOW_REQUEST or PAYMENT_ACCEPTED
        '''
        while not interupt:
            print(self.venmo.payment.get_pay_payments(limit=10))
            time.sleep(1)
            # self.venmo.payment.cancel_payment
            if len(self.venmo.payment.get_pay_payments(limit=10)) > 0:
                print(self.venmo.payment.__update_payment("approve", self.venmo.payment.get_pay_payments(limit=1)[0]))
        # pay_payments = self.venmo.payment.get_pay_payments(limit=1)
        # if len(pay_payments) == 0:

        # # poll the api until a payment request is recieved
        # payment = pay_payments[0]
        # while not interupt and payment == PaymentStatus.PENDING:
        #     time.sleep(1)

        #     # poll the api
        #     payment = self.venmo.payment.get_pay_payments(limit=1)[0]

        # # check if the payment was the correct ammount
        # if payment.amount >= self.payment_amount:
        #     return Venmo.PAYMENT_ACCEPTED
        # else:
        #     # self.venmo.payment.send_money
        #     return Venmo.PAYMENT_BELOW_REQUEST
    
    def clear_payments(self) -> None:
        '''
        Cycles through all payment reqests and denies them, only one person can check out at a time
        '''
        for requested_payment in self.venmo.payment.get_pay_payments():
            if requested_payment.status == PaymentStatus.PENDING:

                print(f"Canceling request to {requested_payment.target.display_name}, Amount: {requested_payment.amount}")
                self.venmo.payment.cancel_payment(requested_payment)