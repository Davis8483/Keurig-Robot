from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class AnimatedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = 0  # Offset for animation

        # Set initial background color
        self.setAutoFillBackground(True)

        # Create timer and connect it to the update function
        self.timer = QTimer(self)
        self.timer.setInterval(10)  # Update every 10 milliseconds
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Get widget width and height
        width = self.width()
        height = self.height()

        # Create a vertical gradient with red at the top and blue at the bottom
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor(255, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 0, 255))
        gradient.setColorAt(1.0, QColor(0, 0, 255))

        # Set the painter brush to the gradient
        painter.setBrush(gradient)

        # Draw a rectangle to fill the widget with the gradient
        painter.drawRect(0, 0, width, height)

    def update(self):
        # Update the offset for animation
        self.offset += 1

        # Reset the offset when it reaches the end
        if self.offset >= 100:
            self.offset = 0

        # Update the widget to show the changes
        self.repaint()

if __name__ == '__main__':
    app = QApplication([])
    widget = AnimatedWidget()
    widget.resize(400, 300)  # Set the widget size
    widget.show()
    app.exec()
