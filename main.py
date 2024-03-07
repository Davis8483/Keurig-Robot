import subprocess
import sys
import os
import time
subprocess.run(["pip", "install", "-r", "requirements.txt"])

import coffee_payment
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import *
from PIL.ImageQt import ImageQt

##Example code for loading qr code supplied by coffee_payment.Stripe()
#qim = ImageQt(your_qr_code)
#pix = QPixmap.fromImage(qim

class stackedExample(QWidget):

    def __init__(self):
        super(stackedExample, self).__init__()
            
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

        start_label = QLabel("Tap to start...")
        start_label.setStyleSheet('''
                                    font-size: 50px;
                                    color: #091236;
                                  ''')

        layout.addWidget(start_label)
        layout.setAlignment(Qt.AlignmentFlag.AlignAbsolute)

        self.stack1.setLayout(layout)
		
    def stack2UI(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        sidebar_layout.setSpacing(20)
        sidebar_layout.setContentsMargins(20, 20, 20, 30)

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
                                    font-size: 20px;
                                    min-width: 300px;
                                    height: 40px;
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

        sidebar_layout.addWidget(pay_button, 0, Qt.AlignmentFlag.AlignCenter)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setStyleSheet('''
                                    QWidget{
                                        background: #202020;
                                    }
                                    ''')

        product_slider = DraggableScrollArea()
        # product_slider.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # product_slider.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        product_slider.setAlignment(Qt.AlignmentFlag.AlignCenter)
        product_slider.setFrameShape(QFrame.Shape.NoFrame)
        product_slider.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        def set_payment_view(show:bool=False) -> None:
            "When show is True, the payment qr code will slide into view"

            # disable butotn
            pay_button.clicked.disconnect()

            if show:
                # save the product section width so we can revert back to this later
                self.product_shown_width = product_slider.width()
            
            def timer_callback():
                # use a porabola to ease the sliding animation
                increment = int(0.005 * (self.product_view_x ** 2))

                if show:
                    new_width = product_slider.width() - increment
                    if new_width <= 0:
                        # we're close enough, jump to the end
                        product_slider.setFixedWidth(0)

                        # stop the animation event timer
                        self.timer.stop()

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=False))
                        pay_button.setText("Back")
                        pay_button.setStyleSheet('''
                                                QPushButton{
                                                    font-size: 20px;
                                                    min-width: 300px;
                                                    height: 40px;
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

                        product_name_label.hide()   
                    
                    else:
                        product_slider.setFixedWidth(new_width)
                else:
                    new_width = product_slider.width() + increment
                    if new_width >= self.product_shown_width:
                        # we're close enough, jump to the end
                        product_slider.setFixedWidth(self.product_shown_width)

                        # stop the animation event timer
                        self.timer.stop()

                        # change button properties
                        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))
                        pay_button.setText("Pay")
                        pay_button.setStyleSheet('''
                                                QPushButton{
                                                    font-size: 20px;
                                                    min-width: 300px;
                                                    height: 40px;
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
                        product_name_label.show()   
                    
                    else:
                        product_slider.setFixedWidth(new_width)


                self.product_view_x += 1

            self.timer=QTimer()
            self.timer.timeout.connect(timer_callback)

            self.product_view_x = 0
            self.timer.start(5)
        
        pay_button.clicked.connect(lambda *_: set_payment_view(show=True))
        
        product_layout = QHBoxLayout()
        product_layout.setSpacing(30)
        product_layout.setContentsMargins(30, 30, 30, 30)

        for index in range(5):
            new_product = QLabel()
            new_product.setPixmap(QPixmap('placeholder.png').scaledToHeight(500))

            product_layout.addWidget(new_product)

        scroll_widget = QWidget()
        scroll_widget.setLayout(product_layout)

        product_slider.setWidget(scroll_widget)

        layout.addWidget(product_slider)
        layout.addWidget(sidebar_widget)
        
        self.stack2.setLayout(layout)

    def keyPressEvent(self, e):  
        if e.key() == Qt.Key.Key_Escape:
            self.close()

    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if self.Stack.currentWidget() == self.stack1:
            self.Stack.setCurrentWidget(self.stack2)

class DraggableScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidgetResizable(True)  # Allow resizing of scroll area content
        self.last_drag_pos = None

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.last_drag_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_drag_pos is not None:
            delta = event.pos() - self.last_drag_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.last_drag_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.last_drag_pos = None

def main():
    app = QApplication(sys.argv)
    ex = stackedExample()
    sys.exit(app.exec())
	
if __name__ == '__main__':
    main()