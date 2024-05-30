package com.example.smartblinds.ui.notifications;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.example.smartblinds.R;
import com.example.smartblinds.databinding.FragmentNotificationsBinding;

public class NotificationsFragment extends Fragment {

    private FragmentNotificationsBinding binding;
    private int[] pvalue;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        NotificationsViewModel notificationsViewModel =
                new ViewModelProvider(this).get(NotificationsViewModel.class);

        binding = FragmentNotificationsBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textNotifications;
        notificationsViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
        ImageButton refbtn = binding.ref3;
        Button applybtn = binding.applyrec;
        Button infbtn = binding.infbtn;

        pvalue = notificationsViewModel.ConnectToGet();
        ImageView bpos = binding.bpos;
        ImageView wpos = binding.wpos;
        TextView textbpos = binding.textbrec;
        TextView textwpos = binding.textwrec;
        if(pvalue[0] == 0) {
            bpos.setImageResource(R.drawable.open);
            textbpos.setText("Blind\nPosition:\nOpen");
        }
        else if (pvalue[0] == 1) {
            bpos.setImageResource(R.drawable.semiopen);
            textbpos.setText("Blind\nPosition:\nSemi-Open");
        }
        else if (pvalue[0] == 2) {
            bpos.setImageResource(R.drawable.semiclose);
            textbpos.setText("Blind\nPosition:\nSemi-Closed");
        }
        else if (pvalue[0] == 3) {
            bpos.setImageResource(R.drawable.close);
            textbpos.setText("Blind\nPosition:\nClosed");
        }

        if(pvalue[1] == 0) {
            wpos.setImageResource(R.drawable.wclosed);
            textwpos.setText("Window\nPosition:\nClosed");
        }
        else if (pvalue[1] == 1) {
            wpos.setImageResource(R.drawable.wsemi);
            textwpos.setText("Window\nPosition:\nSemi-Open");
        }
        else if (pvalue[2] == 2) {
            wpos.setImageResource(R.drawable.wopen);
            textwpos.setText("Window\nPosition:\nOpen");
        }

        refbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Navigation.findNavController(v).navigate(R.id.navigation_notifications);

            }
        });

        applybtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                notificationsViewModel.ConnectToSet(pvalue);
            }
        });

        infbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                notificationsViewModel.InferenceRequest();
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