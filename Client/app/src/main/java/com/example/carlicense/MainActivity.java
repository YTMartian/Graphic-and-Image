package com.example.carlicense;

import android.graphics.Camera;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
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
    boolean camera_is_play = false;
    boolean is_get_in=false;
    Camera camera;

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
                //放入HomeFragment.
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new HomeFragment()).commit();
                break;
            case R.id.nav_settings:
                menu.hideMenu(true);
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new SettingsFragment()).commit();
                break;
            case R.id.nav_about:
                menu.hideMenu(true);
                getSupportFragmentManager().beginTransaction().replace(R.id.nav_host_fragment,
                        new AboutFragment()).commit();
                break;
        }
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    //点击open_camera按钮
    public void clickOpenCamera(View view) {
        FloatingActionButton button = findViewById(R.id.open_camera);
        //更改按钮图标和文字
        if (camera_is_play) {
            button.setImageResource(R.drawable.ic_camera_play);
            button.setLabelText("开始");
        } else {
            button.setImageResource(R.drawable.ic_camera_stop);
            button.setLabelText("停止");
        }
        camera_is_play = !camera_is_play;
    }

    //点击get_in按钮
    public void clickGetIn(View view) {
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
    }

}
