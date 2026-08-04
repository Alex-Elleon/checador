import os
from deepface import DeepFace

MODEL_NAME = "Facenet"
DETECTOR_BACKEND = "opencv"

def verify_faces(img1_path: str, img2_path: str) -> bool:
    """
    Compara dos imágenes de rostros.
    Retorna True si son la misma persona, False en caso contrario.
    """
    try:
        # Verificar que existan las rutas de las fotos
        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            return False

        # Comparación biométrica con DeepFace
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True # Lanza excepción si no hay rostro visible
        )

        return result.get("verified", False)

    except Exception as e:
        print(f"Error en validación biométrica: {str(e)}")
        return False