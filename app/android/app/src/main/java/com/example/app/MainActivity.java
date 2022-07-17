package com.example.app;

import android.content.Context;
import android.content.Intent;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.os.PersistableBundle;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;

import com.example.app.communication.MulticastReceiverService;
import com.example.app.sensing.MotionSensor;

import io.flutter.embedding.android.FlutterActivity;

public class MainActivity extends FlutterActivity {

    private MotionSensor motionSensor;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState, @Nullable PersistableBundle persistentState) {
        super.onCreate(savedInstanceState, persistentState);
    }

    @Override
    protected void onStart() {
        super.onStart();

        System.out.println("Hello World");

        startService(new Intent(this, MulticastReceiverService.class));
    }

    public MainActivity(){

    }

}
