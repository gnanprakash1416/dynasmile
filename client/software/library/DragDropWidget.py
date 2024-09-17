from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
class DragDropWidget(QWidget):
    itemDropped = pyqtSignal(str)
    current_path=os.path.abspath(__file__)
    current_folder=os.path.dirname(current_path)

    def __init__(self):
        super(DragDropWidget, self).__init__()
        # Set up the layout
        self.layout = QVBoxLayout()
        # Create a label to display the file path
        self.label = QLabel("Please drag and drop a file here\nor click the button below.", self)
        self.label.setAlignment(Qt.AlignCenter)  # Center align the label
        self.layout.addWidget(self.label)  # Add the label to the layout
        # Create a label to display the cross icon
        self.cross_image_label = QLabel(self)
        self.cross_image_label.setAlignment(Qt.AlignCenter)  # Center align the image label
        # Load the cross icon and set its size
        self.cross_image = QPixmap(os.path.join(self.current_folder,"upload_button.png")).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cross_image_label.setPixmap(self.cross_image)  # Set the image to the label
        self.layout.addWidget(self.cross_image_label)  # Add the image label to the layout
        # Set the layout to the widget
        self.setLayout(self.layout)
        # Allow the widget to accept drag-and-drop events
        self.setAcceptDrops(True)
        # Flag to indicate if a correct file has been selected
        self.file_selected = False
        # Bind mouse click event on the cross icon to open a file dialog
        self.cross_image_label.mousePressEvent = self.openFileDialog

        self.media=None
    def dragEnterEvent(self, event):
        # Check if the dragged contents are files
        if event.mimeData().hasUrls():
            event.accept()  # Accept the drag event
            print("Right")  
        else:
            print("Not")
            event.ignore()  # Ignore if it's not a file
    def dropEvent(self, event):
        self.disableDragDrop()  # Disable further drag-and-drop
        self.cross_image_label.hide()
        # Get the file paths of the dragged files
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        if file_paths:
            # Process the first file path
            self.processFile(file_paths[0])
    def processFile(self, file_path):
        # Check the file format (example: .txt)
        if file_path.endswith('.mp4'):
            self.cross_image_label.hide()
            self.media=file_path
            self.label.setText("Dropped file")  # Display the dropped file path
            self.label.setStyleSheet("color: gray;")  # Change label color
            self.file_selected = True  # Mark file as selected
            self.itemDropped.emit(self.media)
        else:
            self.label.setText("Please select a .mp4 file")  # Prompt user to select a correct file
            self.label.setStyleSheet("color: black;")  # Reset label color
            self.file_selected = False  # Mark file as unselected
            self.enableDragDrop()
            self.cross_image_label.show()
    def openFileDialog(self, event):
        # If a correct file is already selected, do nothing
        if self.file_selected:
            return
        # Open a file dialog to select a file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.mp4);;All Files (*)", options=options)
        if file_path:
            self.processFile(file_path)  # Process the chosen file
    def disableDragDrop(self):
        # Disable drag-and-drop functionality
        self.setAcceptDrops(False)  # Prevent further file drops
        self.label.setStyleSheet("color: gray;")  # Change label color
    def enableDragDrop(self):
        # Restore drag-and-drop functionality
        self.setAcceptDrops(True)  # Allow dragging files again
        self.label.setStyleSheet("color: black;")  # Reset label color
        self.file_selected = False  # Reset file selection status
        self.label.setText("Please select a .mp4 file")  # Reset label prompt
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Main Window")  # Set window title
        self.setGeometry(100, 100, 400, 500)  # Set window size and position
        # Create and set the DragDropWidget central widget
        self.drag_drop_widget = DragDropWidget()
        self.setCentralWidget(self.drag_drop_widget)
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    main_window = MainWindow()  # Instantiate the main window
    main_window.show()  # Show the main window
    sys.exit(app.exec_())  # Execute the application