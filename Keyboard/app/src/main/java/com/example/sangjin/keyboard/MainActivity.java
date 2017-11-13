package com.example.sangjin.keyboard;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    private TcpClient mTcpClient;

    static Socket clientSocket;
    static PrintWriter outToServer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = (TextView) findViewById(R.id.textview);
        textView.setText("x , y coordinates");

        /*try {
            //InetAddress serverAddr = InetAddress.getByName("localhost");
            clientSocket = new Socket("demos.kaazing.com/echo", 1005);
            outToServer = new PrintWriter(new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream())), true);;
        } catch (IOException e) {
            e.printStackTrace();
        }*/

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

            //sends the message to the server
            if (mTcpClient != null) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String message = x + "," + y;
                        mTcpClient.sendMessage(message);
                    }
                }).start();
            }
            //outToServer.write(5);
        }
        return false;
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
                }
            });
            mTcpClient.run();

            return null;
        }



        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);

            //in the arrayList we add the messaged received from server
            //arrayList.add(values[0]);
            // notify the adapter that the data set has changed. This means that new message received
            // from server was added to the list
            //mAdapter.notifyDataSetChanged();
        }
    }


}

