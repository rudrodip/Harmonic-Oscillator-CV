import cv2
import numpy as np
from processing.detector import ImageProcessor
from scipy.optimize import least_squares
import csv
from utils.utils import load_json, circle_residuals
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class VideoThread(QThread):
    # Define custom signals for communication with the main application
    update_hsv_range_signal = pyqtSignal(int, int, int, int, int, int)
    finished_signal = pyqtSignal()
    change_pixmap_signal = pyqtSignal(np.ndarray)
    new_contour_signal = pyqtSignal(float, float)
    parameter_signal = pyqtSignal(dict)

    initial_guess = np.array([3.0, 3.0, 2.0])

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
        self.frame_number = 0
        self.display_option = display_option
        self.mask_option = mask_option
        self.draw_params = draw_params
        self.data_points = []
        self.params = {
            "xmin": self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            "xmax": 0,
        }
        self.hsvVals = load_json("hsv.json")
        self.processor = ImageProcessor(self.hsvVals)
        self.update_hsv_range_signal.connect(self.update_hsv_range)

    def run(self, save_data=False):
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
                radius = (contours[0]["bbox"][2] + contours[0]["bbox"][3]) / 4
                self.data_points.append((cx, cy))
                time = self.frame_number / self.frame_rate

                self.new_contour_signal.emit(time, cx)

                points = np.array(self.data_points)
                x_data = points[:, 0]
                y_data = points[:, 1]

                result = least_squares(
                    circle_residuals, self.initial_guess, args=(x_data, y_data)
                )
                fitted_a, fitted_b, fitted_r = result.x

                if cx > self.params["xmax"]:
                    self.params["xmax"] = cx
                if cx < self.params["xmin"]:
                    self.params["xmin"] = cx

                self.params["center"] = (int(fitted_a), int(fitted_b))
                self.params["length"] = int(fitted_r)
                self.params["radius"] = radius
                self.parameter_signal.emit(self.params)

            if self.draw_params and self.params:
                cv2.line(
                    frame,
                    (int(self.params["xmin"]), int(fitted_b)),
                    (int(self.params["xmax"]), int(fitted_b)),
                    (255, 255, 0),
                    2,
                )
                cv2.circle(frame, (cx, int(fitted_b)), 5, (0, 0, 0), -1)

                cv2.line(
                    frame, (int(fitted_a), int(fitted_b)), (cx, cy), (0, 255, 0), 2
                )
                cv2.circle(frame, (int(fitted_a), int(fitted_b)), 5, (255, 0, 0), -1)
                cv2.circle(
                    frame,
                    (int(fitted_a), int(fitted_b)),
                    int(fitted_r),
                    (255, 255, 0),
                    2,
                )

            self.frame_number += 1

            if self.display_option == "Mask":
                self.change_pixmap_signal.emit(mask)
            else:
                self.change_pixmap_signal.emit(frame)

        self.cap.release()
        self.finished_signal.emit()
        if save_data:
            self.save_to_csv("data.csv", self.data_points)

    def stop(self):
        self._run_flag = False
        self.wait()

    @staticmethod
    def save_to_csv(filename, data_points):
        with open(filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["X Position", "Y Position"])

            for cx, cy in data_points:
                csv_writer.writerow([cx, cy])

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
