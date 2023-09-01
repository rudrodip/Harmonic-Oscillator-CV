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
        hsv_values = load_json("hsv.json")

        # Create sliders, labels, and value labels
        self.hmin_slider = QSlider(Qt.Horizontal)
        self.hmax_slider = QSlider(Qt.Horizontal)
        self.smin_slider = QSlider(Qt.Horizontal)
        self.smax_slider = QSlider(Qt.Horizontal)
        self.vmin_slider = QSlider(Qt.Horizontal)
        self.vmax_slider = QSlider(Qt.Horizontal)

        self.hmin_slider.valueChanged.connect(self.emit_slider_values)
        self.hmax_slider.valueChanged.connect(self.emit_slider_values)
        self.smin_slider.valueChanged.connect(self.emit_slider_values)
        self.smax_slider.valueChanged.connect(self.emit_slider_values)
        self.vmin_slider.valueChanged.connect(self.emit_slider_values)
        self.vmax_slider.valueChanged.connect(self.emit_slider_values)

        self.hmin_label = QLabel("Hmin:")
        self.hmax_label = QLabel("Hmax:")
        self.smin_label = QLabel("Smin:")
        self.smax_label = QLabel("Smax:")
        self.vmin_label = QLabel("Vmin:")
        self.vmax_label = QLabel("Vmax:")

        self.hmin_value_label = QLabel(f"{hsv_values['hmin']}")  # Initial value label
        self.hmax_value_label = QLabel(f"{hsv_values['hmax']}")  # Initial value label
        self.smin_value_label = QLabel(f"{hsv_values['smin']}")  # Initial value label
        self.smax_value_label = QLabel(f"{hsv_values['smax']}")  # Initial value label
        self.vmin_value_label = QLabel(f"{hsv_values['vmin']}")  # Initial value label
        self.vmax_value_label = QLabel(f"{hsv_values['vmax']}")  # Initial value label

        # Connect slider signals to update value labels
        self.hmin_slider.valueChanged.connect(self.update_hmin_value_label)
        self.hmax_slider.valueChanged.connect(self.update_hmax_value_label)
        self.smin_slider.valueChanged.connect(self.update_smin_value_label)
        self.smax_slider.valueChanged.connect(self.update_smax_value_label)
        self.vmin_slider.valueChanged.connect(self.update_vmin_value_label)
        self.vmax_slider.valueChanged.connect(self.update_vmax_value_label)

        # Set initial values and ranges for sliders
        self.hmin_slider.setRange(0, 179)  # Hue range [0, 179]
        self.hmax_slider.setRange(0, 179)  # Hue range [0, 179]
        self.smin_slider.setRange(0, 255)  # Saturation range [0, 255]
        self.smax_slider.setRange(0, 255)  # Saturation range [0, 255]
        self.vmin_slider.setRange(0, 255)  # Value range [0, 255]
        self.vmax_slider.setRange(0, 255)  # Value range [0, 255]

        # Set initial values for sliders
        self.hmin_slider.setValue(hsv_values['hmin'])
        self.hmax_slider.setValue(hsv_values['hmax'])
        self.smin_slider.setValue(hsv_values['smin'])
        self.smax_slider.setValue(hsv_values['smax'])
        self.vmin_slider.setValue(hsv_values['vmin'])
        self.vmax_slider.setValue(hsv_values['vmax'])

        # Save Button
        self.save_button = QPushButton("Save HSV")
        self.save_button.clicked.connect(self.save_hsv)

        # Create layout for sliders, labels, and value labels
        layout = QGridLayout()
        layout.addWidget(self.hmin_label, 0, 0)
        layout.addWidget(self.hmin_slider, 0, 1)
        layout.addWidget(self.hmin_value_label, 0, 2)
        layout.addWidget(self.hmax_label, 1, 0)
        layout.addWidget(self.hmax_slider, 1, 1)
        layout.addWidget(self.hmax_value_label, 1, 2)
        layout.addWidget(self.smin_label, 2, 0)
        layout.addWidget(self.smin_slider, 2, 1)
        layout.addWidget(self.smin_value_label, 2, 2)
        layout.addWidget(self.smax_label, 3, 0)
        layout.addWidget(self.smax_slider, 3, 1)
        layout.addWidget(self.smax_value_label, 3, 2)
        layout.addWidget(self.vmin_label, 4, 0)
        layout.addWidget(self.vmin_slider, 4, 1)
        layout.addWidget(self.vmin_value_label, 4, 2)
        layout.addWidget(self.vmax_label, 5, 0)
        layout.addWidget(self.vmax_slider, 5, 1)
        layout.addWidget(self.vmax_value_label, 5, 2)
        layout.addWidget(self.save_button, 6, 1)

        self.setLayout(layout)

    # Slot functions to update value labels
    def update_hmin_value_label(self, value):
        self.hmin_value_label.setText(str(value))

    def update_hmax_value_label(self, value):
        self.hmax_value_label.setText(str(value))

    def update_smin_value_label(self, value):
        self.smin_value_label.setText(str(value))

    def update_smax_value_label(self, value):
        self.smax_value_label.setText(str(value))

    def update_vmin_value_label(self, value):
        self.vmin_value_label.setText(str(value))

    def update_vmax_value_label(self, value):
        self.vmax_value_label.setText(str(value))

    @pyqtSlot()
    def emit_slider_values(self):
        hmin_value = self.hmin_slider.value()
        hmax_value = self.hmax_slider.value()
        smin_value = self.smin_slider.value()
        smax_value = self.smax_slider.value()
        vmin_value = self.vmin_slider.value()
        vmax_value = self.vmax_slider.value()

        self.slider_values_signal.emit(
            hmin_value, hmax_value, smin_value, smax_value, vmin_value, vmax_value
        )

    def save_hsv(self):
        hmin_value = self.hmin_slider.value()
        hmax_value = self.hmax_slider.value()
        smin_value = self.smin_slider.value()
        smax_value = self.smax_slider.value()
        vmin_value = self.vmin_slider.value()
        vmax_value = self.vmax_slider.value()

        hsvVal = {
            "hmin": hmin_value,
            "smin": smin_value,
            "vmin": vmin_value,
            "hmax": hmax_value,
            "smax": smax_value,
            "vmax": vmax_value,
        }

        save_json('hsv.json', hsvVal)

        message_box = QMessageBox()
        message_box.setWindowTitle("HSV Values")
        message_box.setText('Saved hsv range values successfully')
        message_box.exec_()