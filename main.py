import cv2
from camera import Camera
from deepface_recognizer import DeepFaceRecognizer
from liveness import LivenessDetector
from attendance import AttendanceLogger
from register import FaceRegistrar
from deepface import DeepFace





def main():

    cam = Camera()
    recognizer = DeepFaceRecognizer()
    liveness = LivenessDetector()
    attendance = AttendanceLogger()
    registrar = FaceRegistrar()




    print("✅ DeepFace Recognition Started")
    print("Press q to quit")

    while True:

      frame = cam.get_frame()

      if frame is None:
        continue

      is_live = liveness.check_liveness(frame)
      faces = DeepFace.extract_faces(
        img_path=frame,
        enforce_detection=False,
        detector_backend="opencv"
      )

      label = "NOT LIVE"   # default

      if is_live:
        # ⭐ speed optimization
        small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        name = recognizer.recognize(small)
        if name != "Unknown":
          attendance.log(name)
        label = "LIVE - " + name

      # ⭐⭐⭐ PUT YOUR BOX CODE HERE ⭐⭐⭐
      for face in faces:
        x = face["facial_area"]["x"]
        y = face["facial_area"]["y"]
        w = face["facial_area"]["w"]
        h = face["facial_area"]["h"]

        if label == "NOT LIVE":
         color = (0, 255, 255) 
        elif "Unknown" in label:
         color = (0, 0, 255)
        else:
         color = (0, 255, 0)  

        cv2.rectangle(frame, (x, y), (x+w, y+h), color , 2)

      cv2.putText(
            frame,
            label,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )
     # ⭐ show AFTER drawing
      cv2.imshow("DeepFace Recognition", frame)
      


      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
       break

      # ⭐ NEW — press R to register
      elif key == ord("r"):
       registrar.register(cam)

      # reload recognizer so new face works immediately
       recognizer.load_faces()


    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
