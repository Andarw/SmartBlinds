package com.example.smartblinds.ui.home;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.example.smartblinds.R;
import com.example.smartblinds.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;
    private float[] pvalue;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        HomeViewModel homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView text_temp = binding.textTemp;
        final TextView text_hum = binding.textHum;
        final TextView text_light = binding.textLight;
        final  TextView text_4 = binding.textView4;
        homeViewModel.getTextTemp().observe(getViewLifecycleOwner(), text_temp::setText);
        homeViewModel.getTextHum().observe(getViewLifecycleOwner(), text_hum::setText);
        homeViewModel.getTextLight().observe(getViewLifecycleOwner(), text_light::setText);
        homeViewModel.getText4().observe(getViewLifecycleOwner(), text_4::setText);
        pvalue = homeViewModel.ConnectToGet();
        TextView temp = binding.textView;
        temp.setText(String.valueOf(pvalue[0]) + "\u00B0");
        TextView hum = binding.textView2;
        hum.setText(String.valueOf(pvalue[1]) + "%");
        TextView lint = binding.textView3;
        lint.setText(String.valueOf(pvalue[2]) + "%");
        ImageButton refbtn = binding.ref2;

        refbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Navigation.findNavController(v).navigate(R.id.navigation_home);

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