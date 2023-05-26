import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {
    @GET("/api/map/{location}")
    fun getMapData(@Path("location") location: String): Call<MapData>
}
