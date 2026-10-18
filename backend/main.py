from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
import csv
import io
import os

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://nutrivision-ai-web.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODEL
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "best_food_model.keras",
)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")

# =========================
# FOOD CLASSES
# =========================

food_classes = [
    "Aloo_matar",
    "Besan_cheela",
    "Biryani",
    "Chapathi",
    "Chole_bature",
    "Dahl",
    "Dhokla",
    "Dosa",
    "Gulab_jamun",
    "Idli",
    "Jalebi",
    "Kadai_paneer",
    "Naan",
    "Paani_puri",
    "Pakoda",
    "Pav_bhaji",
    "Poha",
    "Rolls",
    "Samosa",
    "Vada_pav",
]

# =========================
# LOAD NUTRITION DATA FROM CSV
# =========================

CSV_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "nutrition_dataset.csv",
)

nutrition_data = {}

with open(
    CSV_PATH,
    "r",
    encoding="utf-8-sig",
    newline="",
) as csvfile:
    reader = csv.DictReader(csvfile)

    required_columns = [
        "Food",
        "Calories_kcal",
        "Protein_g",
        "Carbohydrates_g",
        "Fat_g",
        "Fiber_g",
        "Sugar_g",
        "Sodium_mg",
        "Meal_Type",
        "Best_For",
        "Nutrition_Score",
        "Health_Rating",
    ]

    if not reader.fieldnames:
        raise ValueError("The nutrition CSV has no header row.")

    missing_columns = [
        column
        for column in required_columns
        if column not in reader.fieldnames
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in nutrition CSV: {missing_columns}"
        )

    for row in reader:
        food = (row.get("Food") or "").strip()

        if not food:
            continue

        nutrition_data[food] = {
            "calories": float(row["Calories_kcal"]),
            "protein": float(row["Protein_g"]),
            "carbs": float(row["Carbohydrates_g"]),
            "fat": float(row["Fat_g"]),
            "fiber": float(row["Fiber_g"]),
            "sugar": float(row["Sugar_g"]),
            "sodium": float(row["Sodium_mg"]),
            "meal_type": row["Meal_Type"].strip(),
            "best_for": row["Best_For"].strip(),
            "health_score": float(row["Nutrition_Score"]),
            "health_rating": row["Health_Rating"].strip(),
        }

print(f"Loaded nutrition data for {len(nutrition_data)} foods.")

# =========================
# FOOD-SPECIFIC RECOMMENDATIONS
# =========================

recommendations = {
    "Aloo_matar": (
        "Aloo matar provides vegetables and carbohydrates. "
        "Pair it with dal, curd, or paneer for a more balanced meal."
    ),

    "Besan_cheela": (
        "Besan cheela provides protein and works well as a breakfast. "
        "Add vegetables or curd for additional nutritional variety."
    ),

    "Biryani": (
        "Biryani can be calorie-dense. Enjoy a moderate portion "
        "and pair it with raita or a fresh salad."
    ),

    "Chapathi": (
        "Chapathi provides carbohydrates. Pair it with dal, vegetables, "
        "or paneer for a more balanced meal."
    ),

    "Chole_bature": (
        "Chole bhature can be high in calories and fat. "
        "Consider a moderate portion with a fresh salad."
    ),

    "Dahl": (
        "Dal provides plant-based protein and fiber. "
        "Pair it with vegetables and a moderate portion of rice or chapathi."
    ),

    "Dhokla": (
        "Dhokla can be a convenient snack. Pair it with other "
        "nutrient-rich foods to make your meal more balanced."
    ),

    "Dosa": (
        "Dosa provides carbohydrates and energy. "
        "Pair it with sambar for additional protein and vegetables."
    ),

    "Gulab_jamun": (
        "Gulab jamun is high in sugar. Enjoy it occasionally "
        "and keep the portion moderate."
    ),

    "Idli": (
        "Idli is a relatively light option. Pair it with sambar "
        "for additional protein, fiber, and vegetables."
    ),

    "Jalebi": (
        "Jalebi is high in sugar. Enjoy a small portion occasionally "
        "as part of an otherwise balanced diet."
    ),

    "Kadai_paneer": (
        "Kadai paneer provides protein and can also be high in fat. "
        "Pair it with vegetables and a moderate portion of roti."
    ),

    "Naan": (
        "Naan provides carbohydrates. Pair it with a protein-rich curry "
        "and vegetables, and consider a moderate portion."
    ),

    "Paani_puri": (
        "Enjoy paani puri in moderation. For a more filling snack, "
        "consider adding sprouts or another protein-rich side."
    ),

    "Pakoda": (
        "Pakodas are fried and can be high in fat. "
        "Enjoy them occasionally and balance them with other foods."
    ),

    "Pav_bhaji": (
        "Pav bhaji provides vegetables and carbohydrates. "
        "Add extra vegetables and keep the butter and pav portion moderate."
    ),

    "Poha": (
        "Poha provides carbohydrates. Adding peanuts, sprouts, "
        "vegetables, or curd can improve its protein content."
    ),

    "Rolls": (
        "The nutrition of a roll depends on its filling. "
        "Choose vegetable or protein-rich fillings when possible."
    ),

    "Samosa": (
        "Samosas are fried and can be high in fat. "
        "Enjoy them occasionally and keep the serving moderate."
    ),

    "Vada_pav": (
        "Vada pav can be calorie-dense. Enjoy it in moderation "
        "and include vegetables and protein-rich foods in your meals."
    ),
}

# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "NutriVision-AI backend is running",
        "nutrition_food_count": len(nutrition_data),
    }

# =========================
# PREDICT FOOD
# =========================

@app.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    try:
        # Validate file type
        if file.content_type and not file.content_type.startswith("image/"):
            return {"error": "Please upload a valid image file."}

        # Read and process image
        image_bytes = await file.read()

        if not image_bytes:
            return {"error": "The uploaded image is empty."}

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        image = image.resize((224, 224))

        image_array = np.array(
            image,
            dtype=np.float32,
        ) / 255.0

        image_array = np.expand_dims(
            image_array,
            axis=0,
        )

        # Model prediction
        prediction = model.predict(
            image_array,
            verbose=0,
        )

        confidence = float(np.max(prediction))
        predicted_index = int(np.argmax(prediction))

        # Unsupported or uncertain prediction
        if confidence < 0.40:
            return {
                "food": None,
                "confidence": round(confidence, 4),
                "message": "Food not supported or prediction confidence is too low.",
            }

        # Predicted food
        food = food_classes[predicted_index]

        # Look up nutrition in CSV
        nutrition = nutrition_data.get(food)

        if nutrition is None:
            return {
                "food": food,
                "confidence": round(confidence, 4),
                "message": (
                    "Nutrition information is unavailable "
                    "for this food in the dataset."
                ),
            }

        # Dataset-based health score
        health_score = nutrition["health_score"]

        # Food-specific recommendation
        recommendation = recommendations.get(
            food,
            "Enjoy this food as part of a balanced diet.",
        )

        # API response
        return {
            "food": food,
            "confidence": round(confidence, 4),

            "nutrition": {
                "calories": nutrition["calories"],
                "protein": nutrition["protein"],
                "carbs": nutrition["carbs"],
                "fat": nutrition["fat"],
                "fiber": nutrition["fiber"],
                "sugar": nutrition["sugar"],
                "sodium": nutrition["sodium"],
                "health_rating": nutrition["health_rating"],
                "meal_type": nutrition["meal_type"],
                "best_for": nutrition["best_for"],
            },

            "health_score": health_score,
            "recommendation": recommendation,
        }

    except Exception as e:
        print(f"Prediction error: {e}")

        return {
            "error": str(e),
        }
