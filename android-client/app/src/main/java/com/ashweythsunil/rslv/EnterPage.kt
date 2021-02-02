package com.ashweythsunil.rslv

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.View

class EnterPage : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_enter_page)
    }

    fun switchScn(view: View) {
        val intent = Intent(applicationContext, MainNav::class.java)
        startActivity(intent)
    }
}
