package com.example.app;

import java.sql.Time;

public class RoomState {
    public static double soll_temperature = 20;
    public static double ist_temperature = 20;

    public static double soll_lightnig = 490;
    public static double ist_lightnig = 220;

    public static double energy_score = 0;

    public static Time

    public static double getIstTemp(){
        return Math.round(ist_temperature );
    }

    public static double getIstLight(){
        return Math.round(ist_lightnig/10 );
    }

}
