# ui_components.py
import customtkinter as ctk

def setup_control_panel(parent, on_slider_change, on_solve, on_reset):
    """
    Yeh function control widgets banayega aur unke actions ko 
    main app ke functions se connect (callback) karega.
    """
    control_frame = ctk.CTkFrame(parent, fg_color="transparent")
    control_frame.pack(pady=15)

    # 1. Slider Label
    slider_label = ctk.CTkLabel(control_frame, text="Disks: 3", font=("Helvetica", 15, "bold"))
    slider_label.grid(row=1, column=1, padx=20)

    
    def slider_callback(value):
        slider_label.configure(text=f"Disks: {int(value)}")
        on_slider_change(value)

   
    disk_slider = ctk.CTkSlider(control_frame, from_=1, to=8, number_of_steps=7, command=slider_callback)
    disk_slider.set(3)
    disk_slider.grid(row=0, column=1, padx=20)

  
    solve_button = ctk.CTkButton(control_frame, text="AUTO SOLVE", fg_color="#00A86B", hover_color="#008753", 
                                 command=on_solve)
    solve_button.grid(row=0, column=4, padx=20)

   
    reset_button = ctk.CTkButton(control_frame, text="RESET", fg_color="#D9534F", hover_color="#C9302C", 
                                 command=on_reset)
    reset_button.grid(row=0, column=0, padx=20)

    
    speed_slider = ctk.CTkSlider(control_frame, from_=100, to=2000, number_of_steps=19)
    speed_slider.set(500)
    speed_slider.grid(row=2, column=1, padx=20)

   
    speed_label = ctk.CTkLabel(control_frame, text="Speed (ms)", font=("Helvetica", 12))
    speed_label.grid(row=3, column=1, padx=20)

    status_label = ctk.CTkLabel(parent, text="Total Moves: 0 | Moves Left: 0", font=("Helvetica", 14, "italic"), text_color="#05D9E8")
    status_label.pack(pady=5)
    
    return disk_slider, speed_slider, status_label