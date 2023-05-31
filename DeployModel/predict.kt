import okhttp3.*
import org.json.JSONObject
import java.io.IOException

fun sendPredictionRequest(inputData: List<Float>) {
    val url = "http://<IP_SERVER>:8080/predict" // Ganti <IP_SERVER> dengan alamat IP server Anda
    
    // Buat objek JSON yang berisi input data
    val jsonInput = JSONObject()
    jsonInput.put("input", inputData)

    // Buat request body dengan tipe konten application/json
    val requestBody = RequestBody.create(MediaType.parse("application/json"), jsonInput.toString())

    // Buat permintaan POST ke endpoint /predict
    val request = Request.Builder()
        .url(url)
        .post(requestBody)
        .build()

    // Kirim permintaan ke server
    val client = OkHttpClient()
    client.newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            // Tangani jika permintaan gagal
            e.printStackTrace()
        }

        override fun onResponse(call: Call, response: Response) {
            val responseData = response.body()?.string()

            // Tangani respons dari server
            if (response.isSuccessful && responseData != null) {
                // Respons sukses, lakukan operasi dengan data respons
                val predictionData = parsePredictionData(responseData)
                processPredictionResult(predictionData)
            } else {
                // Tangani jika respons tidak berhasil
                println("Request failed")
            }
        }
    })
}

fun parsePredictionData(responseData: String): Float {
    // Parse data respons dari server
    val jsonObject = JSONObject(responseData)
    return jsonObject.getFloat("prediction")
}

fun processPredictionResult(prediction: Float) {
    // Lakukan operasi dengan hasil prediksi
    println("Hasil prediksi: $prediction")
}

fun main() {
    val inputData = listOf(0.1f, 0.2f, 0.3f) // Contoh input data

    sendPredictionRequest(inputData)
}
