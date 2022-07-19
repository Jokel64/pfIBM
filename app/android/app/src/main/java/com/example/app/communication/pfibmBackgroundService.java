package com.example.app.communication;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import com.example.app.R;
import com.example.app.RoomState;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class pfibmBackgroundService extends Service {
    private static final int MAX_UDP_DATAGRAM_LEN = 1500;
    Thread UDPBroadcastThread;
    Intent callingIntent;
    boolean shouldStop = false;
    Socket socket;

    /* access modifiers changed from: package-private */
    public void startListenForUDPCommunication() {
        Thread thread = new Thread(new Runnable() {
            public void run() {
                try {
                    pfibmBackgroundService.this.socket = new Socket("192.168.2.96", 5005);
                    BufferedReader in = new BufferedReader(new InputStreamReader(pfibmBackgroundService.this.socket.getInputStream()));
                    while (!pfibmBackgroundService.this.shouldStop) {
                        String instr = in.readLine();
                        if (instr.contains("ACTION:")) {
                            pfibmBackgroundService.this.sendActionPushMessage("Action Required", instr);
                        }
                        if (instr.contains(NotificationCompat.CATEGORY_STATUS)) {
                            String[] a = instr.split(";");
                            RoomState.ist_lightnig = Double.parseDouble(a[0]);
                            RoomState.ist_temperature = Double.parseDouble(a[1]);
                        }
                    }
                } catch (Exception e) {
                    Log.i("UDP", "no longer listening for UDP broadcasts cause of error " + e.getMessage());
                }
            }
        });
        this.UDPBroadcastThread = thread;
        thread.start();
    }

    public void sendMessage(final String message) {
        new Thread(new Runnable() {
            public void run() {
                try {
                    DataOutputStream dataOutputStream = new DataOutputStream(pfibmBackgroundService.this.socket.getOutputStream());
                    dataOutputStream.writeUTF(message);
                    dataOutputStream.flush();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.i("UDP", "on start command");
        createNotificationChannel();
        this.callingIntent = intent;
        startListenForUDPCommunication();
        sendData();
        return START_STICKY;
    }

    public void onDestroy() {
        super.onDestroy();
        this.shouldStop = true;
        try {
            this.socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public IBinder onBind(Intent intent) {
        Log.i("UDP", "on bind command");
        return null;
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel("pfibm_msg_1", "pfIBM Action Messages", 4);
            channel.setDescription("These Messages are instuctions for you to do something");
            ((NotificationManager) getSystemService(NotificationManager.class)).createNotificationChannel(channel);
        }
    }

    private void sendData() {
        new Thread(new Runnable() {
            public void run() {
                while (!pfibmBackgroundService.this.shouldStop) {
                    pfibmBackgroundService.this.sendMessage(RoomState.soll_lightnig + ";" + RoomState.soll_temperature + ";"+ RoomState.energy_score + "\n");
                    try {
                        Thread.sleep(1000);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    /* access modifiers changed from: private */
    public void sendActionPushMessage(String actionName, String actionDescription) {
        NotificationManagerCompat.from(this).notify(0, new NotificationCompat.Builder((Context) this, "pfibm_msg_1").setSmallIcon((int) R.mipmap.ic_launcher).setContentTitle(actionName).setContentText(actionDescription).setAutoCancel(true).build());
    }
}