package com.example.sangjin.keyboard;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = (TextView) findViewById(R.id.textview);
        textView.setText("x , y coordinates");
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int)event.getX();
        int y = (int)event.getY();

        String strX = String.valueOf(x);
        String strY = String.valueOf(y);

        TextView textView = (TextView) findViewById(R.id.textview);
        textView.setText(strX + " , " + strY);
        return false;
    }


}

