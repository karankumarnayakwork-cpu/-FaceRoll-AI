# camera.py
import cv2


class Camera:

    def __init__(self, index=0):
        # self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.cap = cv2.VideoCapture(index)

        # Optional buffer reduction for IP cam
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        if not self.cap.isOpened():
            raise Exception("❌ Cannot open camera")

    # def get_frame(self):
    #     ret, frame = self.cap.read()

    #     if not ret:
    #         return None

    #     return frame
    def get_frame(self):
    # Skip buffered frames (reduces lag)
      self.cap.grab()

      ret, frame = self.cap.read()

      if not ret:
        return None

      return frame


    def release(self):
        self.cap.release()

