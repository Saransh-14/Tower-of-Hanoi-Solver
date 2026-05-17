# main.py
import customtkinter as ctk
import config as cfg
import logic as lg
import ui_components as ui  # Naya module import kiya

# Global UI Elements
app = None
canvas = None
disk_slider = None
speed_slider = None
disk_object = {}
status_label = None
total_moves_count = 0

def window_setup():
    global app
    app = ctk.CTk()
    app.title("HANOI SOLVER")
    app.resizable(False, False)
    app.geometry(cfg.WINDOW_GEOMETRY)

def canvas_setup():
    global canvas
    canvas = ctk.CTkCanvas(app, width=cfg.CANVAS_WIDTH, height=cfg.CANVAS_HEIGHT, bg=cfg.BG_COLOR, highlightthickness=0)
    canvas.pack(pady=20)

def draw_pegs():
    canvas.create_rectangle(150, 400, 815, 415, fill=cfg.BASE_COLOR, outline="")
    for peg_idx, center_x in cfg.PEG_CENTERS.items():
        canvas.create_oval(center_x - 5, 145, center_x + 4, 155, fill=cfg.PEG_COLOR, outline="")
        canvas.create_rectangle(center_x - 5, 150, center_x + 5, 400, fill=cfg.PEG_COLOR, outline="")
        canvas.create_text(center_x, 430, text=f"PEG {chr(65 + peg_idx)}", fill="white", font=("Helvetica", 11, "bold"))

def draw_disks():
    global disk_object
    for obj_lst in disk_object.values():
        for item in obj_lst: canvas.delete(item)
    disk_object.clear()

    total_disks = len(lg.pegs_data[0]) + len(lg.pegs_data[1]) + len(lg.pegs_data[2])
    if total_disks == 0: return

    disk_height = 200 / total_disks
    max_disk_width, min_disk_width = 180, 50

    for peg_idx in range(3):
        peg_centre = cfg.PEG_CENTERS[peg_idx]
        for i, disk_size in enumerate(lg.pegs_data[peg_idx]):
            disk_width = min_disk_width + (disk_size - 1) * ((max_disk_width - min_disk_width) / (total_disks - 1)) if total_disks > 1 else max_disk_width
            x1, x2 = peg_centre - (disk_width / 2), peg_centre + (disk_width / 2)
            y1, y2 = int(400 - (i + 1) * disk_height),int(400 - (i * disk_height))
            colour = cfg.DISK_COLORS[disk_size % len(cfg.DISK_COLORS)]

            r_oval = canvas.create_oval(x2 - (disk_height * 0.5), y1, x2 + (disk_height * 0.5), y2, fill=colour, outline=colour)
            l_oval = canvas.create_oval(x1 - (disk_height * 0.5), y1, x1 + (disk_height * 0.5), y2, fill=colour, outline=colour)
            rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline=colour)
            text_id = canvas.create_text(peg_centre, (y1 + y2) * 0.5, text=str(disk_size), fill="white", font=("Helvetica", max(8, int(disk_height / 2)), "bold"))

            disk_object[disk_size] = (rect_id, text_id, r_oval, l_oval)

def update_status_bar(moves_left):
    """Status bar ke text ko dynamic neon values ke sath update karega"""
    global status_label, total_moves_count
    if status_label:
        status_label.configure(text=f"Total Moves: {total_moves_count} | Moves Left: {moves_left}")


def handle_slider_move(value):
    global total_moves_count

    num_disks = int(value)
    lg.init_pegs_data(num_disks)

    total_moves_count = (2**num_disks)-1
    update_status_bar(total_moves_count)
    draw_disks()

def move_disks(from_peg, to_peg, on_complete_callback):
    """Disk ko backend se pop karke smoothly slide karte hue target peg par drop karega"""
    global disk_object, app, canvas
    
    if len(lg.pegs_data[from_peg]) == 0:
        if on_complete_callback: on_complete_callback()
        return
    
    # 1. Animation shuru hone se pehle hi backend se disk pop kar lo 
    # taaki new_i nikalte waqt calculations sahi hon
    disk = lg.pegs_data[from_peg].pop()
    
    # Coordinates aur Math nikalna
    old_peg_x = cfg.PEG_CENTERS[from_peg]
    old_i = len(lg.pegs_data[from_peg]) # Purana index (jitni disks bachi hain)
    
    new_peg_x = cfg.PEG_CENTERS[to_peg]
    new_i = len(lg.pegs_data[to_peg]) # Naya index
    
    # Current disk height nikalna
    total_disks = len(lg.pegs_data[0]) + len(lg.pegs_data[1]) + len(lg.pegs_data[2]) + 1
    disk_height = 200 / total_disks
    
    # Start and Target Centers (Y coordinate center-mass par nikalenge)
    start_x = old_peg_x
    start_y = 400 - (old_i + 0.5) * disk_height
    
    target_x = new_peg_x
    target_y = 400 - (new_i + 0.5) * disk_height
    
    # Clearance Height (Poles ke top se thoda upar hawa ka rasta, Y = 100)
    clearance_y = 100
    
    # Moving disk ki saari shape IDs (rect, text, ovals)
    shape_ids = disk_object[disk]
    
    # Step speed control (kitne pixels ka jump lena hai)
    step_pixel = 15 
    
    # --- SUB-ANIMATION LOOP ---
    def animate_step(stage, current_x, current_y):
        if not lg.is_animating:
            # Agar user ne beech mein RESET daba diya, toh animation jhat se rok do
            return

        # STAGE 1: LIFT UP (Hawa mein uthao)
        if stage == 1:
            if current_y > clearance_y:
                dy = -step_pixel
                for sid in shape_ids: canvas.move(sid, 0, dy)
                app.after(10, lambda: animate_step(1, current_x, current_y + dy))
            else:
                animate_step(2, current_x, clearance_y) # Slide stage par bhejo
                
        # STAGE 2: SLIDE HORIZONTALLY (Hawa mein tairao)
        elif stage == 2:
            if abs(current_x - target_x) > step_pixel:
                dx = step_pixel if target_x > current_x else -step_pixel
                for sid in shape_ids: canvas.move(sid, dx, 0)
                app.after(10, lambda: animate_step(2, current_x + dx, current_y))
            else:
                # Exact X align karo taaki float differences na aayein
                exact_dx = target_x - current_x
                for sid in shape_ids: canvas.move(sid, exact_dx, 0)
                animate_step(3, target_x, current_y) # Drop stage par bhejo
                
        # STAGE 3: DROP DOWN (Peg ke andar bithao)
        elif stage == 3:
            if current_y < target_y:
                dy = step_pixel
                for sid in shape_ids: canvas.move(sid, 0, dy)
                app.after(10, lambda: animate_step(3, current_x, current_y + dy))
            else:
                # Exact Y align karo perfect placement ke liye
                exact_dy = target_y - current_y
                for sid in shape_ids: canvas.move(sid, 0, exact_dy)
                
                # --- ANIMATION COMPLETE ---
                # Ab backend memory ko complete karo
                lg.pegs_data[to_peg].append(disk)
                

                draw_disks()
                
                # Main queue ko batao ki "Bhai mera kaam ho gaya, ab tum agla move bhej sakte ho!"
                if on_complete_callback:
                    on_complete_callback()

    # Stage 1 (Lift) se animation trigger kar do
    animate_step(1, start_x, start_y)

# main.py ke andar isey bhi update karo:

def process_next_move():
    """Queue se move uthayega aur slide animation complete hone ka wait karega"""
    if not lg.is_animating: return
    
    if len(lg.moves_queue) > 0:
        update_status_bar(len(lg.moves_queue))
        from_peg, to_peg = lg.moves_queue.pop(0)
        
        # Ek inline function (callback) banaya jo animation khatam hone par chalega
        def on_animation_finish():
            if lg.is_animating:
                # User ke speed slider ke hisab se agla move queue se uthao
                delay = int(speed_slider.get())
                app.after(delay, process_next_move)
                
        # move_disks ko bhej diya aur sath mein callback de diya
        move_disks(from_peg, to_peg, on_animation_finish)
    else:
        lg.is_animating = False
        update_status_bar(0)

def start_solving():
    if lg.is_animating: return
    lg.is_animating = True
    lg.moves_queue.clear()
    lg.hanoi_algo(int(disk_slider.get()), 0, 2, 1)
    process_next_move()

def reset_app():
    lg.is_animating = False
    lg.moves_queue.clear()
    handle_slider_move(disk_slider.get())

# --- ENGINE ROOM ---
window_setup()
canvas_setup()
draw_pegs()

# UI components module se panel inject kiya aur sliders ke handles le liye
disk_slider, speed_slider, status_label= ui.setup_control_panel(app, handle_slider_move, start_solving, reset_app)

# Initial Boot Setup
handle_slider_move(3)
app.mainloop()