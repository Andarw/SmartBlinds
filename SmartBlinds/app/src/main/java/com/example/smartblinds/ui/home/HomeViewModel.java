package com.example.smartblinds.ui.home;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.example.smartblinds.ConnectionClass;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HomeViewModel extends ViewModel {
    ConnectionClass connectionClass;
    Connection con;

    private static float[] pvalue = new float[3];

    private final MutableLiveData<String> mTextt;
    private final MutableLiveData<String> mTexth;
    private final MutableLiveData<String> mTextl;

    private final MutableLiveData<String> mText4;

    public HomeViewModel() {
        mTextt = new MutableLiveData<>();
        mTexth = new MutableLiveData<>();
        mTextl = new MutableLiveData<>();
        mText4 = new MutableLiveData<>();
        mTextt.setValue("Temperature");
        mTexth.setValue("Humidity");
        mTextl.setValue("Light intensity");
        mText4.setValue("Sensor data for the last hour");
        pvalue = this.ConnectToGet();
    }

    public LiveData<String> getTextTemp() {
        return mTextt;
    }
    public LiveData<String> getTextHum() {
        return mTexth;
    }
    public LiveData<String> getTextLight() {
        return mTextl;
    }
    public LiveData<String> getText4() {
        return mText4;
    }

    public float[] ConnectToGet() {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "select temperature, humidity, light_intensity from sensor_data order by rdate desc limit 1";
                PreparedStatement stmt = con.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();
                StringBuilder bStr = new StringBuilder();
                StringBuilder bStr2 = new StringBuilder();
                StringBuilder bStr3 = new StringBuilder();
                rs.next();
                bStr.append(rs.getString("temperature"));
                bStr2.append(rs.getString("humidity"));
                bStr3.append(rs.getString("light_intensity"));
                pvalue[0] = Float.valueOf(bStr.toString());
                pvalue[1] = Float.valueOf(bStr2.toString());
                pvalue[2] = Float.valueOf(bStr3.toString());
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
        return pvalue;
    }
}