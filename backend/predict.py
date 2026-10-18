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
    recommendations = []

    if nutrition is None:
        return recommendations

    # Read nutrition values
    calories = float(nutrition.get("Calories_kcal", 0) or 0)
    protein = float(nutrition.get("Protein_g", 0) or 0)
    fiber = float(nutrition.get("Fiber_g", 0) or 0)
    sugar = float(nutrition.get("Sugar_g", 0) or 0)
    fat = float(nutrition.get("Fat_g", 0) or 0)
    sodium = float(nutrition.get("Sodium_mg", 0) or 0)
    health_score = float(nutrition.get("Nutrition_Score", 0) or 0)

    meal_type = str(nutrition.get("Meal_Type", "") or "")
    best_for = str(nutrition.get("Best_For", "") or "")

    # Food-specific recommendations
    food_advice = {
        "Aloo_matar": [
            "Pair with chapathi for a balanced lunch or dinner.",
            "Its peas provide fiber and some plant-based protein."
        ],
        "Besan_cheela": [
            "A protein-containing breakfast option made with gram flour.",
            "Pair with curd or vegetables for a more varied meal."
        ],
        "Biryani": [
            "Consider a moderate portion and pair with raita or vegetables.",
            "The recipe and cooking method can significantly affect its nutrition."
        ],
        "Chapathi": [
            "Pair with dal, chickpeas, or paneer to increase meal protein.",
            "Add vegetables to make the meal more balanced."
        ],
        "Chole_bature": [
            "Enjoy a smaller portion if you are limiting calories or fat.",
            "Pair with a vegetable salad and choose less oily accompaniments."
        ],
        "Dahl": [
            "A useful source of plant-based protein and fiber.",
            "Pair with chapathi or rice and vegetables for a balanced meal."
        ],
        "Dhokla": [
            "A steamed snack option that can fit into a balanced diet.",
            "Pair with fruit or another protein-rich food if needed."
        ],
        "Dosa": [
            "Pair with sambar for additional protein and fiber.",
            "Consider the oil and chutney portions when planning your meal."
        ],
        "Gulab_jamun": [
            "Enjoy occasionally in a small portion; this serving contains substantial sugar.",
            "Balance sweet treats with nutrient-rich foods throughout the day."
        ],
        "Idli": [
            "A steamed breakfast option that is relatively low in calories per listed serving.",
            "Pair with sambar to add protein and fiber."
        ],
        "Jalebi": [
            "Enjoy occasionally in a small portion because this serving is high in sugar.",
            "Choose water or an unsweetened drink alongside it."
        ],
        "Kadai_paneer": [
            "Paneer contributes protein to the meal.",
            "Pair with vegetables and a moderate portion of chapathi or naan."
        ],
        "Naan": [
            "Pair with dal, chickpeas, or paneer to add protein.",
            "Consider the portion size, particularly when eating it with rich curries."
        ],
        "Paani_puri": [
            "Enjoy in moderation; this serving contains 325 kcal according to the dataset.",
            "For a more filling snack, consider adding sprouts or another protein-rich side."
        ],
        "Pakoda": [
            "Enjoy in moderation because deep-frying contributes to its fat content.",
            "Pair with a fresh vegetable side rather than making fried snacks the main meal."
        ],
        "Pav_bhaji": [
            "The vegetable mixture provides fiber.",
            "Consider the butter and bread portions if you are limiting added fat or calories."
        ],
        "Poha": [
            "A convenient breakfast option that provides carbohydrates and some fiber.",
            "Adding peas or serving it with curd can increase protein."
        ],
        "Rolls": [
            "The filling affects the protein and overall nutritional value.",
            "Choose a vegetable-rich filling and pair with a salad when available."
        ],
        "Samosa": [
            "Enjoy occasionally or choose a smaller portion if you are limiting calories or fat.",
            "Pair with a fresh vegetable side for a more balanced snack."
        ],
        "Vada_pav": [
            "Enjoy in moderation as this serving contains 375 kcal according to the dataset.",
            "Pair with fruit or vegetables and consider the added chutneys and fried portion."
        ]
    }

    # Add food-specific advice
    recommendations.extend(food_advice.get(food_name, []))

    # Add recommendations based on the nutrition values
    if calories >= 500:
        recommendations.append(
            "This serving is relatively high in calories; consider portion size."
        )
    elif calories <= 200:
        recommendations.append(
            "This serving is relatively low in calories compared with many meals."
        )

    if protein < 8:
        recommendations.append(
            "Consider adding a protein-rich food such as dal, curd, paneer, or eggs."
        )

    if fiber < 3:
        recommendations.append(
            "Add vegetables, fruit, or another fiber-rich food to your meal."
        )

    if sugar >= 20:
        recommendations.append(
            "This serving is high in sugar; consider a smaller portion."
        )

    if sodium >= 600:
        recommendations.append(
            "This serving contains relatively high sodium; consider lower-sodium accompaniments."
        )

    if health_score >= 85:
        recommendations.append(
            "The dataset rates this food highly for nutrition."
        )
    elif health_score < 50:
        recommendations.append(
            "The dataset gives this food a low nutrition score, so consider having it occasionally."
        )

    if meal_type:
        recommendations.append(f"Meal suggestion: {meal_type}.")

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