from tensorflow.keras.models import load_model

def load_image_model():
    # Load your trained model
    model = load_model('./model_weights/my_model.keras')
    return model
