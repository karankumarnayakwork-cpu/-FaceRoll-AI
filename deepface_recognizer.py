
from deepface import DeepFace
import numpy as np
import os
import cv2


class DeepFaceRecognizer:

    def __init__(self, db_path="dataset"):
        self.db_path = db_path
        self.embeddings = []
        self.names = []

        self.load_faces()


    # --------------------------------
    # ⭐ LOAD + CACHE EMBEDDINGS
    # --------------------------------
    def load_faces(self):

        self.embeddings = []
        self.names = []

        print("Loading faces from dataset...")

        for person in os.listdir(self.db_path):

            person_path = os.path.join(self.db_path, person)

            if not os.path.isdir(person_path):
                continue

            for img_name in os.listdir(person_path):

                img_path = os.path.join(person_path, img_name)

                embedding = DeepFace.represent(
                    img_path=img_path,
                    model_name="Facenet512",
                    enforce_detection=False
                )[0]["embedding"]

                self.embeddings.append(np.array(embedding))
                self.names.append(person)

        print("Loaded:", self.names)


    # --------------------------------
    # FAST RECOGNITION
    # --------------------------------
    def recognize(self, frame):

        if len(self.embeddings) == 0:
            return "Unknown"

        embedding = DeepFace.represent(
            img_path=frame,
            model_name="Facenet512",
            enforce_detection=False
        )[0]["embedding"]

        embedding = np.array(embedding)

        min_dist = 999
        identity = "Unknown"

        for db_emb, name in zip(self.embeddings, self.names):

            dist = np.linalg.norm(db_emb - embedding)

            if dist < min_dist:
                min_dist = dist
                identity = name

        # threshold tuning
        if min_dist < 10:
            return identity

        return "Unknown"
