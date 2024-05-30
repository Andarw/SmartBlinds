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

public class DashboardViewModel2 extends ViewModel {

    private final MutableLiveData<String> mText;
    ConnectionClass connectionClass;
    Connection con;
    String res, str;
    private static int[] pvalue = new int[2];

    public DashboardViewModel2() {
        mText = new MutableLiveData<>();
        mText.setValue("Select the position of\n your blinds and window.");
        pvalue = this.ConnectToGet();
    }

    public LiveData<String> getText() {

//        mText.setValue(res);
        return mText;
    }

    public int[] ConnectToGet() {
        connectionClass = new ConnectionClass();
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        executorService.execute(() -> {
            try {
                con = connectionClass.CONN();
                String query = "select pvalue from preferences where ptype = \"blind_pos\" or ptype = \"window_pos\" order by id";
                PreparedStatement stmt = con.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();
                StringBuilder bStr = new StringBuilder();
                StringBuilder bStr2 = new StringBuilder();
                rs.next();
                bStr.append(rs.getString("pvalue"));
                rs.next();
                bStr2.append(rs.getString("pvalue"));
//                while(rs.next()) {
//                    bStr.append(rs.getString("pvalue"));
//                }
                pvalue[0] = Integer.valueOf(bStr.toString());
                pvalue[1] = Integer.valueOf(bStr2.toString());
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