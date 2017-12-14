package com.example.sangjin.keyboard;

import android.content.Context;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private TcpClient mTcpClient;

    ArrayList<String> linesToType = new ArrayList<String>();
    ArrayList<String> touchedPoints = new ArrayList<String>();

    static int screenWidth = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Button connectButton = (Button) findViewById(R.id.connectButton);
        connectButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                final EditText ip = (EditText) findViewById(R.id.ip);
                String serverIp = ip.getText().toString();
                TcpClient.serverIp = serverIp;
                new ConnectTask().execute("");
            }
        });

        final Button nextTextButton = (Button) findViewById(R.id.nextTextButton);
        nextTextButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                TextView textView = (TextView) findViewById(R.id.editText2);

                if(linesToType.size() > 0 && touchedPoints.size() > 0) {
                    final String toSend = createStringToSend(linesToType.remove(0), touchedPoints);
                    touchedPoints.clear();
                    if (mTcpClient != null) {
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                mTcpClient.sendMessage(toSend);
                            }
                        }).start();
                    }
                    if (linesToType.size() == 0) {
                        textView.setText("");
                    } else {
                        textView.setText(linesToType.get(0));
                    }
                }
                else if(linesToType.size() > 0 && textView.getText().toString().equals("")) {
                    textView.setText(linesToType.get(0));
                }
            }
        });

        DisplayMetrics displayMetrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        screenWidth = displayMetrics.widthPixels;

        TextView textView = (TextView) findViewById(R.id.textview);
        textView.setText("x , y coordinates");

        new ConnectTask().execute("");
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if(event.getAction() == MotionEvent.ACTION_UP) {
            final int x = (int)event.getX();
            final int y = (int)event.getY();

            String strX = String.valueOf(x);
            String strY = String.valueOf(y);

            TextView textView = (TextView) findViewById(R.id.textview);
            textView.setText(strX + " , " + strY);

            double xDim = x / ((double) screenWidth);

            touchedPoints.add(String.format ("%.6f", xDim));
        }
        return false;
    }

    private String createStringToSend(String text, ArrayList<String> touchedPoints) {
        String toSend = "Message," + text + "_";
        int longestArrayList = text.length() > touchedPoints.size() ? text.length() : touchedPoints.size();

        for(int i = 0; i < longestArrayList; i++) {
            if(i < text.length() && i < touchedPoints.size()) {
                toSend = toSend + text.charAt(i) + "," + touchedPoints.get(i) + "_";
            }
            else if(i < text.length()) {
                toSend = toSend + text.charAt(i) + "," + "?_";
            }
            else {
                toSend = toSend + "?," + touchedPoints.get(i) + "_";
            }
        }

        return toSend;
    }

    public class ConnectTask extends AsyncTask<String, String, TcpClient> {

        @Override
        protected TcpClient doInBackground(String... message) {

            //we create a TCPClient object and
            mTcpClient = new TcpClient(new TcpClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                    linesToType.add(message);
                }
            });
            mTcpClient.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
        }
    }


}

