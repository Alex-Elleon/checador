import os
import cv2
from deepface import DeepFace

def verify_faces(img1_path: str, img2_path: str) -> bool:
    try:
        abs_img1 = os.path.abspath(img1_path)
        abs_img2 = os.path.abspath(img2_path)

        if not os.path.exists(abs_img1) or not os.path.exists(abs_img2):
            print(f"Archivo no encontrado: {abs_img1} o {abs_img2}")
            return False

        # Cargar con OpenCV y convertir de BGR a RGB
        img1 = cv2.imread(abs_img1)
        img2 = cv2.imread(abs_img2)

        if img1 is None or img2 is None:
            print("Error: No se pudo decodificar alguna de las imágenes.")
            return False

        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        # Usar VGG-Face como modelo alternativo de alta compatibilidad y skip de alineación
        result = DeepFace.verify(
            img1_path=img1_rgb,
            img2_path=img2_rgb,
            model_name="VGG-Face",
            detector_backend="skip",  # Evita que el detector falle procesando img1
            enforce_detection=False
        )

        return result.get("verified", False)

    except Exception as e:
        print(f"Error interno en DeepFace: {e}")
        return False