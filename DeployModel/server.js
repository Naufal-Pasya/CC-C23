const express = require("express");
const tf = require("@tensorflow/tfjs");
const cors = require("cors"); // Ditambahkan untuk mengatasi masalah kebijakan CORS
const app = express();

// Muat model TensorFlow.js
const modelPath = "https://storage.cloud.google.com/capstone-project-c23.appspot.com/Soil_Prediction/model_saved.h5";
const weightPath = "https://storage.cloud.google.com/capstone-project-c23.appspot.com/Soil_Prediction/model_weights.h5";

async function loadModel() {
  const model = await tf.loadLayersModel(tf.io.fileSystem(modelPath));
  await model.loadWeights(tf.io.fileSystem(weightPath));
  return model;
}

let loadedModel;

// Middleware untuk mengizinkan permintaan dari sumber yang berbeda (CORS)
app.use(cors());

// Endpoint untuk memuat model sebelum server siap menerima prediksi
app.use(async (req, res, next) => {
  if (!loadedModel) {
    loadedModel = await loadModel();
  }
  next();
});

// Endpoint untuk menerima input dan menghasilkan prediksi
app.post("/predict", express.json(), async (req, res) => {
  const inputData = req.body; // Input dari klien
  const prediction = await loadedModel.predict(tf.tensor(inputData));
  const predictionData = await prediction.data();
  res.send(predictionData); // Mengirimkan prediksi sebagai respons
});

// Jalankan server pada port 8080
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`API berjalan pada port ${PORT}`);
});
