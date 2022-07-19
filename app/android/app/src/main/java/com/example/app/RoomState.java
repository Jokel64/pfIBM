package com.example.app;

public class RoomState {
    public static double soll_temperature = 20;
    public static double ist_temperature = 20;

    public static double soll_lightnig = 1800;
    public static double ist_lightnig = 1400;

    public static double getIstTemp(){
        return Math.round(ist_temperature );
    }

    public static double getIstLight(){
        return Math.round(ist_lightnig/10 );
    }

}
