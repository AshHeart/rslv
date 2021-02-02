package com.ashweythsunil.rslv

import android.Manifest
import android.app.ProgressDialog
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.AsyncTask
import android.support.v4.app.ActivityCompat
import android.support.v4.content.ContextCompat
import android.system.Os.read
import android.system.Os.write

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment

import android.util.Log
import android.widget.TextView
import android.widget.Toast
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.FuelManager
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import com.google.android.gms.location.*
import com.google.android.gms.maps.model.*
import com.google.android.gms.maps.model.MapStyleOptions
import es.dmoral.toasty.Toasty
import java.io.*
import java.net.ContentHandler
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import kotlin.coroutines.experimental.coroutineContext


class MainNav : AppCompatActivity(), OnMapReadyCallback {


    private lateinit var locationCallback: LocationCallback //livelocation vars
    private lateinit var locationRequest: LocationRequest //livelocation vars
    private lateinit var fusedLocationClient: FusedLocationProviderClient//live location vars
    //livelocation code from https://developer.android.com/training/location/receive-location-updates.html


    private lateinit var mMap: GoogleMap

    private var locationManager: LocationManager? = null


    private var currentPositionMarker: Marker? = null

    //TODO("Subject to change") To be refactored in production
    private var myLongitude: Double? = null
    private var myLatitude: Double? = null

    //TODO("Subject to change") To be refactored in production
    //Define a Location Listener
    private val locationListener: LocationListener = object : LocationListener {
        override fun onLocationChanged(location: Location) {


            //remove old marker
            var m1 = currentPositionMarker
            if (currentPositionMarker != null) {
                m1?.remove()

            }

            var latLng = LatLng(location.latitude, location.longitude)
            var cameraPosition = CameraPosition.Builder()
                    .target(latLng).zoom(16.0f).build()
            //marker
            currentPositionMarker = mMap.addMarker(MarkerOptions()
                    .position(latLng).title("You're here"))
            mMap.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
            myLongitude = location.longitude
            myLatitude = location.latitude

        }

        override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}

        override fun onProviderEnabled(provider: String?) {}

        override fun onProviderDisabled(p0: String?) {}
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_nav)


        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
                .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)


        //live location code below
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)

        locationRequest = LocationRequest.create()


        locationRequest.interval = 0
        locationRequest.fastestInterval = 0
        locationRequest.priority = LocationRequest.PRIORITY_HIGH_ACCURACY



        locationCallback = object : LocationCallback() {
            override fun onLocationResult(locationResult: LocationResult?) {
                locationResult ?: return
                for (location in locationResult.locations) {
                    var data = 0.4
                    // Update UI with location data
                    // ...

                    /**
                    For each of the confidence values, return the appropriate toast messages,
                    so that th user can use adjust the speed of the car according to the toast displayed
                     **/

// ...
                    //var confidence= null
//                    var data=" "
//
//                    Fuel.get("http://rslv.xyz/predict/friction").response { request, response, result ->
//                        val bytes = result
//                        if (bytes != null) {
//                            data = result
//                        }
//
//                    }

                    /**
                     * Data Fetch from the server with url http://rslv.xyz/predict/friction
                     * we use http method
                     * take the result fragment from the response string in the http string
                     * in a condition loop result
                     **/
//                    var url = "http://rslv.xyz/predict/friction"
//                    url.httpGet().responseString { request, response, result ->
//                        when(result){
//                            is Result.Success ->
//                            {   Log.d("res",result.get())
//                                data=result.value.toDouble()
//                            }
//                        }
//                    }

                    val confidence= data
                    //  Log.d("abc",data.toString())
                    when (confidence) {
                        0.0 -> Toasty.success(applicationContext, "Safe Roads Ahead", Toast.LENGTH_LONG, true).show()
                        0.2 -> Toasty.normal(applicationContext, "Keep Going", Toast.LENGTH_LONG).show()
                        0.4 -> Toasty.normal(applicationContext, "Keep Going", Toast.LENGTH_LONG).show()
                        0.6 -> Toasty.info(applicationContext, "Mind your speed", Toast.LENGTH_LONG, true).show()
                        0.8 -> Toasty.warning(applicationContext, "Slippery Roads Ahead, Slow Down", Toast.LENGTH_LONG, true).show()
                        1.0 -> Toasty.error(applicationContext, "Danger Ahead, High slip detected", Toast.LENGTH_LONG, true).show()
                    }
                }
            }
        }
        //live location block ends
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        /**
         * styling.....!
         * Two different themes are there, retro and night, retro will be alive till sunsets and later on the night mode gets on automatically
         * */
//        val success = googleMap.setMapStyle(MapStyleOptions(resources
//                .getString(R.string.day_json)))
//
//        if (!success) {
//            Log.d("Style parsing failed.", "Day style error")
//        }
        val success1 = googleMap.setMapStyle(MapStyleOptions(resources
                .getString(R.string.night_json)))

        if (!success1) {
            Log.d("Style parsing failed.","Day style error")
        }
        mMap = googleMap
        //permission request
        ActivityCompat.requestPermissions(this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                100)
        //requesting permission allow/deny
        val permission = ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
        if (permission == PackageManager.PERMISSION_GRANTED) {
            //TODO("Subject to change") To be refactored in production
            //Get a reference to the system Location Manager
            locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager?

            //TODO("Subject to change") To be refactored in production
            try {
                //Register the Location Listener with the Location Manager to receive location updates
                locationManager?.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0L, 0f, locationListener)
            } catch (e: SecurityException) {
                Log.d("LocationTag", "No Location Available")
            }
        }
        //if permission denied
        if (permission != PackageManager.PERMISSION_GRANTED) {
            finish()
        }

    }

    override fun onResume() {
        super.onResume()
        startLocationUpdates()
    }

    //location update function
    private fun startLocationUpdates() {

        val permission = ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
        //if permission denied
        if (permission != PackageManager.PERMISSION_GRANTED) {
            finish()
        } else {
            fusedLocationClient.requestLocationUpdates(locationRequest,
                    locationCallback,
                    null /* Looper */)
        }
    }

}


