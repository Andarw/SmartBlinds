package com.example.smartblinds;

import java.sql.Connection;
import java.sql.DriverManager;

public class ConnectionClass {

    private static final String url = "jdbc:mysql://window.cda6cmuk8kg0.eu-north-1.rds.amazonaws.com:3306/blind";
    private static final String user = "admin";
    private static final String pass = "bmwseria5";
    public Connection CONN() {
        Connection conn = null;
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            conn = DriverManager.getConnection(url, user, pass);
        } catch (Exception e) {
            System.out.println("Not connected");
        }
    return conn;
    }
}
