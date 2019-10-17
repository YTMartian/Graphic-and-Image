package com.example.carlicense;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.VideoView;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import com.example.carlicense.ui.about.AboutFragment;
import com.example.carlicense.ui.home.HomeFragment;
import com.example.carlicense.ui.settings.SettingsFragment;
import com.github.clans.fab.FloatingActionMenu;
import com.github.clans.fab.FloatingActionButton;
import com.google.android.material.navigation.NavigationView;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {
    boolean is_get_in = false;
    Dialog myDialog;
    String server_ip;
    String username;

    private AppBarConfiguration mAppBarConfiguration;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //AndroidManifest.xml里MainActivity要设置android:theme="@style/AppTheme.NoActionBar"
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        mAppBarConfiguration = new AppBarConfiguration.Builder(
                R.id.nav_home,
                R.id.nav_settings,
                R.id.nav_about)
                .setDrawerLayout(drawer)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);
        //设置监听导航按钮的点击
        navigationView.setNavigationItemSelectedListener(this);

        myDialog = new Dialog(this);
        server_ip = "http://10.230.134.201:8000";
        username = "test";
        Intent intent = getIntent();
        username = intent.getStringExtra("username"); //从LoginActivity传来的参数
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }

    //点击不同导航按钮的事件
    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
        FloatingActionMenu menu = findViewById(R.id.menu);
        switch (menuItem.getItemId()) {
            case R.id.nav_home:
                menu.showMenu(true);
                getSupportActionBar().setTitle("主页");//设置导航栏的text
                //放入HomeFragment.
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new HomeFragment()).commit();
                break;
            case R.id.nav_settings:
                menu.hideMenu(true);
                getSupportActionBar().setTitle("设置");
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new SettingsFragment()).commit();
                break;
            case R.id.nav_about:
                menu.hideMenu(true);
                getSupportActionBar().setTitle("关于");
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new AboutFragment()).commit();
                break;
        }
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    //点击history按钮
    public void clickHistory(View view) {
        myDialog.setContentView(R.layout.popup_history_list);
        ListView history_list = myDialog.findViewById(R.id.history_list);
        //传入显示数据,MyAdapter构造函数的的五个参数
        ArrayList<String>[] s = new ArrayList[5];
        for (int i = 0; i < 5; i++) s[i] = new ArrayList<>();

        ServerTools serverTools = new ServerTools(server_ip);
        try {
            String jsons = serverTools.doPost(this.username, "", "/system/get_history/");
            StringBuilder sb = new StringBuilder(jsons);
            //不知道怎么把python server返回的json字符串转为java的json格式，所以直接正则匹配，对每一部分分别转json
            sb.deleteCharAt(0);
            sb.deleteCharAt(sb.length() - 1);//去掉收尾的大括号
            jsons = new String(sb);
            //正则匹配
            Pattern p = Pattern.compile("\\{([^}])*\\}");
            Matcher m = p.matcher(jsons);
            while (m.find()) {
                String json = m.group();
                JSONObject jsonObject = new JSONObject(json);
                s[0].add(jsonObject.optString("photograph"));
                s[1].add(jsonObject.optString("license_plate"));
                s[2].add(jsonObject.optString("type"));
                s[3].add(jsonObject.optString("time"));
                s[4].add(jsonObject.optString("price"));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        //反转ArrayList，将最新的记录显示在上边
        for(ArrayList<String>i:s)Collections.reverse(i);
        MyAdapter myAdapter = new MyAdapter(this, s[0], s[1], s[2], s[3], s[4]);
        history_list.setAdapter(myAdapter);
        myDialog.show();

    }

    //history列表显示类
    class MyAdapter extends ArrayAdapter<String> {
        Context context;
        ArrayList<String> history_license_plate_image;
        ArrayList<String> history_license_plate_text;
        ArrayList<String> history_car_type;
        ArrayList<String> history_time;
        ArrayList<String> history_pay_toll;

        MyAdapter(Context c, ArrayList<String> s1, ArrayList<String> s2, ArrayList<String> s3, ArrayList<String> s4, ArrayList<String> s5) {
            //父类构造函数这里，得加上第三和第四个参数，大概类似于标识符以示区分？
            super(c, R.layout.row, R.id.history_license_plate_text, s2);
            this.context = c;
            this.history_license_plate_image = s1;
            this.history_license_plate_text = s2;
            this.history_car_type = s3;
            this.history_time = s4;
            this.history_pay_toll = s5;
        }

        @SuppressLint("SetTextI18n")
        @NonNull
        @Override
        public View getView(int position, @NonNull View convertView, @NonNull ViewGroup parent) {
            LayoutInflater layoutInflater =
                    (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            View row = layoutInflater.inflate(R.layout.row, parent, false);
            MyImageView history_license_plate_image = row.findViewById(R.id.history_license_plate_image);
            TextView history_license_plate_text = row.findViewById(R.id.history_license_plate_text);
            TextView history_car_type = row.findViewById(R.id.history_car_type);
            TextView history_time = row.findViewById(R.id.history_time);
            TextView history_pay_toll = row.findViewById(R.id.history_pay_toll);

            history_license_plate_image.setImageURL(server_ip + "/static/images/" + this.history_license_plate_image.get(position));
            history_license_plate_text.setText(history_license_plate_text.getText() + this.history_license_plate_text.get(position));
            history_car_type.setText(history_car_type.getText() + this.history_car_type.get(position));
            history_time.setText(history_time.getText() + this.history_time.get(position));
            history_pay_toll.setText(history_pay_toll.getText() + this.history_pay_toll.get(position) + "元");
            return row;
        }
    }

    //点击get_in按钮
    @SuppressLint("SetTextI18n")
    public void clickGetIn(View view) {
        //弹出确认框
        myDialog.setContentView(R.layout.popup);
        //注意应在myDialog下find，否则就是空指针错误
        MyImageView license_plate_image = myDialog.findViewById(R.id.license_plate_image);
        TextView license_plate_text = myDialog.findViewById(R.id.license_plate_text);
        TextView car_type = myDialog.findViewById(R.id.car_type);
        TextView now_time = myDialog.findViewById(R.id.now_time);
        TextView pay_toll = myDialog.findViewById(R.id.pay_toll);
        //向服务器请求当前结果
        ServerTools serverTools = new ServerTools(server_ip);
        String json = "";
        try {
            if (is_get_in) {
                //这里其实应该写"True"，懒得改了。。。
                json = serverTools.doPost("False", "", "/system/get_current_result/");
            } else {
                json = serverTools.doPost("True", "", "/system/get_current_result/");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (!json.isEmpty()) {
            try {
                //处理json数据
                JSONObject jsonObject = new JSONObject(json);
                String color = jsonObject.optString("color");
                color = color.equals("黄") ? "大车" : color.equals("蓝") ? "小车" : "";
                String license_plate = jsonObject.optString("license_plate");
                String time = jsonObject.optString("time");
                String image = jsonObject.optString("image");
                String price = jsonObject.optString("price");
                /**
                 * 太坑了！！！一直app内不能联网，但avd是能的，每次重新run依然不能联网，需要
                 * 在avd内把app卸载了，再run app就能联网了，可能是部分文件没更新？
                 */
                license_plate_image.setImageURL(server_ip + "/static/images/" + image);
                license_plate_text.setText(license_plate_text.getText() + license_plate);
                car_type.setText(car_type.getText() + color);
                now_time.setText(now_time.getText() + time);
                pay_toll.setText(pay_toll.getText() + price + "元");
                if (is_get_in) {
                    pay_toll.setVisibility(View.VISIBLE);
                } else {
                    pay_toll.setVisibility(View.GONE);
                }
                myDialog.show();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }


    }

    //点击确定按钮
    public void clickEnsure(View view) {
        String state = "success";
        if (is_get_in) {
            //记录进入
            ServerTools serverTools = new ServerTools(server_ip);
            try {
                String json = serverTools.doPost("False", "", "/system/get_in_and_out/");
                JSONObject jsonObject = new JSONObject(json);
                state = jsonObject.optString("state");
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            //记录离开
            ServerTools serverTools = new ServerTools(server_ip);
            try {
                String json = serverTools.doPost("True", "", "/system/get_in_and_out/");
                JSONObject jsonObject = new JSONObject(json);
                state = jsonObject.optString("state");

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        myDialog.dismiss();
        if (state.equals("failed")) {
            showHint("保存失败！未检测到车牌", Boolean.FALSE);
        } else {
            FloatingActionButton button = findViewById(R.id.get_in);
            //更改按钮图标和文字
            if (is_get_in) {
                button.setImageResource(R.drawable.ic_get_in);
                button.setLabelText("进入");
            } else {
                button.setImageResource(R.drawable.ic_get_out);
                button.setLabelText("离开");
            }
            is_get_in = !is_get_in;
            showHint("", true);
        }
    }


    //弹窗信息显示
    public void showHint(String s, Boolean play_video) {
        myDialog.setContentView(R.layout.popup_hint);
        //播放视频
        VideoView videoView = myDialog.findViewById(R.id.railing_video);
        videoView.setVideoURI(Uri.parse("android.resource://" + getPackageName() + "/" + R.raw.railing));
        TextView hint = myDialog.findViewById(R.id.hint_text);
        hint.setText(s);
        if (play_video) {
            videoView.setVisibility(View.VISIBLE);
        } else {
            videoView.setVisibility(View.GONE);
        }
        myDialog.show();
        if (play_video) {
            videoView.requestFocus();
            videoView.start();
        }
    }

    public void clickPlaySettingsVideo(View view) {
        VideoView videoView = findViewById(R.id.settings_video);
        videoView.setVideoURI(Uri.parse("android.resource://" + getPackageName() + "/" + R.raw.ape));
        videoView.requestFocus();
        videoView.start();
    }

}
