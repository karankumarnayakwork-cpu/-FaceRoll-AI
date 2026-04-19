
import cv2
import os
import time
from deepface import DeepFace

class FaceRegistrar:

    def __init__(self, dataset_path="dataset", total_images=5):
        self.dataset_path = dataset_path
        self.total_images = total_images
        os.makedirs(self.dataset_path, exist_ok=True)

    def register(self, cam):
        name = input("Enter name: ").strip()
        phone = input("Enter phone number: ").strip()

        person_id = f"{name}_{phone}"
        person_dir = os.path.join(self.dataset_path, person_id)

        if os.path.exists(person_dir):
            print("❌ Person already registered")
            return

        os.makedirs(person_dir)
        print("📸 Registration started (press C to capture)")

        instructions = [
            "Look STRAIGHT",
            "Turn LEFT",
            "Turn RIGHT",
            "Look UP",
            "Smile / Neutral"
        ]

        captured = 0

        while captured < self.total_images:
            frame = cam.get_frame()
            if frame is None:
                continue

            cv2.putText(
                frame,
                instructions[captured],
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow("Face Registration", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("c"):
                try:
                    faces = DeepFace.extract_faces(
                        img_path=frame,
                        detector_backend="retinaface",
                        enforce_detection=True
                    )

                    face_img = faces[0]["face"]
                    save_path = os.path.join(
                        person_dir, f"img{captured+1}.jpg"
                    )

                    cv2.imwrite(save_path, face_img)
                    captured += 1
                    print(f"✅ Captured {captured}/{self.total_images}")
                    time.sleep(0.7)

                except Exception:
                    print("⚠️ Face not detected properly")

            elif key == ord("q"):
                break

        cv2.destroyWindow("Face Registration")
        print("🎉 Registration completed successfully")
