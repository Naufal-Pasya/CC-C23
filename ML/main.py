import os
import uvicorn
from fastapi import FastAPI, UploadFile
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from google.cloud import storage
from PIL import Image
from io import BytesIO

# Set up GCS client
storage_client = storage.Client()

# GCS bucket and model file paths
bucket_name = "capstone-project-c23.appspot.com"
crop_model_file_path = "Crop/Crop_predict.h5"
fert_model_file_path = "Fertilizer/Fert_predict.h5"
paddy_model_file_path = "Paddy/Paddy_predict.h5"
cotton_model_file_path = "Cotton/modelcotton1_saved.h5"
soil_model_file_path = "Soil_Prediction/model_saved.h5"

# Download the crop model file from GCS
crop_model_blob = storage_client.bucket(bucket_name).blob(crop_model_file_path)
crop_model_path = "/tmp/crop_model.h5"  # Temporary local path to save the crop model file
crop_model_blob.download_to_filename(crop_model_path)

# Download the fertilizer model file from GCS
fert_model_blob = storage_client.bucket(bucket_name).blob(fert_model_file_path)
fert_model_path = "/tmp/fert_model.h5"  # Temporary local path to save the fertilizer model file
fert_model_blob.download_to_filename(fert_model_path)

# Download the paddy model file from GCS
paddy_model_blob = storage_client.bucket(bucket_name).blob(paddy_model_file_path)
paddy_model_path = "/tmp/paddy_model.h5"  # Temporary local path to save the paddy model file
paddy_model_blob.download_to_filename(paddy_model_path)

# Download the cotton model file from GCS
cotton_model_blob = storage_client.bucket(bucket_name).blob(cotton_model_file_path)
cotton_model_path = "/tmp/cotton_model.h5"  # Temporary local path to save the cotton model file
cotton_model_blob.download_to_filename(cotton_model_path)

# Download the soil model file from GCS
soil_model_blob = storage_client.bucket(bucket_name).blob(soil_model_file_path)
soil_model_path = "/tmp/soil_model.h5"  # Temporary local path to save the soil model file
soil_model_blob.download_to_filename(soil_model_path)

# Load the crop model
crop_model = load_model(crop_model_path)

# Load the fertilizer model
fert_model = load_model(fert_model_path)

# Load the paddy model
paddy_model = load_model(paddy_model_path)

# Load the cotton model
cotton_model = load_model(cotton_model_path)

# Load the soil model
soil_model = load_model(soil_model_path)

# Load the crop label encoder
crop_label_encoder = LabelEncoder()
crop_label_encoder.classes_ = np.load("crop_recommend_name.npy", allow_pickle=True)

# Load the fertilizer label encoder
fert_label_encoder = LabelEncoder()
fert_label_encoder.classes_ = np.load("fert_recommend_name.npy", allow_pickle=True)

# Define the class labels for paddy prediction
paddy_class_labels = ['hispa', 'paddy_blast','paddy_blight','paddy_normal','paddy_tungro'] 

# Define the class labels for cotton prediction
cotton_class_labels = ['Target spot', 'Powdery Mildew', 'Healthy', 'Bacterial Blight', 'Army worm'] 

# Define the class labels for soil prediction
soil_class_labels = ['01-Aluvial', '02-Andosol', '03-Entisol', '04-Humus', '05-Inceptisol', '06-Laterit', '07-Kapur', '08-Pasir'] 

# Create the FastAPI app
app = FastAPI()

# Define the crop prediction endpoint
@app.post("/predict/crop")
def predict_crop(data: dict):
    # Extract the features from the request data
    features = np.array(data["features"]).reshape(1, -1)

    # Preprocess the features if needed (e.g., scaling, encoding)

    # Make the prediction using the crop model
    prediction = crop_model.predict(features)
    predicted_label = np.argmax(prediction, axis=-1)

    # Postprocess the prediction if needed
    predicted_crop = crop_label_encoder.inverse_transform(predicted_label)[0]

    # Convert predicted_crop to a regular string
    predicted_crop = str(predicted_crop)

    # Return the prediction as a JSON response
    return {"predicted_crop": predicted_crop}

# Define the fertilizer prediction endpoint
@app.post("/predict/fert")
def predict_fert(data: dict):
    # Extract the features from the request data
    features = np.array(data["features"]).reshape(1, -1)

    # Preprocess the features if needed (e.g., scaling, encoding)

    # Make the prediction using the fertilizer model
    prediction = fert_model.predict(features)
    predicted_label = np.argmax(prediction, axis=-1)

    # Postprocess the prediction if needed
    predicted_fert = fert_label_encoder.inverse_transform(predicted_label)[0]

    # Convert predicted_fert to a regular string
    predicted_fert = str(predicted_fert)

    # Return the prediction as a JSON response
    return {"predicted_fert": predicted_fert}

# Define the paddy prediction endpoint
@app.post("/predict/paddy")
async def predict_paddy(image: UploadFile):
    # Read the uploaded image file
    contents = await image.read()

    # Process the image and make the prediction using the paddy model
    img = Image.open(BytesIO(contents))
    img = img.resize((128, 128))  # Resize the image to match the expected input shape
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize the pixel values

    # Add batch dimension to the image array
    img_array = np.expand_dims(img_array, axis=0)

    # Make the prediction using the paddy model
    prediction = paddy_model.predict(img_array)
    predicted_label = np.argmax(prediction, axis=-1)

    # Get the predicted class label
    predicted_class = paddy_class_labels[predicted_label[0]]

    # Convert predicted_class to a regular string
    predicted_class = str(predicted_class)

    # Return the prediction as a JSON response
    return {"predicted_class": predicted_class}

@app.post("/predict/cotton")
async def predict_cotton(image: UploadFile):
    # Read the uploaded image file
    contents = await image.read()

    # Process the image and make the prediction using the fifth model
    img = Image.open(BytesIO(contents))
    img = img.resize((224, 224))  # Resize the image to match the expected input shape
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize the pixel values

    # Add batch dimension to the image array
    img_array = np.expand_dims(img_array, axis=0)

    # Make the prediction using the fifth model
    prediction = cotton_model.predict(img_array)
    predicted_label = np.argmax(prediction, axis=-1)

    # Get the predicted class label
    predicted_class = cotton_class_labels[predicted_label[0]]

    # Convert predicted_class to a regular string
    predicted_class = str(predicted_class)

    # Return the prediction as a JSON response
    return {"predicted_class": predicted_class}

    # Define the fourth prediction endpoint
@app.post("/predict/soil")
async def predict_soil(image: UploadFile):
    # Read the uploaded image file
    contents = await image.read()

    # Process the image and make the prediction using the fourth model
    img = Image.open(BytesIO(contents))
    img = img.resize((224, 224))  # Resize the image to match the expected input shape
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize the pixel values

    # Add batch dimension to the image array
    img_array = np.expand_dims(img_array, axis=0)

    # Make the prediction using the fourth model
    prediction = soil_model.predict(img_array)
    predicted_label = np.argmax(prediction, axis=-1)

    # Get the predicted class label
    predicted_class = soil_class_labels[predicted_label[0]]

    # Convert predicted_class to a regular string
    predicted_class = str(predicted_class)

    # Return the prediction as a JSON response
    return {"predicted_class": predicted_class}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
