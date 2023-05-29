import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface MyApiService {
    @POST("/signup")
    suspend fun signUp(@Body request: SignUpRequest): Response<Void>

    @POST("/signin")
    suspend fun signIn(@Body request: SignInRequest): Response<SignInResponse>

    @GET("/user")
    suspend fun getUser(): Response<UserData>

    @POST("/weather-forecast")
    suspend fun getWeatherForecast(@Body request: WeatherForecastRequest): Response<WeatherForecast>
}