package com.example.carlicense;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {
    public String server_ip = "http://10.230.134.201:8000";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        //隐藏title bar.
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
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
        String pasword = login_password.getText().toString();
        if (checkUser(username, pasword)) {
            //启动MainActivity
            //https://stackoverflow.com/questions/4186021/how-to-start-new-activity-on-button-click
            Intent myIntent = new Intent(this, MainActivity.class);
            myIntent.putExtra("username", username); //Optional parameters
            startActivity(myIntent);
        } else {
            Dialog myDialog = new Dialog(this);
            myDialog.setContentView(R.layout.popup_hint);
            TextView hint = myDialog.findViewById(R.id.hint_text);
            hint.setText("登录失败！用户名或密码错误");
            myDialog.show();
        }

    }

    //点击注册按钮
    public void clickRegister(View view) {

    }

    //验证用户
    @SuppressLint("SetTextI18n")
    public Boolean checkUser(String username, String password) {
        if (username.isEmpty() || password.isEmpty()) return false;
        ServerTools serverTools = new ServerTools(server_ip);
        String json = "";
        try {
            json = serverTools.doPost(username, password);
        } catch (Exception ignored) {

        }
        if (json.isEmpty()) {
            return false;
        } else {
            try {
                //处理json数据
                JSONObject jsonObject = new JSONObject(json);
                String status = jsonObject.optString("status");
                System.out.println(status+" ******DDDDDDDDDDDDDDDDDDDDD");
                return status.equals("True");
            } catch (Exception e) {
                e.printStackTrace();
                return false;
            }
        }
    }
}
