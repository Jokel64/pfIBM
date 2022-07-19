package com.example.app.sensing;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.hardware.TriggerEvent;
import android.hardware.TriggerEventListener;
import android.os.Build;

import androidx.annotation.RequiresApi;

import com.example.app.RoomState;

public class MotionSensor implements SensorEventListener {

    private SensorManager sensorManager;
    private Sensor sensor;
    private TriggerEventListener triggerEvent;

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN_MR2)
    public MotionSensor(SensorManager manager){
        sensorManager = manager;
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
        sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_FASTEST);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        System.out.println("Person is moving");
        RoomState.soll_lightnig=1000;
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}
