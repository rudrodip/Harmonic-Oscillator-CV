from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QWidget,
    QSlider,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from utils.utils import save_json

class AnalyzeWindow(QWidget):
    analyze_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.params = [1.0, 0.1, 1.0, 0.0, 0.0]
        self.visual_params = {}

        # Create labels for displaying parameter values
        self.param1_label = QLabel("A (amplitude): ")
        self.param2_label = QLabel("γ (damping coefficient): ")
        self.param3_label = QLabel("f (frequency): ")
        self.param4_label = QLabel("ϕ (phase angle): ")
        self.param5_label = QLabel("C (constant): ")

        self.center_label = QLabel("Center: ")
        self.length_label = QLabel("Length (pixel): ")
        self.radius_label = QLabel("Radius (ball)): ")
        self.ratio_label = QLabel("Ratio (L/r): ")
        self.length_pivot_to_center_label = QLabel("Length (pivot to center): ")
        self.length_pivot_to_surface_label = QLabel("Length (pivot to sur): ")

        # Create placeholders for parameter values
        self.param1_value_label = QLabel("0")
        self.param2_value_label = QLabel("0")
        self.param3_value_label = QLabel("0")
        self.param4_value_label = QLabel("0")
        self.param5_value_label = QLabel("0")

        self.center_value_label = QLabel("(0, 0) pixel")
        self.length_value_label = QLabel("0 pixel")
        self.radius_value_label = QLabel("0 pixel")
        self.ratio_value_label = QLabel("0 pixel")
        self.length_pivot_to_center_value_label = QLabel("0 m")
        self.length_pivot_to_surface_value_label = QLabel("0 m")

        # a button for curve fit
        self.curve_fit_button = QPushButton("Estimate")
        self.save_button = QPushButton("Save")

        # Create a layout for arranging the widgets
        layout = QGridLayout()
        layout.addWidget(self.param1_label, 0, 0)
        layout.addWidget(self.param1_value_label, 0, 1)
        layout.addWidget(self.param2_label, 1, 0)
        layout.addWidget(self.param2_value_label, 1, 1)
        layout.addWidget(self.param3_label, 2, 0)
        layout.addWidget(self.param3_value_label, 2, 1)
        layout.addWidget(self.param4_label, 3, 0)
        layout.addWidget(self.param4_value_label, 3, 1)
        layout.addWidget(self.param5_label, 4, 0)
        layout.addWidget(self.param5_value_label, 4, 1)
        layout.addWidget(self.curve_fit_button, 5, 0)
        layout.addWidget(self.save_button, 5, 2)
        
        layout.addWidget(self.center_label, 0, 2)
        layout.addWidget(self.center_value_label, 0, 3)
        layout.addWidget(self.length_label, 1, 2)
        layout.addWidget(self.length_value_label, 1, 3)
        layout.addWidget(self.radius_label, 2, 2)
        layout.addWidget(self.radius_value_label, 2, 3)
        layout.addWidget(self.ratio_label, 3, 2)
        layout.addWidget(self.ratio_value_label, 3, 3)
        layout.addWidget(self.length_pivot_to_center_label, 4, 2)
        layout.addWidget(self.length_pivot_to_center_value_label, 4, 3)
        layout.addWidget(self.length_pivot_to_surface_label, 0, 4)
        layout.addWidget(self.length_pivot_to_surface_value_label, 0, 5)

        self.setLayout(layout)

        # connecting the curve fit button to a slot function
        self.curve_fit_button.clicked.connect(self.trigger_analysis)
        self.save_button.clicked.connect(self.save_params)

    def trigger_analysis(self):
        # Emit the custom signal when the button is clicked
        self.analyze_signal.emit()

    def update_params(self, params):
        self.params = params
        self.param1_value_label.setText(f"{params[0]:.3f}")
        self.param2_value_label.setText(f"{params[1]:.3f}")
        self.param3_value_label.setText(f"{params[2]:.3f}")
        self.param4_value_label.setText(f"{params[3]:.3f}")
        self.param5_value_label.setText(f"{params[4]:.3f}")

        length = 9.8 / (2*3.1416*params[2])**2
        self.length_pivot_to_center_value_label.setText(f"{length:.2f} m")

        ratio = self.visual_params['length'] / self.visual_params['radius'] if self.visual_params['radius'] != 0 else None
        length_pivot_to_sur = length - (length / ratio)
        self.length_pivot_to_surface_value_label.setText(f"{length_pivot_to_sur:.2f} m")

    def save_params(self):
        A, gamma, f, phi, C = self.params
        param_json = {"A": A, "gamma": gamma, "f": f, "phi": phi, "C": C}
        save_json('parameters.json', param_json)

        message_box = QMessageBox()
        message_box.setWindowTitle("Parameters")
        message_box.setText('Saved parameters successfully')
        message_box.exec_()

    @pyqtSlot(dict)
    def show_params(self, params):
        self.visual_params = params
        self.center_value_label.setText(f"{params['center']} pixel")
        self.length_value_label.setText(f"{params['length']} pixel")
        self.radius_value_label.setText(f"{params['radius']} pixel")

        ratio = params['length'] / params['radius'] if params['radius'] != 0 else None
        self.ratio_value_label.setText(f"{ratio:.2f}")