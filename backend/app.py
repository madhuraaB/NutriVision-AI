import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_food_with_nutrition


app = FastAPI(
    title="NutriVision AI",
    description="Indian Food Recognition and Nutrition Analysis API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://nutrivision-ai-k18lw931o-bhuvadmadhura982-4419s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "NutriVision AI Backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict_food_endpoint(
    file: UploadFile = File(...)
):
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp"
    ]

    if file.content_type not in allowed_types:
        return {
            "error": "Please upload a valid image file."
        }

    suffix = os.path.splitext(file.filename)[1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_path = temp_file.name
    temp_file.close()

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_food_with_nutrition(temp_path)

        return result

    except Exception as e:
        print("Prediction error:", repr(e))

        return {
            "error": str(e)
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)