from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
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
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODEL
# =========================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "best_food_model.keras"
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
    "Vada_pav"
]

# =========================
# NUTRITION DATA
# =========================

nutrition_data = {

    "Aloo_matar": {
        "calories": 180,
        "protein": 5,
        "carbs": 25,
        "fat": 7
    },

    "Besan_cheela": {
        "calories": 170,
        "protein": 7,
        "carbs": 20,
        "fat": 7
    },

    "Biryani": {
        "calories": 300,
        "protein": 9,
        "carbs": 45,
        "fat": 9
    },

    "Chapathi": {
        "calories": 120,
        "protein": 3,
        "carbs": 18,
        "fat": 3
    },

    "Chole_bature": {
        "calories": 450,
        "protein": 12,
        "carbs": 60,
        "fat": 18
    },

    "Dahl": {
        "calories": 180,
        "protein": 9,
        "carbs": 25,
        "fat": 5
    },

    "Dhokla": {
        "calories": 160,
        "protein": 6,
        "carbs": 25,
        "fat": 4
    },

    "Dosa": {
        "calories": 170,
        "protein": 4,
        "carbs": 28,
        "fat": 5
    },

    "Gulab_jamun": {
        "calories": 150,
        "protein": 2,
        "carbs": 22,
        "fat": 6
    },

    "Idli": {
        "calories": 60,
        "protein": 2,
        "carbs": 12,
        "fat": 0.5
    },

    "Jalebi": {
        "calories": 150,
        "protein": 1,
        "carbs": 25,
        "fat": 5
    },

    "Kadai_paneer": {
        "calories": 300,
        "protein": 15,
        "carbs": 12,
        "fat": 22
    },

    "Naan": {
        "calories": 260,
        "protein": 8,
        "carbs": 45,
        "fat": 6
    },

    "Paani_puri": {
        "calories": 180,
        "protein": 4,
        "carbs": 28,
        "fat": 6
    },

    "Pakoda": {
        "calories": 250,
        "protein": 5,
        "carbs": 25,
        "fat": 14
    },

    "Pav_bhaji": {
        "calories": 300,
        "protein": 8,
        "carbs": 40,
        "fat": 12
    },

    "Poha": {
        "calories": 180,
        "protein": 4,
        "carbs": 30,
        "fat": 5
    },

    "Rolls": {
        "calories": 280,
        "protein": 10,
        "carbs": 35,
        "fat": 11
    },

    "Samosa": {
        "calories": 260,
        "protein": 5,
        "carbs": 30,
        "fat": 14
    },

    "Vada_pav": {
        "calories": 290,
        "protein": 7,
        "carbs": 40,
        "fat": 12
    }
}

# =========================
# FOOD-SPECIFIC RECOMMENDATIONS
# =========================

recommendations = {

    "Aloo_matar":
        "Aloo matar provides vegetables and carbohydrates. Pair it with a protein-rich side such as dal, curd, or paneer for a more balanced meal.",

    "Besan_cheela":
        "Besan cheela is a good protein-rich breakfast option. Add vegetables or curd to increase its nutritional balance.",

    "Biryani":
        "Biryani is relatively calorie-dense. Enjoy a moderate portion and pair it with raita or a fresh salad for a more balanced meal.",

    "Chapathi":
        "Chapathi is a lighter carbohydrate source. Pair it with dal, vegetables, or paneer to increase protein and overall nutritional balance.",

    "Chole_bature":
        "Chole bhature is high in calories and fat. Enjoy it occasionally and consider a smaller portion with a fresh salad.",

    "Dahl":
        "Dal is a good source of plant-based protein and carbohydrates. Pair it with vegetables and a moderate portion of rice or chapathi.",

    "Dhokla":
        "Dhokla is a relatively light snack. Pair it with vegetables or another protein source for a more complete meal.",

    "Dosa":
        "Dosa provides carbohydrates and energy. Pair it with sambar and vegetables to increase protein and micronutrients.",

    "Gulab_jamun":
        "Gulab jamun is a sweet treat that is high in sugar. Enjoy it occasionally and keep the portion moderate.",

    "Idli":
        "Idli is a light and relatively low-calorie option. Pair it with sambar for additional protein, fiber, and vegetables.",

    "Jalebi":
        "Jalebi is high in sugar and should be enjoyed occasionally. Keep the serving small and balance it with nutrient-rich foods.",

    "Kadai_paneer":
        "Kadai paneer provides a good amount of protein but can also be high in fat. Pair it with vegetables and a moderate portion of roti.",

    "Naan":
        "Naan is a calorie-dense carbohydrate source. Pair it with a protein-rich curry and vegetables, and consider a moderate portion.",

    "Paani_puri":
        "Paani puri can be enjoyed as an occasional snack. Keep the portion moderate and include healthier foods throughout the rest of the meal.",

    "Pakoda":
        "Pakodas are fried and relatively high in fat. Enjoy them occasionally and consider pairing them with vegetables or a lighter meal.",

    "Pav_bhaji":
        "Pav bhaji provides vegetables and carbohydrates. Add extra vegetables and keep the butter and pav portion moderate.",

    "Poha":
        "Poha is a light carbohydrate-rich meal. Adding peanuts, sprouts, vegetables, or curd can improve its protein content.",

    "Rolls":
        "Rolls can provide protein depending on the filling but may be calorie-dense. Choose vegetable or lean-protein fillings when possible.",

    "Samosa":
        "Samosas are fried and relatively high in fat. Enjoy them occasionally and keep the serving moderate.",

    "Vada_pav":
        "Vada pav is a calorie-dense snack. Enjoy it occasionally and balance it with vegetables and protein-rich foods."
}

# =========================
# HEALTH SCORE
# =========================

def calculate_health_score(calories, protein, carbs, fat):

    score = 100

    if calories > 400:
        score -= 20
    elif calories > 300:
        score -= 10

    if fat > 20:
        score -= 20
    elif fat > 15:
        score -= 10

    if carbs > 50:
        score -= 10

    if protein >= 10:
        score += 5

    return max(0, min(100, score))


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "NutritionAI Backend is running"
    }


# =========================
# PREDICT FOOD
# =========================

@app.post("/predict")
async def predict_food(file: UploadFile = File(...)):

    try:

        # Read image
        image_bytes = await file.read()

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        # Resize
        image = image.resize((224, 224))

        # Convert to array
        image_array = np.array(image) / 255.0

        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # Prediction
        prediction = model.predict(
            image_array,
            verbose=0
        )

        confidence = float(np.max(prediction))

        predicted_index = int(
            np.argmax(prediction)
        )

        # Unsupported food
        if confidence < 0.40:

            return {
                "food": None,
                "confidence": round(confidence, 4),
                "message": "Food not supported"
            }

        # Food name
        food = food_classes[predicted_index]

        # Nutrition
        nutrition = nutrition_data.get(food)

        if nutrition is None:

            return {
                "food": food,
                "confidence": round(confidence, 4),
                "message": "Nutrition information unavailable"
            }

        # Health score
        health_score = calculate_health_score(
            nutrition["calories"],
            nutrition["protein"],
            nutrition["carbs"],
            nutrition["fat"]
        )

        # Food-specific recommendation
        recommendation = recommendations.get(
            food,
            "Enjoy this food as part of a balanced diet."
        )

        # Final response
        return {

            "food": food,

            "confidence": round(
                confidence,
                4
            ),

            "nutrition": {
                "calories": nutrition["calories"],
                "protein": nutrition["protein"],
                "carbs": nutrition["carbs"],
                "fat": nutrition["fat"]
            },

            "health_score": health_score,

            "recommendation": recommendation
        }

    except Exception as e:

        return {
            "error": str(e)
        }