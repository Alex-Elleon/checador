import os
import cv2
import numpy as np

# Ruta donde están los datasets
DATASET_PATH = "uploads"
OUTPUT_MODEL_PATH = "modelo_LBPH.yaml"

def train_model():
    # Inicializar el detector de rostros de OpenCV y el reconocedor LBPH
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    if not os.path.exists(DATASET_PATH):
        print(f"La carpeta '{DATASET_PATH}' no existe.")
        return

    # Recorrer cada subcarpeta (cada carpeta corresponde al employ_number de un usuario)
    for folder_name in os.listdir(DATASET_PATH):
        folder_path = os.path.join(DATASET_PATH, folder_name)

        # Validar que sea un directorio y que el nombre sea un número/ID interpretable
        if os.path.isdir(folder_path):
            try:
                user_id = int(folder_name)  # LBPH requiere etiquetas enteras (int)
            except ValueError:
                continue

            # Leer cada imagen dentro de la carpeta del usuario
            for image_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, image_name)
                
                # Leer en escala de grises (LBPH trabaja solo en escala de grises)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    continue

                # Detectar el rostro en la imagen
                detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in detected_faces:
                    roi = image[y:y+h, x:x+w]  # Recortar solo la región del rostro
                    faces.append(roi)
                    labels.append(user_id)

    if len(faces) == 0:
        print("No se encontraron rostros suficientes para entrenar.")
        return

    # Entrenar el modelo con todas las fotos y etiquetas recolectadas
    print(f"Entrenando modelo con {len(faces)} rostros...")
    recognizer.train(faces, np.array(labels))
    
    # Guardar el archivo YAML actualizado
    recognizer.write(OUTPUT_MODEL_PATH)
    print(f"¡Modelo guardado exitosamente en '{OUTPUT_MODEL_PATH}'!")

if __name__ == "__main__":
    train_model()