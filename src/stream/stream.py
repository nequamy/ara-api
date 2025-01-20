import cv2
import numpy as np

class Stream(object):
    def __init__(self, mode: str = None):
        self.cap = None
        self.ids = None
        self.url = "http://192.168.2.113:81/stream"
        self.mode = mode

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = cv2.aruco.DetectorParameters()

    def stream(self):
        self.cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():
            print("Ошибка: Не удалось открыть поток видео.")
            exit()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Ошибка: Не удалось получить кадр.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            corners, self.ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict,
                                                                           parameters=self.parameters)
        
            
        self.cap.release()
        cv2.destroyAllWindows()

    def get_id(self):
        return self.ids

stream = Stream()
stream.stream()