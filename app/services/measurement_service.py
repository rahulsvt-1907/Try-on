import cv2
import numpy as np


class MeasurementService:
    def estimate_size(self, image_bytes: bytes) -> tuple[str, float]:
        array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if image is None:
            return 'M', 0.3

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 'M', 0.35

        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        ratio = w / max(h, 1)

        if ratio < 0.35:
            return 'S', 0.62
        if ratio < 0.5:
            return 'M', 0.72
        if ratio < 0.65:
            return 'L', 0.74
        return 'XL', 0.66
