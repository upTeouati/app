import sys
import asyncio
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QWidget, QLabel, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt, QTimer
from screen_capture import ScreenCapture
from stream_server import StreamServer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Screen Sharing")
        self.setMinimumSize(400, 300)
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.stream_server = StreamServer()
        self.is_streaming = False
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel("Status: Not Streaming")
        layout.addWidget(self.status_label)
        
        # Quality settings
        quality_label = QLabel("Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High", "Medium", "Low"])
        layout.addWidget(quality_label)
        layout.addWidget(self.quality_combo)
        
        # FPS settings
        fps_label = QLabel("FPS:")
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(30)
        layout.addWidget(fps_label)
        layout.addWidget(self.fps_spin)
        
        # Stream button
        self.stream_button = QPushButton("Start Streaming")
        self.stream_button.clicked.connect(self.toggle_streaming)
        layout.addWidget(self.stream_button)
        
        # Connection info
        self.connection_label = QLabel("Connection URL will appear here")
        layout.addWidget(self.connection_label)
        
    def toggle_streaming(self):
        if not self.is_streaming:
            # Start streaming
            self.stream_server.start()
            self.screen_capture.start(fps=self.fps_spin.value())
            self.status_label.setText("Status: Streaming")
            self.stream_button.setText("Stop Streaming")
            self.connection_label.setText(f"Connect to: {self.stream_server.get_connection_url()}")
        else:
            # Stop streaming
            self.stream_server.stop()
            self.screen_capture.stop()
            self.status_label.setText("Status: Not Streaming")
            self.stream_button.setText("Start Streaming")
            self.connection_label.setText("Connection URL will appear here")
            
        self.is_streaming = not self.is_streaming

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
