from fastapi import FastAPI, File, UploadFile
from app.model import load_image_model
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import tensorflow as tf

app = FastAPI()

# Assuming you've loaded your image model somewhere
image_model = load_image_model()

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        
        # Read image file
        contents = await file.read()
        # Save the image file temporarily
        # with open(file.filename, "wb") as image_file:
        #     image_file.write(contents)
        
        # Preprocess the image data
        img = tf.keras.preprocessing.image.load_img(io.BytesIO(contents), target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.array([img_array])

        # Make predictions using the loaded model
        predictions = image_model.predict(img_array)


        class_id = np.argmax(predictions, axis=1).item()
        # define classes name
        class_names = [ "battery",
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
                        "white-glass"]

        # Extracting class probabilities and class name
        class_probabilities = predictions.tolist()[0]
        class_name = class_names[class_id]

        return JSONResponse(content={"class_probabilities": class_probabilities,"class": class_name})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
