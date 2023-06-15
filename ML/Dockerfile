FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV GCS_BUCKET_NAME="capstone-project-c23.appspot.com"
ENV MODEL_FILE_PATH_1="gs://${GCS_BUCKET_NAME}/Crop/Crop_predict.h5"
ENV MODEL_FILE_PATH_2="gs://${GCS_BUCKET_NAME}/Fertilizer/Fert_predict.h5"
ENV MODEL_FILE_PATH_3="gs://${GCS_BUCKET_NAME}/Paddy/Paddy_predict.h5"
ENV MODEL_FILE_PATH_4="gs://${GCS_BUCKET_NAME}/Cotton/modelcotton1_saved.h5"
ENV MODEL_FILE_PATH_5="gs://${GCS_BUCKET_NAME}/Soil_Prediction/model_saved.h5"

# Expose the port
EXPOSE 8080

# Set the command to run the application
CMD uvicorn main:app --host=0.0.0.0 --port=8080
