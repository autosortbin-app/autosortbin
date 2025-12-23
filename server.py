from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
import random
import tempfile
import os
import threading

import utility.thingspeak_services as srv
from utility.waste_predict import predict_waste
from utility.thingspeak_services import write_bintoopen
from utility.mail_service import send_bin_alert_mail
from utility.settings import settings

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# WRITE (GET only, as requested)
# -----------------------------

@app.get("/bintoopen/set/{value}")
def set_bintoopen(value: int):
    success = srv.write_bintoopen(value)
    return {"bintoopen": value, "success": success}

@app.get("/binfull/set/{value}")
def set_binfull(value: int):

    BIN_CATEGORY_MAP = {
        1: "ewaste",
        2: "glass",
        3: "metal",
        4: "organic",
        5: "paper",
        6: "plastic",
    }

    success = srv.write_binfull(value)

    if not success:
        return "failure"

    if value in BIN_CATEGORY_MAP:
        category = BIN_CATEGORY_MAP[value]

        # ✅ run mail in a separate thread
        threading.Thread(
            target=send_bin_alert_mail,
            kwargs={
                "receiver_email": settings.email_admin,
                "category": category
            },
            daemon=True
        ).start()

    return "success"



# -----------------------------
# READ (latest value)
# -----------------------------

@app.get("/bintoopen")
def get_bintoopen():
    return srv.read_bintoopen()


@app.get("/binfull")
def get_binfull():
    return {"binfull": srv.read_binfull()}


# -----------------------------
# predict and open bin api
# -----------------------------
@app.post("/predict-and-open-bin")
async def predict_and_open_bin(image: UploadFile = File(...)):
    # -----------------------------
    # Save uploaded image temporarily
    # -----------------------------
    suffix = os.path.splitext(image.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await image.read())
        temp_image_path = tmp.name

    # -----------------------------
    # Predict waste category
    # -----------------------------
    predicted_class, confidence = predict_waste(temp_image_path)

    # -----------------------------
    # Encode bin value
    # -----------------------------
    if predicted_class == "ewaste":
        data = 1 * 100 + random.randint(1, 99)
    elif predicted_class == "glass":
        data = 2 * 100 + random.randint(1, 99)
    elif predicted_class == "metal":
        data = 3 * 100 + random.randint(1, 99)
    elif predicted_class == "organic":
        data = 4 * 100 + random.randint(1, 99)
    elif predicted_class == "paper":
        data = 5 * 100 + random.randint(1, 99)
    elif predicted_class == "plastic":
        data = 6 * 100 + random.randint(1, 99)
    else:
        data = 0  # unknown / fallback

    # -----------------------------
    # Update ThingSpeak
    # -----------------------------
    success = write_bintoopen(data)

    # -----------------------------
    # Cleanup temp file
    # -----------------------------
    os.remove(temp_image_path)

    # -----------------------------
    # Response to React
    # -----------------------------
    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "bintoopen_value": data,
        "thingspeak_updated": success
    }
