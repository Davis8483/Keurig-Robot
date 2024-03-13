import subprocess
import sys
import os
import time
import urllib.request
import json

subprocess.run(["pip", "install", "-r", "requirements.txt"])

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PIL.ImageQt import ImageQt
from coffee_payment import Stripe
from stripe import Product
import qrcode
##Example code for loading qr code supplied by coffee_payment.Stripe()
#qim = ImageQt(your_qr_code)
#pix = QPixmap.fromImage(qim

def getConfig() -> dict:
    "Returns the dictionary stored in config.json"

    with open("config.json", "r") as config_file:  # Open in read mode
        config = json.load(config_file)  # Load data from the opened file

    return config

class stackedExample(QWidget):

    def __init__(self):
        super(stackedExample, self).__init__()

        self.payment_handler = Stripe(getConfig()["stripe"]["api_key"])
            
        self.stack1 = QWidget()
        self.stack2 = QWidget()
            
        self.stack1UI()
        self.stack2UI()
            
        self.Stack = QStackedLayout (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)

        self.setLayout(self.Stack)
        self.setWindowTitle('StackedWidget demo')
        self.showFullScreen()
        self.show()

        
    def stack1UI(self):
 
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        video_widget = QVideoWidget()

        # create background video
        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile(getConfig()["assets"]["start_menu_video"]["path"]))
        self.player.setVideoOutput(video_widget)
        video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        # enable autoplay and looping
        self.player.play()
        self.player.setLoops(-1)

        start_label = QLabel("Tap to start...")
        start_label.setStyleSheet('''QLabel{
                                        font-size: 40px;
                                        font-weight: bold;
                                        color: #ffffff;
                                    }''')
        
        bar_layout = QVBoxLayout()
        bar_layout.addWidget(start_label)
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom_bar_widget = QWidget()
        bottom_bar_widget.setLayout(bar_layout)
        bottom_bar_widget.setFixedHeight(100)
        bottom_bar_widget.setStyleSheet('''QWidget{
                                                background: #202020;
                                            }
                                            ''')

        layout.addWidget(video_widget)
        layout.addWidget(bottom_bar_widget)
        self.stack1.setLayout(layout)
        
    def stack2UI(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.setSpacing(20)
        sidebar_layout.setContentsMargins(30, 30, 30, 30) 

        sidebar_layout.addStretch()

        pay_qr_image = QLabel()
        pay_qr_image.hide()

        sidebar_layout.addWidget(pay_qr_image)

        sidebar_layout.addStretch()

        
        product_name_label = QLabel("Product Name")
        product_name_label.setStyleSheet('''
                                        QLabel{
                                        font-size: 25px;
                                        font-weight: bold;
                                        color: #ffffff;
                                        }
                                        ''')
        
        sidebar_layout.addWidget(product_name_label, 0, Qt.AlignmentFlag.AlignCenter)

        pay_button = QPushButton("Pay")
        pay_button.setStyleSheet('''
                                QPushButton{
                                    font-size: 25px;
                                    width: 300px;
                                    height: 60px;
                                    color: #ffffff;
                                    padding: 5px 10px;
                                    font-weight: bold;
                                    position: relative;
                                    outline: none;
                                    border-radius: 20px;
                                    border: none;
                                    background: #476ade;
                                }
                                ''')

        sidebar_layout.addWidget(pay_button)

        # use a widget to store the sidebar layout so we can set a styelsheet
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(sidebar_layout)
        self.sidebar_widget.setStyleSheet('''
                                    QWidget{
                                        background: #202020;
                                    }
                                    ''')
        
        self.selected_product = Product()
        def product_selected(product: Product) -> None:
            # change item name
            product_name_label.setText(product.name)

            self.selected_product = product

        self.product_slider = ProductSelection()
        self.product_slider.setProducts(self.payment_handler.getProducts(getConfig()["hardware"]["vending_slots"]))
        self.product_slider.selected.connect(product_selected)

        def set_payment_view(show:bool=False) -> None:
            "When show is True, the payment qr code will slide into view"

            # disable button interactions
            pay_button.clicked.disconnect()

            if show:
                # save the product section width so we can revert back to this later
                self.product_shown_width = self.product_slider.width()
            
            else:
                # disable payment qr
                pay_qr_image.hide()

                # disable payment link
                self.payment_handler.disableLastPaymentLink()

            def timer_callback():
                # use a porabola to ease the sliding animation
                increment = int(0.005 * (self.product_view_x ** 2))

                if show:
                    new_width = self.product_slider.width() - increment
                    if new_width <= 0:
                        # we're close enough, jump to the end
                        self.product_slider.setFixedWidth(0)

                        # stop the animation event timer
                        self.timer.stop()

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=False))
                        pay_button.setText("Back")
                        pay_button.setStyleSheet('''
                                                QPushButton{
                                                    font-size: 25px;
                                                    width: 300px;
                                                    height: 60px;
                                                    color: #ffffff;
                                                    padding: 5px 10px;
                                                    font-weight: bold;
                                                    position: relative;
                                                    outline: none;
                                                    border-radius: 20px;
                                                    border: none;
                                                    background: #de4747;
                                                }
                                                ''')
                        
                        # set placeholder and show it
                        pay_qr_image.setPixmap(QPixmap(getConfig()["assets"]["qr_placeholder_image"]["path"]).scaledToHeight(400))
                        pay_qr_image.show()

                        # load actual qr code, takes about a second
                        def loadQR():
                            qr = qrcode.QRCode(version=1,
                                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                                border=0)
                            qr.add_data(self.payment_handler.getPaymentLink(self.selected_product))
                            qr.make(fit=True)

                            qim = ImageQt(qr.make_image(fill_color="#ffffff", back_color="#202020"))
                            pay_qr_image.setPixmap(QPixmap.fromImage(qim).scaledToHeight(400))
                        
                        # use a timer so animation finnishes before the blocking function, loadQR(), is called
                        self.qr_timer = QTimer()
                        self.qr_timer.timeout.connect(loadQR)
                        self.qr_timer.setSingleShot(True)
                        self.qr_timer.start(10)
                    
                    else:
                        self.product_slider.setFixedWidth(new_width)
                else:
                    new_width = self.product_slider.width() + increment
                    if new_width >= self.product_shown_width:
                        # we're close enough, jump to the end
                        self.product_slider.setFixedWidth(self.product_shown_width)

                        # stop the animation event timer
                        self.timer.stop()

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))
                        pay_button.setText("Pay")
                        pay_button.setStyleSheet('''
                                                QPushButton{
                                                    font-size: 25px;
                                                    width: 300px;
                                                    height: 60px;
                                                    color: #ffffff;
                                                    padding: 5px 10px;
                                                    font-weight: bold;
                                                    position: relative;
                                                    outline: none;
                                                    border-radius: 20px;
                                                    border: none;
                                                    background: #476ade;
                                                }
                                                ''')
                    
                    else:
                        self.product_slider.setFixedWidth(new_width)


                self.product_view_x += 1

            self.timer=QTimer()
            self.timer.timeout.connect(timer_callback)

            self.product_view_x = 0
            self.timer.start(5)
        
        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))

        layout.addWidget(self.product_slider)
        layout.addWidget(self.sidebar_widget)
        
        self.stack2.setLayout(layout)

    def keyPressEvent(self, e):  
        if e.key() == Qt.Key.Key_Escape:
            self.close()

    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if self.Stack.currentWidget() == self.stack1:
            self.Stack.setCurrentWidget(self.stack2)

            # make sure a product is centered in the scroll area
            self.product_slider.mouseReleaseEvent()

class ProductSelection(QScrollArea):
    # define a pyqt signal to be called when a product is selected
    selected = pyqtSignal(Product)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)  # Allow resizing of scroll area content
        self.last_drag_pos = None

        self.product_image_spacing = 100
        self.product_image_size = 500
        self.product_layout = QHBoxLayout()
        self.product_layout.setSpacing(self.product_image_spacing)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.product_layout)
        self.scroll_widget.setStyleSheet('''QWidget{
                                            background-color: #c9c9c5;
                                         }''')

        self.setWidget(self.scroll_widget)

        # hide horizontal scroll bar while maintaining scroll functionality
        self.horizontalScrollBar().setStyleSheet("height: 1px;")

        # disable vertical scroll bar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # disable frame
        self.setFrameShape(QFrame.Shape.NoFrame)

    def setProducts(self, products: list[Product]) -> None:
        self.products = products
        self.product_widgets = []

        for index in products:

            new_widget = QLabel()

            # set to placeholder if image isn't found
            if len(index.images) == 0:
                pixmap = QPixmap(getConfig()["assets"]["placeholder_image"]["path"])
            
            else:
                # load image from url specified on stripe product page
                with urllib.request.urlopen(index.images[0]) as url:
                    data = url.read()

                pixmap = QPixmap()
                pixmap.loadFromData(data)

            new_widget.setPixmap(pixmap.scaled(self.product_image_size, self.product_image_size))

            self.product_layout.addWidget(new_widget)
            self.product_widgets.append(new_widget)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.last_drag_pos = event.pos()

    def mouseMoveEvent(self, event) -> None:
        if self.last_drag_pos is not None:
            delta = event.pos() - self.last_drag_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.last_drag_pos = event.pos()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        
        # # slide products quickly to the left out of view
        # new_width = event.size().width()
        # old_width = event.oldSize().width()
        # scroll_position = self.horizontalScrollBar().sliderPosition()

        # self.horizontalScrollBar().setSliderPosition(scroll_position + (old_width - new_width))

        # set content margins so that products can be scrolled completely out of view
        self.product_layout.setContentsMargins(self.width(), 0, self.width(), 0)

    def mouseReleaseEvent(self, *kwargs) -> None:
        """Centers the slider on the closest widget when the user releases it."""

        # Get slider position and widget size
        slider_pos = self.horizontalScrollBar().sliderPosition()

        widget_spacing = self.product_image_size + self.product_image_spacing

        # Calculate potential snap positions (centers of each widget)
        snap_positions = [(i * widget_spacing) + ((self.width() + self.product_image_size) / 2) for i in range(len(self.products))]

        # Find the closest snap position based on current slider position
        closest_snap_pos = min(snap_positions, key=lambda pos: abs(pos - slider_pos))
        
        def timer_callback():
            new_pos = int((self.horizontalScrollBar().sliderPosition() - closest_snap_pos) / 10)

            if new_pos == 0:
                # stop animation
                self.timer.stop()

                # emit selected product
                self.selected.emit(self.products[self.current_product_index])

            else:
                # ease slider to the closest snap position
                self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().sliderPosition() - new_pos)

        # animate sliding to the product
        self.timer = QTimer()
        self.timer.timeout.connect(timer_callback)
        self.timer.start(5)

        # Clear last drag position (optional for potential future use)
        self.last_drag_pos = None

        # set grayed out item images
        self.current_product_index = snap_positions.index(closest_snap_pos)
        for index in range(len(self.products)):

            opacity_effect = QGraphicsOpacityEffect()

            if index == self.current_product_index:
                # Create the opacity effect
                opacity_effect.setOpacity(1.0)  # Set desired opacity (0.0 - fully transparent, 1.0 - opaque)

            else:
                opacity_effect.setOpacity(0.3)

            # Apply the effect to the widget
            self.product_widgets[index].setGraphicsEffect(opacity_effect)

def main():
    app = QApplication(sys.argv)
    ex = stackedExample()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()