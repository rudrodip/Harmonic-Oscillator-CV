import os
import math
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QPushButton, QMessageBox
from utils.utils import save_json, get_project_root

project_root = get_project_root(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, 'data')

class AnalyzeWidget(QWidget):
    analyze_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.params = [1.0, 0.1, 1.0, 0.0, 0.0]
        self.visual_params = {}

        # Initialize GUI components
        self.init_ui()

    def init_ui(self):
        # Create labels for displaying parameter values
        self.create_param_labels()
        self.create_value_labels()

        # Create buttons
        self.create_buttons()

        # Create layout for arranging widgets
        self.create_layout()

        # Connect button click events to slots
        self.connect_buttons()

    def create_param_labels(self):
        self.param_labels = [
            QLabel("A (amplitude): "),
            QLabel("γ (damping coefficient): "),
            QLabel("ω (omega): "),
            QLabel("ϕ (phase angle): "),
            QLabel("C (constant): "),
        ]

    def create_value_labels(self):
        self.param_value_labels = [
            QLabel("0"),
            QLabel("0"),
            QLabel("0"),
            QLabel("0"),
            QLabel("0"),
        ]

        self.center_value_label = QLabel("(0, 0) pixel")
        self.length_value_label = QLabel("0 pixel")
        self.radius_value_label = QLabel("0 m")
        self.length_pivot_to_center_value_label = QLabel("0 m")
        self.length_pivot_to_surface_value_label = QLabel("0 m")
        self.angle_rad_value_label = QLabel("0 rad")
        self.angle_deg_value_label = QLabel("0 deg")

    def create_buttons(self):
        self.curve_fit_button = QPushButton("Estimate")
        self.save_button = QPushButton("Save")

    def create_layout(self):
        layout = QGridLayout()

        for row, (param_label, param_value_label) in enumerate(
            zip(self.param_labels, self.param_value_labels)
        ):
            layout.addWidget(param_label, row, 0)
            layout.addWidget(param_value_label, row, 1)

        layout.addWidget(self.curve_fit_button, len(self.param_labels), 0)
        layout.addWidget(self.save_button, len(self.param_labels), 2)

        layout.addWidget(QLabel("Center: "), 0, 2)
        layout.addWidget(self.center_value_label, 0, 3)
        layout.addWidget(QLabel("Length (pixel): "), 1, 2)
        layout.addWidget(self.length_value_label, 1, 3)
        layout.addWidget(QLabel("Radius (bob)): "), 2, 2)
        layout.addWidget(self.radius_value_label, 2, 3)
        layout.addWidget(QLabel("Length (pivot to center): "), 3, 2)
        layout.addWidget(self.length_pivot_to_center_value_label, 3, 3)
        layout.addWidget(QLabel("Length (pivot to sur): "), 4, 2)
        layout.addWidget(self.length_pivot_to_surface_value_label, 4, 3)
        layout.addWidget(QLabel("Angle (rad): "), 0, 4)
        layout.addWidget(self.angle_rad_value_label, 0, 5)
        layout.addWidget(QLabel("Angle (deg): "), 1, 4)
        layout.addWidget(self.angle_deg_value_label, 1, 5)

        self.setLayout(layout)

    def connect_buttons(self):
        self.curve_fit_button.clicked.connect(self.trigger_analysis)
        self.save_button.clicked.connect(self.save_params)

    def trigger_analysis(self):
        self.analyze_signal.emit()

    def update_params(self, params):
        self.params = params
        for i, value_label in enumerate(self.param_value_labels):
            value_label.setText(f"{params[i]:.3f}")

        length = 9.8 / (params[2]) ** 2
        self.length_pivot_to_center_value_label.setText(f"{length:.4f} m")

        ratio = (
            self.visual_params["length"] / self.visual_params["radius_bob"]
            if self.visual_params["radius_bob"] != 0
            else None
        )
        length_pivot_to_sur = length - (length / ratio)
        self.length_pivot_to_surface_value_label.setText(f"{length_pivot_to_sur:.4f} m")

    def save_params(self):
        A, gamma, w, phi, C = self.params
        param_json = {"A": A, "gamma": gamma, "w": w, "phi": phi, "C": C}
        save_json(os.path.join(data_folder, "json", "parameters.json"), param_json)
        self.show_message_box("Parameters", "Saved parameters successfully")

    @pyqtSlot(dict)
    def show_params(self, params):
        self.visual_params = params
        self.center_value_label.setText(f"{params['center']} pixel")
        self.length_value_label.setText(f"{params['length']} pixel")
        self.angle_rad_value_label.setText(f"{params['angle_rad']:.3f} rad")
        self.angle_deg_value_label.setText(f"{math.degrees(params['angle_rad']):.3f} deg")

    def show_message_box(self, title, message):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec_()
