package com.example.app.communication;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Looper;
import android.util.Log;

import androidx.annotation.Nullable;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.MulticastSocket;

public class MulticastReceiverService extends Service {

    MulticastSocket socket;
    boolean shouldStop = false;

    Intent callingIntent;

    private void listenAndWaitForCommunication() throws IOException {
        byte[] recvBuf = new byte[15000];

        socket = new MulticastSocket(5005);
        InetAddress group = InetAddress.getByName("224.0.0.0");
        socket.joinGroup(group);

        while (!shouldStop){
            DatagramPacket packet = new DatagramPacket(recvBuf, recvBuf.length);
            socket.receive(packet);
            String received = new String(packet.getData(),0,packet.getLength());
            Log.i("UDP", "Received UDP Brodcast:"+ received);
        }

        socket.leaveGroup(group);
        socket.close();
    }

    Thread UDPBroadcastThread;

    void startListenForUDPBroadcast() {
        UDPBroadcastThread = new Thread(new Runnable() {
            public void run() {
                try {
                    listenAndWaitForCommunication();
                    //if (!shouldListenForUDPBroadcast) throw new ThreadDeath();
                } catch (Exception e) {
                    Log.i("UDP", "no longer listening for UDP broadcasts cause of error " + e.getMessage());
                }
            }
        });
        UDPBroadcastThread.start();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.i("UDP", "on start command");
        callingIntent = intent;
        startListenForUDPBroadcast();
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        shouldStop = true;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        Log.i("UDP", "on bind command");
        return null;
    }
}
