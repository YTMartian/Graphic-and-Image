package com.example.carlicense;

import android.app.Dialog;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
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
        server_ip = "192.168.137.1";
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
    public void clickOpenCamera(View view) {

    }

    //点击get_in按钮
    public void clickGetIn(View view) {
        FloatingActionButton button = findViewById(R.id.get_in);
        //弹出确认框
        myDialog.setContentView(R.layout.popup);
        //注意应在myDialog下find，否则就是空指针错误
        MyImageView license_plate_image = myDialog.findViewById(R.id.license_plate_image);
        TextView license_plate_text = myDialog.findViewById(R.id.license_plate_text);
        TextView car_type = myDialog.findViewById(R.id.car_type);
        TextView now_time = myDialog.findViewById(R.id.now_time);
        TextView pay_toll = myDialog.findViewById(R.id.pay_toll);
        //更改按钮图标和文字
        if (is_get_in) {
            button.setImageResource(R.drawable.ic_get_in);
            button.setLabelText("进入");
            pay_toll.setVisibility(View.VISIBLE);
            myDialog.show();
            license_plate_image.setImageURL("http://www.potatochip.cn/wallpaper-118.jpg");
        } else {
            button.setImageResource(R.drawable.ic_get_out);
            button.setLabelText("离开");
            pay_toll.setVisibility(View.GONE);
            myDialog.show();
            license_plate_image.setImageURL("http://www.potatochip.cn/wallpaper-112.jpg");
        }
        is_get_in = !is_get_in;
    }

    //点击确定按钮
    public void clickEnsure(View view) {
        myDialog.dismiss();
    }

    //点击更改ip按钮
    public void clickChangeIp(View view) {
        EditText ip = findViewById(R.id.ip_address);
        if (ip.getText().toString().isEmpty()) return;
        server_ip = ip.getText().toString();
        myDialog.setContentView(R.layout.popup_ip_ensure);
        TextView ip_address_hint = myDialog.findViewById(R.id.ip_address_hint);
        ip_address_hint.setText(ip_address_hint.getText() + server_ip);
        myDialog.show();
    }

}
