from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QWidget,
    QSlider,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from utils.utils import load_json, save_json

class HSVSlider(QWidget):
    slider_values_signal = pyqtSignal(int, int, int, int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Load HSV values from JSON
        try:
            hsv_values = load_json("hsv.json")
        except Exception as e:
            print(e)
            hsv_values = {"hmin": 77, "hmax": 179, "smin": 45, "smax": 255, "vmin": 0, "vmax": 255}

        # Create sliders, labels, and value labels
        self.sliders = {}
        self.labels = {}
        self.value_labels = {}
        self.create_slider("hmin", 0, 179, hsv_values)
        self.create_slider("hmax", 0, 179, hsv_values)
        self.create_slider("smin", 0, 255, hsv_values)
        self.create_slider("smax", 0, 255, hsv_values)
        self.create_slider("vmin", 0, 255, hsv_values)
        self.create_slider("vmax", 0, 255, hsv_values)

        # Save Button
        self.save_button = QPushButton("Save HSV")
        self.save_button.clicked.connect(self.save_hsv)

        # Create layout for sliders, labels, and value labels
        layout = QGridLayout()
        self.add_to_layout(layout, "hmin", 0)
        self.add_to_layout(layout, "hmax", 1)
        self.add_to_layout(layout, "smin", 2)
        self.add_to_layout(layout, "smax", 3)
        self.add_to_layout(layout, "vmin", 4)
        self.add_to_layout(layout, "vmax", 5)
        layout.addWidget(self.save_button, 6, 1)

        self.setLayout(layout)

    def create_slider(self, name, min_val, max_val, hsv_values):
        # Create slider, label, and value label
        slider = QSlider(Qt.Horizontal)
        label = QLabel(f"{name.capitalize()}:")
        value_label = QLabel(f"{hsv_values[name]}")

        # Set initial values and ranges for sliders
        slider.setRange(min_val, max_val)
        slider.setValue(hsv_values[name])

        # Store references
        self.sliders[name] = slider
        self.labels[name] = label
        self.value_labels[name] = value_label

        # Connect slider signals to update value labels
        slider.valueChanged.connect(lambda value, name=name: self.update_value_label(name, value))
        slider.valueChanged.connect(self.emit_slider_values)

    def add_to_layout(self, layout, name, row):
        layout.addWidget(self.labels[name], row, 0)
        layout.addWidget(self.sliders[name], row, 1)
        layout.addWidget(self.value_labels[name], row, 2)

    def update_value_label(self, name, value):
        self.value_labels[name].setText(str(value))

    @pyqtSlot()
    def emit_slider_values(self):
        values = {name: slider.value() for name, slider in self.sliders.items()}
        self.slider_values_signal.emit(*values.values())

    def save_hsv(self):
        hsv_values = {name: slider.value() for name, slider in self.sliders.items()}
        save_json('hsv.json', hsv_values)

        message_box = QMessageBox()
        message_box.setWindowTitle("HSV Values")
        message_box.setText('Saved HSV range values successfully')
        message_box.exec_()