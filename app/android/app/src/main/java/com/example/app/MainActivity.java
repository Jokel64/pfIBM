package com.example.app;

import android.content.Context;
import android.content.Intent;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.os.PersistableBundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;

import com.example.app.communication.pfibmBackgroundService;
import com.example.app.sensing.CalendarSensor;
import com.example.app.sensing.MotionSensor;

import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodChannel;

public class MainActivity extends FlutterActivity {

    private static final String CHANNEL = "samples.flutter.dev/pfibm";
    private CalendarSensor c_sensor = new CalendarSensor();
    private MotionSensor motionSensor;

    @Override
    public void configureFlutterEngine(@NonNull FlutterEngine flutterEngine) {
        super.configureFlutterEngine(flutterEngine);
        new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
                .setMethodCallHandler(
                        (call, result) -> {
                            String method_name = call.method;
                            switch (method_name){
                                case "temp":
                                    RoomState.soll_temperature = call.argument("t");
                                    result.success(RoomState.getIstTemp());
                                    break;
                                case "light":
                                    RoomState.soll_lightnig = call.argument("l");
                                    result.success(RoomState.getIstLight());
                                    break;
                                case "temp_soll":
                                    result.success(RoomState.soll_temperature);
                                    break;
                                case "temp_ist":
                                    result.success(RoomState.getIstTemp());
                                    break;
                                case "light_soll":
                                    result.success(RoomState.soll_lightnig / 10);
                                    break;
                                case "light_ist":
                                    result.success(RoomState.getIstLight());
                                    break;
                                case "energy":
                                    RoomState.energy_score = call.argument("e");
                                    result.success(0);
                                    break;
                                case "energy_get":
                                    result.success(RoomState.energy_score);
                                    break;

                                default:
                                    break;
                            }
                        }
                );
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState, @Nullable PersistableBundle persistentState) {
        super.onCreate(savedInstanceState, persistentState);
    }

    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN_MR2)
    @Override
    public void onStart() {
        super.onStart();
        motionSensor = new MotionSensor((SensorManager) getSystemService(Context.SENSOR_SERVICE));
        this.c_sensor.getEvents(getContentResolver());
        System.out.println("Hello World");
        startService(new Intent(this, pfibmBackgroundService.class));
    }

    public MainActivity(){

    }

}
