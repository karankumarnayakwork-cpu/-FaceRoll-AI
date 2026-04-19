import cv2


class LivenessDetector:
    """
    Simple liveness:
    If face moves OR blinks naturally → LIVE
    If still photo → NOT LIVE
    """

    def __init__(self):
        self.prev_gray = None
        self.motion_frames = 0

    def check_liveness(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = gray
            return False

        # difference between frames
        diff = cv2.absdiff(self.prev_gray, gray)
        score = diff.mean()

        self.prev_gray = gray

        # if movement detected
        if score > 2:   # threshold
            self.motion_frames += 1

        # after few movements → live
        if self.motion_frames > 5:
            return True

        return False
