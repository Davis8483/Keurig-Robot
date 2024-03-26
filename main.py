import subprocess
import sys
import os
import time
import urllib.request
import traceback

subprocess.run(["pip", "install", "-r", "requirements.txt"])

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PIL.ImageQt import ImageQt
from coffee_payment import Stripe
from coffee_logging import Notifications
from stripe import Product
import qrcode
import commentjson

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

def getStylesheet(name:str, transformationName:str=None) -> str:
    '''
    Returns the stylesheet for the specified widget stored in config.json

    Parameters:
        `name`: The name of the stylesheet in config.json
        `transformationName`: The trasformation name to apply over the default stylesheet
    '''
    # load style for param:name
    stylesheet:dict = getConfig()["ui"]["stylesheets"][name]

    # applly transformation to default style
    if (transformationName != None) and ("transformations" in stylesheet.keys()):

        transformation:dict = stylesheet["transformations"][transformationName]

        for style in transformation.keys():
            stylesheet[style] = transformation[style]

        # now delete transformation key
        stylesheet.pop("transformations")

    # format data into a string thats readable by the pyqt6
    stylesheet_str = ""
    for style in stylesheet.keys():
        stylesheet_str += f"{style}: {stylesheet[style]};\n"

    return stylesheet_str

# used to send error and status notifications through discord
discord_logging = Notifications(url=getConfig()["logging"]["discord_webhook_url"],
                                allowedNotifications=getConfig()["logging"]["notifications"])

class coffeeUI(QWidget):

    def __init__(self):
        super(coffeeUI, self).__init__()

        self.payment_handler = Stripe(getConfig()["stripe"]["api_key"], discord_logging)
            
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
            
        self.makeStartUI(self.stack1)
        self.makeProductsUI(self.stack2)
        self.makeDispensingUI(self.stack3)
            
        self.Stack = QStackedLayout(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        self.setLayout(self.Stack)
        self.showFullScreen()
        self.show()

        discord_logging.initialized()

    def makeStartUI(self, widget:QWidget):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        video_widget = QVideoWidget()

        # create background video
        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile(getAssetPath("start_menu_video")))
        self.player.setVideoOutput(video_widget)
        video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        # enable autoplay and looping
        self.player.play()
        self.player.setLoops(-1)

        start_label = QLabel("Tap to start...")
        start_label.setStyleSheet(getStylesheet("start_label"))
        
        bar_layout = QVBoxLayout()
        bar_layout.addWidget(start_label)
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom_bar_widget = QWidget()
        bottom_bar_widget.setLayout(bar_layout)
        bottom_bar_widget.setFixedHeight(100)
        bottom_bar_widget.setStyleSheet(getStylesheet("bottom_bar_widget"))

        layout.addWidget(video_widget)
        layout.addWidget(bottom_bar_widget)

        widget.setLayout(layout)
        
    def makeProductsUI(self, widget:QWidget):

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
        product_name_label.setStyleSheet(getStylesheet("product_name_label"))
        
        sidebar_layout.addWidget(product_name_label, 0, Qt.AlignmentFlag.AlignCenter)

        pay_button = QPushButton("Pay")
        pay_button.setStyleSheet(getStylesheet("pay_button", transformationName="pay"))

        sidebar_layout.addWidget(pay_button)

        # use a widget to store the sidebar layout so we can set a styelsheet
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(sidebar_layout)
        self.sidebar_widget.setStyleSheet(getStylesheet("sidebar_widget"))
        
        self.selected_product = Product()
        def product_selected(product: Product) -> None:
            self.selected_product = product

            # change item name
            product_name_label.setText(self.selected_product.name)

            # check if product is in stock
            if self.selected_product.active:
                pay_button.setText("Pay")
                pay_button.setStyleSheet(getStylesheet("pay_button", transformationName="pay"))
                pay_button.setDisabled(False)
            
            else:
                pay_button.setText("Out of Stock")
                pay_button.setStyleSheet(getStylesheet("pay_button", transformationName="out_of_stock"))
                pay_button.setDisabled(True)


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
            
            # continualy checks if payment is complete, then redirects to next screen
            def poll_payment():
                if self.payment_handler.isPaymentComplete():
                    # hide the payment view for next transaction
                    set_payment_view(show=False)

                    # use a timer to allow payment view to finnish hiding before showing next stack item
                    def payment_complete():
                        self.Stack.setCurrentWidget(self.stack3)

                    self.complete_timer = QTimer()
                    self.complete_timer.timeout.connect(payment_complete)
                    self.complete_timer.setSingleShot(True)
                    self.complete_timer.start()

                    # return back to start menu after 5 seconds
                    def return_to_start():
                        self.Stack.setCurrentWidget(self.stack1)

                    self.return_timer = QTimer()
                    self.return_timer.timeout.connect(return_to_start)
                    self.return_timer.setSingleShot(True)
                    self.return_timer.start(5000)

                    self.payment_timer.stop()

            self.payment_timer = QTimer()
            self.payment_timer.timeout.connect(poll_payment)

            def animate_sidebar():
                # use a porabola to ease the sliding animation
                increment = int(0.005 * (self.product_view_x ** 2))

                if show:
                    new_width = self.product_slider.width() - increment
                    if new_width <= 0:
                        # we're close enough, jump to the end
                        self.product_slider.setFixedWidth(0)

                        # stop the animation event timer
                        self.sidebar_timer.stop()

                        # listen for payment
                        self.payment_timer.start(1000)

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=False))
                        pay_button.setText("Back")
                        pay_button.setStyleSheet(getStylesheet("pay_button", transformationName="back"))
                        
                        # set placeholder and show it
                        pay_qr_image.setPixmap(QPixmap(getAssetPath("qr_placeholder_image")).scaledToHeight(400))
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
                        self.sidebar_timer.stop()
                        
                        # stop listening for payment
                        self.payment_timer.stop()

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))
                        pay_button.setText("Pay")
                        pay_button.setStyleSheet(getStylesheet("pay_button", transformationName="pay"))
                    
                    else:
                        self.product_slider.setFixedWidth(new_width)


                self.product_view_x += 1

            self.sidebar_timer=QTimer()
            self.sidebar_timer.timeout.connect(animate_sidebar)

            self.product_view_x = 0
            self.sidebar_timer.start(5)
        
        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))

        layout.addWidget(self.product_slider)
        layout.addWidget(self.sidebar_widget)
        
        widget.setLayout(layout)

    def makeDispensingUI(self, widget:QWidget):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        successful_label = QLabel("Payment successful...")
        successful_label.setStyleSheet(getStylesheet("successful_label"))
        layout.addWidget(successful_label)

        widget.setLayout(layout)

    def keyPressEvent(self, e):  
        if e.key() == Qt.Key.Key_Escape:
            self.close()

    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if self.Stack.currentWidget() == self.stack1:
            
            # update products from the stripe API
            self.product_slider.refreshProducts()

            self.Stack.setCurrentWidget(self.stack2)

            # make sure a product is centered in the scroll area
            self.product_slider.setCurrentProduct(0)

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
        self.scroll_widget.setStyleSheet(getStylesheet("scroll_widget"))

        self.setWidget(self.scroll_widget)

        # hide horizontal scroll bar while maintaining scroll functionality
        self.horizontalScrollBar().setStyleSheet("height: 1px;")

        # disable vertical scroll bar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # disable frame
        self.setFrameShape(QFrame.Shape.NoFrame)

    def setProducts(self, products: list[Product]) -> None:
        '''
        Sets products and loads their respective images from the Stripe api

        Parameters:
            `products`: A list of stripe products
        '''

        self.products = products
        self.product_widgets = []

        for index in products:

            new_widget = QLabel()

            # set to placeholder if image isn't found
            if len(index.images) == 0:
                pixmap = QPixmap(getAssetPath("placeholder_image"))
            
            else:
                # load image from url specified on stripe product page
                with urllib.request.urlopen(index.images[0]) as url:
                    data = url.read()

                pixmap = QPixmap()
                pixmap.loadFromData(data)

            new_widget.setPixmap(pixmap.scaled(self.product_image_size, self.product_image_size))

            self.product_layout.addWidget(new_widget)
            self.product_widgets.append(new_widget)

    def refreshProducts(self) -> None:
        '''
        Refreshes the current products from the strip API
        '''

        # loop through all products and refresh them using the API
        for product in self.products:
            product.refresh()

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
    
    def setFocusedProduct(self, index:int) -> None:
        '''
        Greys out all products besides the one at the specified index
        
        Parameters:
            `index`: The index to focus
        '''

        # set grayed out item images
        for i in range(len(self.products)):

            opacity_effect = QGraphicsOpacityEffect()

            if i == index:
                # Create the opacity effect
                opacity_effect.setOpacity(1.0)  # Set desired opacity (0.0 - fully transparent, 1.0 - opaque)

            else:
                opacity_effect.setOpacity(0.3)

            # Apply the effect to the widget
            self.product_widgets[i].setGraphicsEffect(opacity_effect)

    def setCurrentProduct(self, index:int) -> None:
        '''
        Scrolls the product slider to the specified product index
        
        Parameters:
            `index`: The product index to center on
        '''

        widget_spacing = self.product_image_size + self.product_image_spacing

        # Calculate potential snap positions (centers of each widget)
        snap_positions = [(i * widget_spacing) + ((self.width() + self.product_image_size) / 2) for i in range(len(self.products))]

        def timer_callback():
            new_pos = int((self.horizontalScrollBar().sliderPosition() - snap_positions[index]) / 10)

            if new_pos == 0:
                # stop animation
                self.timer.stop()

                # emit selected product
                self.selected.emit(self.products[index])

            else:
                # ease slider to the closest snap position
                self.horizontalScrollBar().setSliderPosition(self.horizontalScrollBar().sliderPosition() - new_pos)

        # animate sliding to the product
        self.timer = QTimer()
        self.timer.timeout.connect(timer_callback)
        self.timer.start(5)

        self.setFocusedProduct(index)

    def mouseReleaseEvent(self, *kwargs) -> None:
        '''
        Centers the slider on the closest widget when the user releases it
        '''

        # Get slider position and widget size
        slider_pos = self.horizontalScrollBar().sliderPosition()

        widget_spacing = self.product_image_size + self.product_image_spacing

        # Calculate potential snap positions (centers of each widget)
        snap_positions = [(i * widget_spacing) + ((self.width() + self.product_image_size) / 2) for i in range(len(self.products))]

        # Find the closest snap position based on current slider position
        closest_snap_pos = min(snap_positions, key=lambda pos: abs(pos - slider_pos))

        current_product_index = snap_positions.index(closest_snap_pos)
        
        self.setCurrentProduct(current_product_index)

        # Clear last drag position (optional for potential future use)
        self.last_drag_pos = None

def error_handler(etype, value, tb):
    '''
    Handles thrown exceptions
    '''

    error_msg = ''.join(traceback.format_exception(etype, value, tb))

    # requires an internet connection
    try:
        # send an error message on discord
        discord_logging.unexpectedError(error_msg)

    except:
        pass

    # spawn a new instance of the progarm
    process = QProcess()
    process.startDetached("python", sys.argv)

    # stop current instance
    exit()

def check_internet_connection() -> bool:
    '''
    Returns if the host device has an internet connection.
    '''

    try:
        urllib.request.urlopen("https://google.com", timeout=5)
        return True
    
    except:
        return False


def main():
    sys.excepthook = error_handler  # redirect std error

    # wait for internet connection
    while not check_internet_connection():
        print("no internet")
        time.sleep(1)

    # start application
    app = QApplication(sys.argv)
    ex = coffeeUI()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()