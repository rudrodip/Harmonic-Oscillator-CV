from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QFileDialog,
    QComboBox,
    QInputDialog,
    QHBoxLayout,
    QSplitter,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
import pyqtgraph as pg
import os
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from scipy.optimize import curve_fit
from processing.video_thread import VideoThread
from windows.hsv_slider import HSVSlider
from windows.analyze_widget import AnalyzeWidget
from utils.utils import (
    underdamped_harmonic_oscillator,
    upper_decaying_component_curve,
    lower_decaying_component_curve,
)


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Constants
        self.postion_plot_color = QColor(3, 252, 194)
        self.fitted_plot_color = QColor(255, 127, 80)

        # Initialize attributes
        self.setWindowTitle("Harmonic Oscillator")
        self.disply_width = 1280
        self.display_height = 720
        self.video_path = None
        self.initial_guess = [1.0, 0.1, 1.0, 0.0, 0.0]
        self.data_points = []
        self.thread = None
        self.selected_display_option = "Main Video"
        self.selected_mask_option = "Color Detection"
        self.draw_params = True

        # Create UI components
        self.create_buttons()
        self.create_labels()
        self.create_graph_layout()
        self.create_hsv_slider()
        self.create_analyze_widget()

        # Set up the main layout
        self.create_layout()
        self.setFixedWidth(self.disply_width)

    def create_buttons(self):
        # "Run" button
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.start_video_thread)
        self.run_button.setEnabled(False)

        # "Stop" button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_video_thread)
        self.stop_button.setEnabled(False)

        # "Select File" button
        self.select_file_button = QPushButton("Select Video", self)
        self.select_file_button.clicked.connect(self.select_video_file)

        # "WebCam" button
        self.webcam_button = QPushButton("Webcam", self)
        self.webcam_button.clicked.connect(self.webcam_selection)

        # "Draw Param" button
        self.draw_param_button = QPushButton("Hide Param", self)
        self.draw_param_button.clicked.connect(self.draw_param_selection)

        # URL Input Dialog
        self.url_button = QPushButton("URL", self)
        self.url_button.clicked.connect(self.url_submission)

        # Dropdown selection - display options
        self.display_options = QComboBox(self)
        self.display_options.addItems(["Main Video", "Image Contours", "Mask"])
        self.display_options.currentTextChanged.connect(self.display_selection_changed)

        # Dropdown selection - mask options
        self.mask_options = QComboBox(self)
        self.mask_options.addItems(
            ["Color Detection", "Edge Detection", "Circle Detection"]
        )
        self.mask_options.currentTextChanged.connect(self.mask_selection_changed)

    def create_labels(self):
        # QLabel with the text "Video"
        self.video_label = QLabel("No video selected", self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(
            "font-size: 24px; background-color: black; color: white;"
        )

    def create_graph_layout(self):
        self.graph_layout = pg.GraphicsLayoutWidget()
        self.plot = self.graph_layout.addPlot(title="Position v/s time plot")
        self.plot.showGrid(x=True, y=True)
        self.plot.addLegend()
        self.plot.setLabel("left", "X position of BOB")
        self.plot.setLabel("bottom", "Time")

        # Initialize plots

        # position vs time plot
        self.position_plot_data = self.plot.plot(
            pen=pg.mkPen(color=self.postion_plot_color, width=3),
            symbol="o",
            symbolPen="b",
            symbolBrush=self.postion_plot_color,
            symbolSize=3,
            name="Actual Position",
        )
        self.position_plot_data.setDownsampling(auto=True, method="subsample")
        self.position_plot_data.setClipToView(True)
        self.position_plot_data.setClipToView(True)

        # curve fit plot
        self.fitted_plot_data = self.plot.plot(
            pen=pg.mkPen(color=self.fitted_plot_color, width=3, style=Qt.DashLine),
            name="Fitted Curve",
        )

        # upper decaying component curve plot
        self.upper_decay_plot = self.plot.plot(
            pen=pg.mkPen(color="g", width=2, style=Qt.DashLine),
        )

        # lower decaying component curve plot
        self.lower_decay_plot = self.plot.plot(
            pen=pg.mkPen(color="g", width=2, style=Qt.DashLine),
            name="Decay Curve",
        )

    def create_hsv_slider(self):
        # HSVSlider
        self.hsv_slider = HSVSlider(self)
        self.hsv_slider.setEnabled(False)

    def create_analyze_widget(self):
        # Analyze widget
        self.analyze_widget = AnalyzeWidget(self)
        self.analyze_widget.analyze_signal.connect(self.fit_data_point)
        self.analyze_widget.setEnabled(False)

    def create_layout(self):
        # Create layouts for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.select_file_button)
        button_layout.addWidget(self.webcam_button)
        button_layout.addWidget(self.url_button)
        button_layout.addWidget(self.display_options)
        button_layout.addWidget(self.mask_options)
        button_layout.addWidget(self.draw_param_button)

        # Create a vertical splitter for the second row (video and graph)
        video_graph_splitter = QSplitter(Qt.Horizontal)
        video_graph_splitter.addWidget(self.video_label)
        video_graph_splitter.addWidget(self.graph_layout)

        # Set stretch factors for video and graph (40% for video, 60% for graph)
        video_graph_splitter.setSizes(
            [int(self.display_height * 0.4), int(self.display_height * 0.6)]
        )

        # Create a vertical splitter for the third row (HSV Slider and Analyze widget)
        slider_analyze_splitter = QSplitter(Qt.Horizontal)
        slider_analyze_splitter.addWidget(self.hsv_slider)
        slider_analyze_splitter.addWidget(self.analyze_widget)

        # Set stretch factors for slider and analyzer (40% for slider,60% for analyzer)
        slider_analyze_splitter.setSizes(
            [int(self.display_height * 0.4), int(self.display_height * 0.6)]
        )

        # Create a grid layout
        grid_layout = QGridLayout()
        grid_layout.addLayout(button_layout, 0, 0)
        grid_layout.addWidget(video_graph_splitter, 1, 0)
        grid_layout.addWidget(slider_analyze_splitter, 2, 0)

        # Set stretch factors
        grid_layout.setRowStretch(0, 0)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 0)

        # Set the grid layout as the main widget's layout
        self.setLayout(grid_layout)

    @pyqtSlot()
    def url_submission(self):
        dialog = QInputDialog()
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("Submit video URL")
        dialog.setLabelText("URL:")
        dialog.setTextValue("")
        dialog.resize(400, 200)

        pressed = dialog.exec_()

        if pressed == QInputDialog.Accepted:
            self.video_path = dialog.textValue()
            self.video_label.setText("Video Url Submitted\nClick Run button to play!")
            self.video_label.adjustSize()
            self.run_button.setEnabled(True)

    @pyqtSlot()
    def webcam_selection(self):
        self.video_path = 0
        self.video_label.setText("Webcam selected\nClick Run button to play!")
        self.video_label.adjustSize()
        self.run_button.setEnabled(True)

    @pyqtSlot()
    def draw_param_selection(self):
        self.draw_params = not self.draw_params
        self.draw_param_button.setText(
            "Hide Param" if self.draw_params else "Draw Params"
        )

    @pyqtSlot()
    def select_video_file(self):
        if self.thread is None or (
            not self.thread.isRunning() and self.video_path is not None
        ):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Select Video File",
                "",
                "Video Files (*.mp4 *.avi);;All Files (*)",
                options=options,
            )

            if file_name:
                self.video_path = file_name
                self.video_label.setText(
                    f"{os.path.basename(file_name)} selected\nClick Run button to play!"
                )
                self.video_label.adjustSize()
                self.run_button.setEnabled(True)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)

        # Calculate the scaled size while maintaining the aspect ratio
        scaled_size = qt_img.size().scaled(self.video_label.size(), Qt.KeepAspectRatio)

        # Set the scaled pixmap
        self.video_label.setPixmap(qt_img.scaled(scaled_size, Qt.KeepAspectRatio))

    @pyqtSlot(float, float)
    def update_graph(self, time, cx):
        if self.thread and self.thread.isRunning():
            self.data_points.append((time, cx))
            if len(self.data_points) != 0:
                x_data = np.array(self.data_points)[:, 0]
                y_data = np.array(self.data_points)[:, 1]
                self.position_plot_data.setData(x=x_data, y=y_data)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        p = convert_to_Qt_format.scaled(
            self.disply_width, self.display_height, Qt.KeepAspectRatio
        )
        return QPixmap.fromImage(p)

    def closeEvent(self, event):
        if self.thread:
            self.thread.stop()
            event.accept()

    def update_button_states(self, running):
        """
        Update the enabled/disabled state of buttons and widgets based on whether
        the video thread is running or not.

        Args:
            running (bool): True if the video thread is running, False otherwise.
        """
        self.run_button.setEnabled(not running)
        self.select_file_button.setEnabled(not running)
        self.webcam_button.setEnabled(not running)
        self.display_options.setEnabled(not running)
        self.mask_options.setEnabled(not running)
        self.url_button.setEnabled(not running)
        self.draw_param_button.setEnabled(not running)
        self.analyze_widget.setEnabled(not running)

        self.stop_button.setEnabled(running)
        self.hsv_slider.setEnabled(running)

    def start_video_thread(self):
        if (
            self.thread is None
            or not self.thread.isRunning()
            and self.video_path is not None
        ):
            self.thread = VideoThread(
                video_path=self.video_path,
                display_option=self.selected_display_option,
                mask_option=self.selected_mask_option,
                draw_params=self.draw_params,
            )
            # Clear all data and plots before running
            self.data_points.clear()
            self.position_plot_data.clear()
            self.fitted_plot_data.clear()

            self.thread.finished_signal.connect(self.video_thread_finished)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.new_contour_signal.connect(self.update_graph)
            self.thread.parameter_signal.connect(self.analyze_widget.show_params)
            self.hsv_slider.slider_values_signal.connect(self.thread.update_hsv_range)

            self.thread.start()
            self.update_button_states(running=True)

    def stop_video_thread(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
        self.update_button_states(running=False)

    def display_selection_changed(self, selected_option):
        self.selected_display_option = selected_option

    def mask_selection_changed(self, selected_option):
        self.selected_mask_option = selected_option

    def video_thread_finished(self):
        self.update_button_states(False)

    def fit_data_point(self):
        x_data = np.array(self.data_points)[:, 0]
        y_data = np.array(self.data_points)[:, 1]

        # Perform the curve fitting
        initial_guess = [1.0, 0.1, 1.0, 0.0, 0.0]
        params, _ = curve_fit(
            underdamped_harmonic_oscillator, x_data, y_data, p0=initial_guess
        )

        # Extract the fitted parameters
        A, gamma, f, phi, C = params
        self.fitted_plot_data.setData(
            x=x_data, y=underdamped_harmonic_oscillator(x_data, A, gamma, f, phi, C)
        )

        self.upper_decay_plot.setData(
            x=x_data, y=upper_decaying_component_curve(x_data, A, gamma, C)
        )
        self.lower_decay_plot.setData(
            x=x_data, y=lower_decaying_component_curve(x_data, A, gamma, C)
        )

        self.analyze_widget.update_params(params)
