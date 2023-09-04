import os
import cv2
import numpy as np
from processing.detector import ImageProcessor
from scipy.optimize import least_squares
import csv
from utils.utils import load_json, get_project_root, rotated_circle_residuals, rotate_point, rotate_opencv_point
from utils.contansts import WHITE, BLACK, BLUE, CYAN, GREEN, RED
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

project_root = get_project_root(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, 'data')

class VideoThread(QThread):
    # Define custom signals for communication with the main application
    update_hsv_range_signal = pyqtSignal(int, int, int, int, int, int)
    finished_signal = pyqtSignal()
    change_pixmap_signal = pyqtSignal(np.ndarray)
    new_contour_signal = pyqtSignal(float, float)
    parameter_signal = pyqtSignal(dict)
    processing_signal = pyqtSignal(int)

    # initial values
    initial_circle_guess = np.array([0.0, 0.0, 1.0, 0.0])
    circle_params = initial_circle_guess

    # bools
    circle_threshold_reached = False
    save_data = True

    def __init__(
        self,
        video_path,
        display_option,
        mask_option,
        draw_params=False,
    ):
        super().__init__()
        self._run_flag = True
        self.cap = cv2.VideoCapture(video_path)
        self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.display_option = display_option
        self.mask_option = mask_option
        self.draw_params = draw_params
        self.update_hsv_range_signal.connect(self.update_hsv_range)

        # internal data
        self.hsvVals = load_json(os.path.join(data_folder, "json", "hsv.json"))
        self.data_points = np.empty((0, 3), dtype=float)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.params = {
            "angle_rad": 0,
        }

        # image processor initialization
        self.processor = ImageProcessor(self.hsvVals)

    def calculate_static_params(self):
        if len(self.data_points) == 0: return
        x_data = self.data_points[:, 0]  # x positions
        y_data = self.data_points[:, 1]  # y positions

        # attempting to fit the values in a circle
        circle_result = least_squares(
            rotated_circle_residuals, self.initial_circle_guess, args=(x_data, y_data)
        )

        self.circle_params = circle_result.x
        fitted_a, fitted_b, fitted_r, _ = self.circle_params

        self.calculate_rotation_angle(fitted_a, fitted_b)

        self.params['mean_point'] = self.calculate_mean_point()
        self.params['center'] = (int(fitted_a), int(fitted_b))
        self.params["length"] = int(fitted_r)
        self.parameter_signal.emit(self.params)

    def calculate_rotation_angle(self, fitted_a, fitted_b):
        # Calculate the angles of data points with respect to the circle's center
        self.data_points = np.array(self.data_points)
        mean_x = np.mean(self.data_points[:, 0])
        mean_y = np.mean(self.data_points[:, 1])

        OFFSET = 90
        rotation_angle = np.arctan2(fitted_b - mean_y, fitted_a - mean_x) + np.radians(OFFSET)
        self.params["angle_rad"] = rotation_angle

    def calculate_mean_point(self):
        mean_x = np.mean(self.data_points[:, 0])
        mean_y = np.mean(self.data_points[:, 1])
        return (int(mean_x), int(mean_y))

    def run(self):
        frame_number = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while self._run_flag:
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.mask_option == "Color Detection":
                mask = self.processor.get_color_mask(frame)
            elif self.mask_option == "Edge Detection":
                mask = self.processor.get_edges(frame)
            else:
                mask = self.processor.get_best_circle(frame)

            contours_output = self.processor.get_contours(frame, mask)

            if self.display_option == "Image Contours":
                frame = contours_output["image_contours"]

            contours = contours_output["contours"]

            if contours:
                cx, cy = contours[0]["center"]
                radius_bob = (contours[0]["bbox"][2] + contours[0]["bbox"][3]) / 4
                fitted_a, fitted_b, _, _ = self.circle_params

                if frame_number < 1000 and frame_number % 50 == 0:
                    self.data_points = np.append(self.data_points, [[cx, cy, frame_number]], axis=0)
                    self.calculate_static_params()
                    self.params['radius_bob'] = radius_bob

                x_transformed, _ = rotate_opencv_point(
                    cx, cy, fitted_a, fitted_b, self.params['angle_rad'], self.height
                )
                self.draw_param(frame, (cx, cy))
                if frame_number % 10 == 0:
                    # emit signals
                    self.new_contour_signal.emit(frame_number, x_transformed)

            frame_number += 1

            if self.display_option == "Mask":
                self.change_pixmap_signal.emit(mask)
            else:
                self.change_pixmap_signal.emit(frame)

        self.cap.release()
        self.finished_signal.emit()

    def draw_param(self, frame, bob_pos):
        if not self.draw_params or not self.params:
            return
        cx, cy = bob_pos
        fitted_a, fitted_b, fitted_r, _ = self.circle_params

        pivot_point = (int(fitted_a), int(fitted_b))
        mean_point = self.params['mean_point']

        # string line
        cv2.line(frame, pivot_point, (cx, cy), WHITE, 2)

        # pivot point to mean point
        # cv2.line(frame, pivot_point, mean_point, BLACK, 2)

        # horizontal line
        VideoThread.draw_tangent_line(frame, pivot_point, self.params['angle_rad'], GREEN)

        # pivot point
        cv2.circle(frame, (int(fitted_a), int(fitted_b)), 5, RED, -1)

        # mean point
        # cv2.circle(frame, mean_point, 5, BLUE, -1)

        # draw pendulum path
        cv2.circle(
            frame,
            pivot_point,
            int(abs(fitted_r)),
            CYAN,
            2,
        )

    def stop(self):
        self._run_flag = False
        self.wait()

    @pyqtSlot(int, int, int, int, int, int)
    def update_hsv_range(self, hmin, hmax, smin, smax, vmin, vmax):
        hsv_vals = {
            "hmin": hmin,
            "smin": smin,
            "vmin": vmin,
            "hmax": hmax,
            "smax": smax,
            "vmax": vmax,
        }
        self.processor.hsv_vals = hsv_vals

    @staticmethod
    def save_to_csv(filename, data_points):
        filename = os.path.join(data_folder, "csv", filename)
        with open(filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["X Position", "Y Position", "Time"])

            for cx, cy, time in data_points:
                csv_writer.writerow([cx, cy, time])

    @staticmethod
    def draw_tangent_line(image, point, theta, color=(0, 255, 0), thickness=2):
        # Calculate the slope of the line (tangent of theta)

        # theta += np.pi / 2
        length = image.shape[1]
        x, y = point[0], point[1]

        # Calculate the endpoint of the line
        x_end = int(x + length * np.cos(theta))
        y_end = int(y + length * np.sin(theta))

        # Calculate the start point of the line to ensure it passes through (x, y)
        x_start = int(x - length * np.cos(theta))
        y_start = int(y - length * np.sin(theta))

        # Draw the line on the image
        cv2.line(image, (x_start, y_start), (x_end, y_end), color, thickness)
