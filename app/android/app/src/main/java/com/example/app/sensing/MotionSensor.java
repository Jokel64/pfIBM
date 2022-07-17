package com.example.app.sensing;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.hardware.TriggerEvent;
import android.hardware.TriggerEventListener;
import android.os.Build;

import androidx.annotation.RequiresApi;

public class MotionSensor {

    private SensorManager sensorManager;
    private Sensor sensor;
    private TriggerEventListener triggerEvent;

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN_MR2)
    public MotionSensor(SensorManager manager){
        sensorManager = manager;
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_SIGNIFICANT_MOTION);

        triggerEvent = new TriggerEventListener() {
            @Override
            public void onTrigger(TriggerEvent event) {
                System.out.println(event.values);
            }
        };

        sensorManager.requestTriggerSensor(triggerEvent, sensor);
    }
}
