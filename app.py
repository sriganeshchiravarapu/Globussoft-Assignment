from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import shutil
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Face Authentication API Running"}

@app.post("/verify-faces")
async def verify_faces(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    img1_path = "img1.jpg"
    img2_path = "img2.jpg"

    with open(img1_path, "wb") as buffer:
        shutil.copyfileobj(image1.file, buffer)

    with open(img2_path, "wb") as buffer:
        shutil.copyfileobj(image2.file, buffer)

    verification = DeepFace.verify(
        img1_path,
        img2_path,
        model_name="Facenet"
    )

    face1 = DeepFace.extract_faces(
        img_path=img1_path,
        detector_backend="opencv"
    )

    face2 = DeepFace.extract_faces(
        img_path=img2_path,
        detector_backend="opencv"
    )

    bbox1 = face1[0]["facial_area"] if face1 else {}
    bbox2 = face2[0]["facial_area"] if face2 else {}

    os.remove(img1_path)
    os.remove(img2_path)

    return {
        "verification_result":
            "same person"
            if verification["verified"]
            else "different person",

        "similarity_score":
            round(1 - verification["distance"], 4),

        "bounding_boxes": {
            "image1": bbox1,
            "image2": bbox2
        }
    }