import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

class ImageProcessor:
    def __init__(self, hsvVals):
        self.hsvVals = hsvVals
        self.colorFinder = ColorFinder()
        self.KERNEL = (17, 17)

    def get_contours(self, frame, mask, minArea=200):
        imageContours, contours = cvzone.findContours(
            frame, mask, minArea=minArea
        )

        if contours:
            cx, cy = contours[0]["center"]
            area = int(contours[0]["area"])
            cv2.putText(imageContours, f'({cx}, {cy}, {area})', (cx, cy + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_4)
        
        return {
            "mask": mask,
            "imageContours": imageContours,
            "contours": contours
        }
    
    def get_color_mask(self, frame):
        _, mask = self.colorFinder.update(frame, self.hsvVals)
        return mask
    
    def get_edges(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.KERNEL, 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    def _get_circles_mask(self, frame, best_circle=False):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.KERNEL, 0)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50)

        circle_mask = np.zeros_like(gray)
        max_acc = 0
        best_circle_coords = None  # Initialize best_circle_coords here

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                if best_circle:
                    acc = r  # Use radius as an "accumulator" for best circle detection
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
        return self._get_circles_mask(frame)
    
    def get_best_circle(self, frame):
        return self._get_circles_mask(frame, best_circle=True)
