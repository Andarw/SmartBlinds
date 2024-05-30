package com.example.smartblinds.ui.dashboard;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.SeekBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.example.smartblinds.R;
import com.example.smartblinds.databinding.FragmentDashboard2Binding;

public class DashboardFragment2 extends Fragment {

    private FragmentDashboard2Binding binding;

    private int[] pvalue;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        DashboardViewModel2 dashboardViewModel2 =
                new ViewModelProvider(this).get(DashboardViewModel2.class);

        binding = FragmentDashboard2Binding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textDashboard;
        dashboardViewModel2.getText().observe(getViewLifecycleOwner(), textView::setText);
        pvalue = dashboardViewModel2.ConnectToGet();
        Button btn2auto = binding.btn2auto;
        SeekBar seekb = binding.seekbar;
        SeekBar seekb2 = binding.seekbar2;
        seekb.setProgress(pvalue[0]);
        seekb2.setProgress(pvalue[1]);
        Button setbtn = binding.seekbarset;
        ImageButton refbtn = binding.seekref;

        seekb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                pvalue[0] = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        seekb2.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                pvalue[1] = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        btn2auto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Navigation.findNavController(v).navigate(R.id.navigation_dashboard);

            }
        });

        setbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dashboardViewModel2.ConnectToSet(pvalue);

            }
        });

        refbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Navigation.findNavController(v).navigate(R.id.navigation_dashboard2);

            }
        });
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}