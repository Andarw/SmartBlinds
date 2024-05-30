package com.example.smartblinds.ui.dashboard;

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

public class DashboardViewModel extends ViewModel {

    private final MutableLiveData<String> mText;
    ConnectionClass connectionClass;
    Connection con;
    String str;
    private static int pvalue;

    public DashboardViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Select your preferred sensibility\n for your blinds.");
        pvalue = this.ConnectToGet();
    }

    public LiveData<String> getText() {

        return mText;
    }

    public int ConnectToGet() {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "select pvalue from preferences where ptype = \"sensitivity\"";
                PreparedStatement stmt = con.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();
                StringBuilder bStr = new StringBuilder();
                while(rs.next()) {
                    bStr.append(rs.getString("pvalue"));
                }
                pvalue = Integer.valueOf(bStr.toString());
                if(con == null)
                    str = "Error";
                else
                    str = "Successful";
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
        return pvalue;
    }

    public void ConnectToSet(int val) {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "update preferences set pvalue = " + val + " where ptype = \"sensitivity\"";
                String query2 = "update preferences set pvalue = 1 where ptype = \"blind_mode\"";
                Statement stmt = con.createStatement();
                stmt.executeUpdate(query);
                stmt.executeUpdate(query2);
                if(con == null)
                    str = "Error";
                else
                    str = "Successful";
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
    }
}