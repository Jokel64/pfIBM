package com.example.app;

import android.content.Intent;
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
                                    result.success(RoomState.ist_temperature);
                                    break;
                                case "light":
                                    RoomState.soll_lightnig = call.argument("l");
                                    result.success(RoomState.ist_lightnig);
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

    @Override
    public void onStart() {
        super.onStart();
        this.c_sensor.getEvents(getContentResolver());
        System.out.println("Hello World");
        startService(new Intent(this, pfibmBackgroundService.class));
    }

    public MainActivity(){

    }

}
