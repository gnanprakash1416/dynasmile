import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QSize,pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from library.smoother import lognormal_map_values,moving_average,smooth_and_preserve_extrema,map_to_color
class EmotionSlider(QSlider):
    sliderReleasedSignal = pyqtSignal()
    def __init__(self, scores, orientation, parent=None):
        super().__init__(orientation, parent)
        self.scores = scores  # List of emotion scores for each frame
        self.setFixedHeight(30)  # Set fixed height for the slider
        self.setMinimum(0)
        self.setMaximum(len(self.scores) - 1)
        #self.installEventFilter(self)
        self.location=0
        self.colors=[]
        #self.valueChanged.connect(self.on_value_changed)
    
    def on_value_changed(self, value):
        # 在值改变时自动重绘滑块
        self.location=value
        #print(f"on_value_changed called.Now the location is {self.location}")
        self.update()
        
    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress or event.type() == event.MouseMove:
            pass
            #print(f"Mouse event {event.type()} detected in {source}")
        return super().eventFilter(source, event)
    def paintEvent(self, event):
        painter = QPainter(self)
        # Enable anti-aliasing for smoother edges
        painter.setRenderHint(QPainter.Antialiasing)
        # Calculate the width for each frame
        num_frames = len(self.scores)
        frame_width = self.width() / (num_frames - 1)
        # Get colors for each frame
        colors = self.colors if self.colors else self.get_colors()
        # Draw gradient background (rounded rectangle)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        for i, color in enumerate(colors):
            gradient.setColorAt(i / (num_frames - 1), QColor(*color))
        painter.setBrush(gradient)
        # Draw the background as a rounded rectangle
        border_radius = 15
        painter.drawRoundedRect(0, 0, self.width(), self.height(), border_radius, border_radius)
        # Draw the rounded border of the slider
        painter.setPen(QColor(200, 200, 200))  # Gray border
        painter.drawRoundedRect(0, 0, self.width(), self.height(), border_radius, border_radius)
        # Draw the custom slider (as a circular handle)
        thumb_position = self.location * (self.width() / (num_frames - 1))
        #print("location from TEST_SLIDING: "+str(self.location))
        #print(f"Paintevent is called. The thumb_position is {thumb_position}")
        thumb_radius = 15  # Radius of the slider handle
        painter.setBrush(QColor(255, 255, 255))  # White slider handle
        painter.drawEllipse(thumb_position - thumb_radius, (self.height() - thumb_radius * 2) / 2, thumb_radius * 2, thumb_radius * 2)
    def get_colors(self):
        # Color mapping function
        color_scale = [(1, 1, 1),  # White
                       (102 / 255, 204 / 255, 102 / 255)]  # RGB(102, 204, 102)
        colors = map_to_color(self.scores, color_scale)
        self.colors = [tuple(i) for i in colors[:, :3]]  # Store colors
        return self.colors
    def sizeHint(self):
        return QSize(400, 30)  # Set the preferred size for the slider
    def update_scores(self, new_scores):
        self.scores = new_scores  # Update the emotion scores
        mapped_score=lognormal_map_values(self.scores, mu=0, sigma=1)
        smoothed_score=moving_average(mapped_score, window_size=5)
        final_smoothed_score = smooth_and_preserve_extrema(mapped_score, smoothed_score)
        self.scores = final_smoothed_score
        self.colors = []  # Reset colors to force recalculation on the next draw
        self.get_colors()  # Update colors based on new scores
        self.update()  # Redraw the slider
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.update_slider_position(event.pos())
        super().mousePressEvent(event)  # Ensure the base class event is called to retain event handling
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            # 发出自定义信号
            self.sliderReleasedSignal.emit()
        super().mouseReleaseEvent(event)
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_slider_position(event.pos())
        super().mouseMoveEvent(event)  # Ensure the base class event is called
    
    def update_slider_position(self, pos):
        # Ensure position is within the slider range
        if pos.x() < 0:
            pos.setX(0)
        elif pos.x() > self.width():
            pos.setX(self.width())
        # Calculate slider position based on mouse position
        value = int((pos.x() / self.width()) * (len(self.scores) - 1))
        #self.setSliderPosition(value)  # Update the slider position
        self.location=value
        #print(f"The value is now changing in UPDATE_SLIDER_POSITION.The value is {value}")
        #print(self.sliderPosition())
        self.update()  # Redraw the slider
        #self.valueChanged.emit(value)  # Emit value changed signal
class EmotionVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Visualization Slider")
        self.setGeometry(100, 100, 600, 200)
        # Initial emotion scores (modifiable as needed)
        self.scores = [20, 50, 70, 90, 30, 40, 80, 60, 110, 30]
        # Create central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        # Create custom emotion slider
        self.emotion_slider = EmotionSlider(self.scores, Qt.Horizontal)
        self.emotion_slider.valueChanged.connect(self.update_label)
        #self.emotion_slider.setEnabled(False)
        # Create label to display current frame and score
        self.frame_label = QLabel()
        self.update_label(self.emotion_slider.value())
        # Add widgets to layout
        self.layout.addWidget(self.emotion_slider)
        self.layout.addWidget(self.frame_label)
        # Set central widget
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        # Example: Dynamic score updates
        self.update_scores_example()
    def update_scores_example(self):
        # Simulate updating emotion scores
        new_scores = [10, 80, 90, 60, 40, 20, 100, 30, 50, 70]
        self.emotion_slider.update_scores(new_scores)  # Update slider scores
    def update_label(self, value):
        # Get the emotion score for the currently selected frame
        score = self.scores[value]
        self.frame_label.setText(f"Current Frame: {value + 1}, Emotion Score: {score}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = EmotionVisualizer()
    main_window.show()
    sys.exit(app.exec_())