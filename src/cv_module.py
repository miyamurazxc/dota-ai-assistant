import cv2
import easyocr
from typing import List


class CVHeroExtractor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, image_path: str) -> List[str]:
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Image not found")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        results = self.reader.readtext(gray)

        detected_words = []

        for (_, text, confidence) in results:
            if confidence > 0.4:
                detected_words.append(text)

        return detected_words