package com.example.smartblinds.ui.notifications;

import androidx.annotation.NonNull;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.example.smartblinds.ConnectionClass;

import org.jetbrains.annotations.NotNull;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class NotificationsViewModel extends ViewModel {

    private final MutableLiveData<String> mText;
    ConnectionClass connectionClass;
    Connection con;

    private static int[] pvalue = new int[2];

    public NotificationsViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Recommended settings for your blinds and window");
        pvalue = this.ConnectToGet();
    }

    public LiveData<String> getText() {
        return mText;
    }

    public void InferenceRequest() {
        // creating a client
        OkHttpClient okHttpClient = new OkHttpClient();

        // building a request
        Request request = new Request.Builder().url("http://192.168.56.1:5000/ai").build();

        // making call asynchronously
        okHttpClient.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(@NonNull Call call, @NonNull IOException e) {

            }

            @Override
            // called if we get a
            // response from the server
            public void onResponse(
                    @NotNull Call call,
                    @NotNull Response response)
                   {}
        });
    }

    public int[] ConnectToGet() {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "select pvalue from preferences where ptype = \"rec_blind_pos\" or ptype = \"rec_window_pos\" order by id";
                PreparedStatement stmt = con.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();
                StringBuilder bStr = new StringBuilder();
                StringBuilder bStr2 = new StringBuilder();
                rs.next();
                bStr.append(rs.getString("pvalue"));
                rs.next();
                bStr2.append(rs.getString("pvalue"));

                pvalue[0] = Integer.valueOf(bStr.toString());
                pvalue[1] = Integer.valueOf(bStr2.toString());
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
        return pvalue;
    }

    public void ConnectToSet(int val[]) {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "update preferences set pvalue = " + val[0] + " where ptype = \"blind_pos\"";
                String query2 = "update preferences set pvalue = " + val[1] + " where ptype = \"window_pos\"";
                String query3 = "update preferences set pvalue = 0 where ptype = \"blind_mode\"";
                Statement stmt = con.createStatement();
                stmt.executeUpdate(query);
                stmt.executeUpdate(query2);
                stmt.executeUpdate(query3);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
    }
}