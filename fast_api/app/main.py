from fastapi import FastAPI, File, UploadFile
from app.model import load_image_model
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np

app = FastAPI()

# Assuming you've loaded your image model somewhere
image_model = load_image_model()

# Mocking a simple image model for demonstration
def mock_image_model_predict(image_array):
    # Replace this with your actual prediction logic
    return np.random.rand(1, 12)  # Assuming 12 classes

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        # Read image file
        contents = await file.read()
        
        # Preprocess the image data
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_array = np.array(image.resize((224, 224))) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Make predictions using the loaded model
        predictions = image_model.predict(image_array)


        class_id = np.argmax(predictions, axis=1).item()
        class_names = ["battery", "biological", "brown glass", "clothes", "green glass", "metal", "paper", "plastic", "shoes",
                       "trash", "white glass", "cardboard"]
        # Example code for extracting class probabilities and class name
        class_probabilities = predictions.tolist()[0]
        class_name = class_names[class_id]

        return JSONResponse(content={"class_probabilities": class_probabilities, "class": class_id})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
