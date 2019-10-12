package com.example.carlicense;


import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.SurfaceTexture;
import android.os.Message;
import android.widget.Toast;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;

class ServerTools {
    private String server_ip;

    ServerTools(String server_ip) {
        this.server_ip = server_ip;
    }

    String doPost(String username, String password, String Url) throws UnsupportedEncodingException {
        String response = "";
        String parameters = URLEncoder.encode("username", "UTF-8")
                + "=" + URLEncoder.encode(username, "UTF-8");
        parameters += "&" + URLEncoder.encode("password", "UTF-8") + "="
                + URLEncoder.encode(password, "UTF-8");
        try {
            URL url = new URL(server_ip + Url);//url前面要带http://之类
            //获取连接
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            //使用POST方法访问网络
            connection.setRequestMethod("POST");
            //超时时间为10秒
            connection.setConnectTimeout(10000);
            connection.setDoOutput(true);
            OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
            out.write(parameters);
            out.flush();
            out.close();
//            System.out.println("damn it!***************"+parameters);
            InputStream inputStream = connection.getInputStream();
            byte[] data = StreamTool.read(inputStream);
            response = new String(data, "utf-8");

        } catch (Exception e) {
            e.printStackTrace();
        }
        return response;
    }

    //get请求
    String doGet(String Url) throws UnsupportedEncodingException {
        String response = "";
        try {
            URL url = new URL(server_ip + Url);//url前面要带http://之类
            //获取连接
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            //使用GET方法访问网络
            connection.setRequestMethod("GET");
            //超时时间为10秒
            connection.setConnectTimeout(10000);
            InputStream inputStream = connection.getInputStream();
            byte[] data = StreamTool.read(inputStream);
            response = new String(data, "utf-8");

        } catch (Exception e) {
            e.printStackTrace();
        }
        return response;
    }

}
