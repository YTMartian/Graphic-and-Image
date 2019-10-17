package com.example.carlicense;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.VideoView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {
    public String server_ip = "http://10.230.134.201:8000";
    private Dialog myDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        //隐藏title bar.
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        myDialog = new Dialog(this);
        /**
         * 网络连接问题
         https://stackoverflow.com/questions/43486939/no-network-security-config-specified-using-platform-default?rq=1
         */
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
    }

    //点击登录按钮
    public void clickLogin(View view) {
        TextView login_username = findViewById(R.id.login_username);
        TextView login_password = findViewById(R.id.login_password);
        String username = login_username.getText().toString();
        String password = login_password.getText().toString();
        int flag = checkUser(username, password);
        if (flag == 1) {
            //启动MainActivity
            //https://stackoverflow.com/questions/4186021/how-to-start-new-activity-on-button-click
            Intent myIntent = new Intent(this, MainActivity.class);
            myIntent.putExtra("username", username); //Optional parameters
            startActivity(myIntent);
        } else if (flag == 0) {
            showHint("登录失败！用户名或密码错误");
        } else if (flag == -1) {
            showHint("服务器连接失败！");
        }

    }

    //点击注册按钮
    public void clickRegister(View view) {
        TextView login_username = findViewById(R.id.login_username);
        TextView login_password = findViewById(R.id.login_password);
        String username = login_username.getText().toString();
        String password = login_password.getText().toString();
        if (username.isEmpty() || password.isEmpty()) {
            showHint("注册失败！用户名或密码为空");
        } else {
            ServerTools serverTools = new ServerTools(server_ip);
            String json = "";
            try {
                json = serverTools.doPost(username, password, "/system/register_user/");
            } catch (Exception e) {
                e.printStackTrace();
            }
            if (json.isEmpty()) {
                showHint("注册失败！服务器连接失败！");
            } else {
                try {
                    //处理json数据
                    JSONObject jsonObject = new JSONObject(json);
                    String status = jsonObject.optString("status");
                    if (status.equals("False")) {
                        showHint("注册失败！用户名已存在");
                    } else if (status.equals("True")) {
                        showHint("注册成功！");
                    } else {
                        showHint("未知返回参数！");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    //验证用户
    @SuppressLint("SetTextI18n")
    public int checkUser(String username, String password) {
        //1表示成功 0表示验证失败，-1表示网络连接失败
        if (username.isEmpty() || password.isEmpty()) return 0;
        ServerTools serverTools = new ServerTools(server_ip);
        String json = "";
        try {
            json = serverTools.doPost(username, password, "/system/check_user/");
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (json.isEmpty()) {
            return -1;
        } else {
            try {
                //处理json数据
                JSONObject jsonObject = new JSONObject(json);
                String status = jsonObject.optString("status");
//                System.out.println(status+" ******DDDDDDDDDDDDDDDDDDDDD");
                if (status.equals("True")) {
                    return 1;
                } else {
                    return 0;
                }
            } catch (Exception e) {
                e.printStackTrace();
                return -1;
            }
        }
    }

    //弹窗信息显示
    public void showHint(String s) {
        myDialog.setContentView(R.layout.popup_hint);
        VideoView videoView = myDialog.findViewById(R.id.railing_video);
        videoView.setVisibility(View.GONE);
        TextView hint = myDialog.findViewById(R.id.hint_text);
        hint.setText(s);
        myDialog.show();
    }
}
