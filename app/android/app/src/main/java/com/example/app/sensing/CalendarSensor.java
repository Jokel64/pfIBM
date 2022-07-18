package com.example.app.sensing;

import android.content.ContentResolver;
import android.database.Cursor;
import android.provider.CalendarContract;
import java.util.Calendar;

public class CalendarSensor {
    public static final String[] EVENT_PROJECTION = {"calendar_id", "organizer", "title", "eventLocation"};

    public void getEvents(ContentResolver contentResolver) {
        Calendar beginTime = Calendar.getInstance();
        beginTime.set(2022, 7, 1, 8, 0);
        long timeInMillis = beginTime.getTimeInMillis();
        Calendar endTime = Calendar.getInstance();
        endTime.set(2022, 8, 1, 8, 0);
        long timeInMillis2 = endTime.getTimeInMillis();
        Cursor cur = contentResolver.query(CalendarContract.Events.CONTENT_URI.buildUpon().build(), EVENT_PROJECTION, (String) null, (String[]) null, (String) null);
        while (cur.moveToNext()) {
            int id = cur.getInt(0);
            String Organizer = cur.getString(1);
            String Title = cur.getString(2);
            String EventLocation = cur.getString(3);
        }
    }
}