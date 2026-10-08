import os
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "best_food_model.keras"
)

NUTRITION_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "nutrition_dataset.csv"
)


# ============================================================
# FOOD CLASSES
# ============================================================

FOOD_CLASSES = [
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


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading NutriVision AI model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# LOAD NUTRITION DATASET
# ============================================================

print("Loading nutrition dataset...")

nutrition_df = pd.read_csv(NUTRITION_PATH)

print("Nutrition dataset loaded successfully.")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_food(image_path, confidence_threshold=0.60):
    """
    Predict the food class from an image.

    Returns:
        food_name
        confidence
    """

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Resize to model input size
    image = image.resize((224, 224))

    # Convert to NumPy array
    image_array = np.array(image).astype("float32") / 255.0

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Model prediction
    prediction = model.predict(
        image_array,
        verbose=0
    )

    # Highest probability
    predicted_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    # Make sure index is valid
    if predicted_index >= len(FOOD_CLASSES):
        return None, confidence

    food_name = FOOD_CLASSES[predicted_index]

    # Unsupported image handling
    if confidence < confidence_threshold:
        return None, confidence

    return food_name, confidence


# ============================================================
# NUTRITION LOOKUP
# ============================================================

def get_nutrition(food_name):
    """
    Find nutrition information for the predicted food.
    """

    result = nutrition_df[
        nutrition_df["Food"].str.lower() == food_name.lower()
    ]

    if result.empty:
        return None

    # Convert first matching row into dictionary
    nutrition = result.iloc[0].to_dict()

    # Convert NumPy values to normal Python values
    cleaned = {}

    for key, value in nutrition.items():

        if pd.isna(value):
            cleaned[key] = None

        elif isinstance(value, np.generic):
            cleaned[key] = value.item()

        else:
            cleaned[key] = value

    return cleaned


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendation(food_name, nutrition):
    """
    Generate simple rule-based dietary recommendations.
    """

    recommendations = []

    if nutrition is None:
        return recommendations

    calories = float(nutrition.get("Calories_kcal", 0))
    protein = float(nutrition.get("Protein_g", 0))
    fiber = float(nutrition.get("Fiber_g", 0))
    sugar = float(nutrition.get("Sugar_g", 0))
    health_score = float(nutrition.get("Nutrition_Score", 0))

    meal_type = str(
        nutrition.get("Meal_Type", "")
    )

    best_for = str(
        nutrition.get("Best_For", "")
    )

    # Calories
    if calories <= 250:
        recommendations.append(
            "Light meal with relatively low calories."
        )

    elif calories >= 500:
        recommendations.append(
            "High-calorie food; consider a moderate portion."
        )

    else:
        recommendations.append(
            "Moderate-calorie food suitable as part of a balanced meal."
        )

    # Protein
    if protein < 8:
        recommendations.append(
            "Pair with a protein-rich food such as curd, paneer, eggs, or dal."
        )

    else:
        recommendations.append(
            "Provides a useful amount of protein."
        )

    # Fiber
    if fiber < 3:
        recommendations.append(
            "Consider pairing it with vegetables, salad, or another fiber-rich food."
        )

    # Sugar
    if sugar >= 20:
        recommendations.append(
            "High in sugar; best consumed occasionally and in a small portion."
        )

    # Health score
    if health_score >= 85:
        recommendations.append(
            "Good nutritional profile for regular consumption."
        )

    elif health_score < 50:
        recommendations.append(
            "Better consumed occasionally rather than as a regular food choice."
        )

    # Meal type
    if meal_type:
        recommendations.append(
            f"Best consumed during {meal_type}."
        )

    # Best for
    if best_for:
        recommendations.append(
            f"Suitable for: {best_for}."
        )

    return recommendations


# ============================================================
# COMPLETE PREDICTION + NUTRITION FUNCTION
# ============================================================
def predict_food_with_nutrition(image_path, confidence_threshold=0.60):

    food, confidence = predict_food(image_path, confidence_threshold)

    # Unsupported / low-confidence food
    if food is None:
        return {
            "food": None,
            "confidence": confidence,
            "nutrition": None,
            "health_score": None,
            "recommendation": None,
            "supported": False,
            "message": "Food not supported"
        }

    # Get nutrition data from CSV
    nutrition = get_nutrition(food)

    if nutrition is None:
        return {
            "food": food,
            "confidence": confidence,
            "nutrition": None,
            "health_score": None,
            "recommendation": None,
            "supported": False,
            "message": "Nutrition information not available"
        }

    # Convert CSV column names to the names expected by React
    frontend_nutrition = {
        "calories": nutrition.get("Calories_kcal"),
        "protein": nutrition.get("Protein_g"),
        "carbs": nutrition.get("Carbohydrates_g"),
        "fat": nutrition.get("Fat_g"),
        "fiber": nutrition.get("Fiber_g"),
        "sugar": nutrition.get("Sugar_g"),
        "sodium": nutrition.get("Sodium_mg"),
        "serving_size": nutrition.get("Serving_Size"),
        "meal_type": nutrition.get("Meal_Type"),
        "best_for": nutrition.get("Best_For"),
        "allergens": nutrition.get("Allergens"),
        "description": nutrition.get("Description")
    }

    # Nutrition score is already 0–100 in the CSV
    health_score = nutrition.get("Nutrition_Score")

    # Generate recommendations
    recommendations = generate_recommendation(food, nutrition)

    # Convert list to one string because React displays one paragraph
    recommendation_text = " ".join(recommendations)

    return {
        "food": food,
        "confidence": confidence,
        "nutrition": frontend_nutrition,
        "health_score": health_score,
        "recommendation": recommendation_text,
        "supported": True
    }