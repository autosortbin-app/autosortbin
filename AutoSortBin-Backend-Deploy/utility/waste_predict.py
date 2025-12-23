import numpy as np
from PIL import Image

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

# -----------------------------
# Load TFLite model (once)
# -----------------------------
MODEL_PATH = "utility/predictWaste12.tflite"

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# -----------------------------
# Class definitions
# -----------------------------
OUTPUT_CLASSES = [
    "battery",
    "biological",
    "brown-glass",
    "cardboard",
    "clothes",
    "green-glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash",
    "white-glass",
]

CLASS_MAPPING = {
    "battery": "ewaste",
    "biological": "organic",
    "brown-glass": "glass",
    "cardboard": "paper",
    "clothes": "organic",
    "green-glass": "glass",
    "metal": "metal",
    "paper": "paper",
    "plastic": "plastic",
    "shoes": "organic",
    "trash": "organic",
    "white-glass": "glass",
}


# -----------------------------
# Prediction function
# -----------------------------
def predict_waste(image_path: str) -> tuple[str, float]:
    """
    Predict waste category from image.

    Returns:
        (merged_class, confidence_percentage)
    """

    # Load & preprocess image (MUST match training)
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]["index"], img_array)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]["index"])

    class_index = int(np.argmax(predictions))
    confidence = round(float(np.max(predictions)) * 100, 2)

    raw_class = OUTPUT_CLASSES[class_index]
    merged_class = CLASS_MAPPING.get(raw_class, "unknown")

    return merged_class, confidence
