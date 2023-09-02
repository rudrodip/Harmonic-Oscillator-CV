import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

class ImageProcessor:
    def __init__(self, hsv_vals: dict, gaussian_kernel: tuple = (17, 17)):
        """
        Initialize the ImageProcessor.

        Args:
            hsv_vals (dict): HSV color values for color-based processing.
            gaussian_kernel (tuple): Gaussian kernel size for image smoothing. Default is (17, 17).
        """
        self.hsv_vals = hsv_vals
        self.color_finder = ColorFinder()
        self.gaussian_kernel = gaussian_kernel

    def get_contours(self, frame, mask, min_area: int = 200):
        """
        Get contours from the input frame using a mask.

        Args:
            frame (numpy.ndarray): Input image frame.
            mask (numpy.ndarray): Mask to filter objects of interest.
            min_area (int): Minimum area for detected contours. Default is 200.

        Returns:
            dict: Dictionary containing mask, image with drawn contours, and list of detected contours.
        """
        frame_with_contours, contours = cvzone.findContours(
            frame, mask, minArea=min_area
        )

        if contours:
            cx, cy = contours[0]["center"]
            area = int(contours[0]["area"])
            cv2.putText(
                frame_with_contours,
                f"({cx}, {cy}, {area})",
                (cx, cy + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                2,
                cv2.LINE_4,
            )

        return {
            "mask": mask,
            "image_contours": frame_with_contours,
            "contours": contours,
        }

    def get_color_mask(self, frame):
        """
        Get a mask for detecting objects based on color.

        Args:
            frame (numpy.ndarray): Input image frame.

        Returns:
            numpy.ndarray: Color mask for objects matching the specified HSV values.
        """
        _, mask = self.color_finder.update(frame, self.hsv_vals)
        return mask

    def get_edges(self, frame):
        """
        Detect edges in the input image frame.

        Args:
            frame (numpy.ndarray): Input image frame.

        Returns:
            numpy.ndarray: Image containing detected edges.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.gaussian_kernel, 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges

    def _get_circles_mask(self, frame, best_circle: bool = False):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.gaussian_kernel, 0)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=5,
            maxRadius=50,
        )

        circle_mask = np.zeros_like(gray)
        max_acc = 0
        best_circle_coords = None

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for x, y, r in circles:
                if best_circle:
                    acc = r
                    if acc > max_acc:
                        max_acc = acc
                        best_circle_coords = (x, y, r)
                else:
                    cv2.circle(circle_mask, (x, y), r, 255, -1)

        if best_circle:
            if best_circle_coords is not None:
                x, y, r = best_circle_coords
                cv2.circle(circle_mask, (x, y), r, 255, -1)

        return circle_mask

    def get_circles(self, frame):
        """
        Detect and return circles in the input frame.

        Args:
            frame (numpy.ndarray): Input image frame.

        Returns:
            numpy.ndarray: Mask with detected circles.
        """
        return self._get_circles_mask(frame)

    def get_best_circle(self, frame):
        """
        Detect and return the best circle in the input frame.

        Args:
            frame (numpy.ndarray): Input image frame.

        Returns:
            numpy.ndarray: Mask with the best detected circle.
        """
        return self._get_circles_mask(frame, best_circle=True)