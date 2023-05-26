import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.MapView
import com.google.android.gms.maps.OnMapReadyCallback
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {
    private lateinit var mapView: MapView
    private lateinit var googleMap: GoogleMap

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        mapView = findViewById(R.id.mapView)
        mapView.onCreate(savedInstanceState)
        mapView.getMapAsync { map ->
            googleMap = map
            // Mengatur tampilan peta dan operasi lainnya di sini

            val apiService = ApiClient.apiService
            val location = "New York" // Ganti dengan lokasi yang diinginkan
            apiService.getMapData(location).enqueue(object : Callback<MapData> {
                override fun onResponse(call: Call<MapData>, response: Response<MapData>) {
                    if (response.isSuccessful) {
                        val mapData = response.body()
                        // Gunakan data peta yang diterima di sini
                        val latitude = mapData?.latitude
                        val longitude = mapData?.longitude
                        // Tampilkan lokasi pada peta
                    }
                }

                override fun onFailure(call: Call<MapData>, t: Throwable) {
                    // Tangani kesalahan jika permintaan gagal
                }
            })
        }
    }

    override fun onResume() {
        super.onResume()
        mapView.onResume()
    }

    override fun onPause() {
        super.onPause()
        mapView.onPause()
    }

    override fun onDestroy() {
        super.onDestroy()
        mapView.onDestroy()
    }

    override fun onLowMemory() {
        super.onLowMemory()
        mapView.onLowMemory()
    }
}
