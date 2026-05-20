import cv2
import mediapipe as mp
import numpy as np


class AnalyseurClignements:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )

        self.seuil_fermeture = 0.20
        self.oeil_gauche = [33, 160, 158, 133, 153, 144]
        self.oeil_droit = [362, 385, 387, 263, 373, 380]

    def analyser(self, chemin_video: str) -> float:
        video = cv2.VideoCapture(chemin_video)

        nombre_images = 0
        nombre_clignements = 0
        oeil_ferme_avant = False

        while True:
            succes, image = video.read()

            if not succes:
                break

            nombre_images += 1

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            resultats = self.face_mesh.process(image_rgb)

            if not resultats.multi_face_landmarks:
                continue

            landmarks = resultats.multi_face_landmarks[0].landmark

            ouverture_gauche = self.calculer_ouverture_oeil(
                landmarks,
                self.oeil_gauche
            )

            ouverture_droite = self.calculer_ouverture_oeil(
                landmarks,
                self.oeil_droit
            )

            ouverture_moyenne = (ouverture_gauche + ouverture_droite) / 2

            if ouverture_moyenne < self.seuil_fermeture:
                if not oeil_ferme_avant:
                    nombre_clignements += 1
                    oeil_ferme_avant = True
            else:
                oeil_ferme_avant = False

        video.release()

        return self.calculer_score(nombre_clignements, nombre_images)

    def calculer_ouverture_oeil(self, landmarks, indices_oeil) -> float:
        points = []

        for index in indices_oeil:
            point = landmarks[index]
            points.append(np.array([point.x, point.y]))

        gauche = points[0]
        haut_1 = points[1]
        haut_2 = points[2]
        droite = points[3]
        bas_1 = points[4]
        bas_2 = points[5]

        distance_verticale_1 = np.linalg.norm(haut_1 - bas_2)
        distance_verticale_2 = np.linalg.norm(haut_2 - bas_1)
        distance_horizontale = np.linalg.norm(gauche - droite)

        if distance_horizontale == 0:
            return 0

        ouverture = (distance_verticale_1 + distance_verticale_2) / (
            2 * distance_horizontale
        )

        return ouverture

    def calculer_score(self, nombre_clignements: int, nombre_images: int) -> float:
        if nombre_images == 0:
            return 100.0

        duree_estimee_secondes = nombre_images / 30
        clignements_par_minute = (
            nombre_clignements / duree_estimee_secondes
        ) * 60

        if clignements_par_minute < 5:
            return 85.0

        if clignements_par_minute < 10:
            return 60.0

        if clignements_par_minute <= 30:
            return 25.0

        return 70.0