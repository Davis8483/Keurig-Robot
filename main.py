import subprocess
import sys
import threading
subprocess.run(["pip", "install", "-r", "requirements.txt"])

import coffee_payment
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from PIL.ImageQt import ImageQt

venmo_payment = coffee_payment.Venmo(username="Noah-Davis-244", 
                                    password="YdU671IYaT!!OKC")

test = venmo_payment.payment_qr(amount=0.01,
                                note="Coffee Test")
def myThread():
    print("waiting for payment")
    venmo_payment.wait_for_payment(False)

t = threading.Thread(target=myThread)
t.start()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image")
        self.setGeometry(0, 0, 400, 300)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(central_widget)

        # Assuming 'test' is your QR code image
        # Convert it to a QPixmap
        qim = ImageQt(test)
        pix = QPixmap.fromImage(qim)

        # Create the image label
        self.label = QLabel(self)
        self.label.setPixmap(pix.scaled(300, 300))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set alignment to center

        # Add the image label to the layout
        layout.addWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())