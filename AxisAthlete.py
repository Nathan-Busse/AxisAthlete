import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import os
from datetime import timedelta

class AxisAthleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AxisAthlete - 3D Printer Motion System Exercise Generator")
        self.root.geometry("850x1300")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with branding
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=10)
        
        title_label = ttk.Label(title_frame, text="⚙️ AxisAthlete", 
                               font=("Arial", 18, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="3D Printer Motion System Exercise Generator", 
                                  font=("Arial", 10, "italic"))
        subtitle_label.pack()
        
        # --- FIRMWARE SELECTION SECTION ---
        firmware_frame = ttk.LabelFrame(main_frame, text="🖥️ FIRMWARE SELECTION", padding="10")
        firmware_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(firmware_frame, text="Select your printer's firmware:",
                 font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        self.firmware_var = tk.StringVar(value="")
        firmware_options = ["Marlin 1.x", "Marlin 2.x", "Klipper"]
        
        for i, firmware in enumerate(firmware_options):
            ttk.Radiobutton(firmware_frame, text=firmware, variable=self.firmware_var, 
                           value=firmware, command=self.on_firmware_changed).grid(row=1, column=i, sticky=tk.W, padx=10, pady=5)
        
        # HELP BUTTON (Restored)
        help_btn = ttk.Button(firmware_frame, text="❓ How to identify my firmware", 
                             command=self.show_firmware_help)
        help_btn.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        self.firmware_info = ttk.Label(firmware_frame, text="ℹ️ Select a firmware to generate compatible G-Code",
                                      font=("Arial", 8, "italic"), foreground="darkblue")
        self.firmware_info.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # --- SAFETY CHECK SECTION (Restored) ---
        safety_frame = ttk.LabelFrame(main_frame, text="⚠️ SAFETY CHECK - FILAMENT STATUS", padding="10")
        safety_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.filament_var = tk.StringVar(value="")
        ttk.Label(safety_frame, text="Is filament currently installed? (yes/no):").grid(row=0, column=0, sticky=tk.W)
        self.filament_entry = ttk.Entry(safety_frame, textvariable=self.filament_var, width=15)
        self.filament_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.filament_entry.bind('<KeyRelease>', lambda e: self.check_filament_status())
        
        self.status_label = ttk.Label(safety_frame, text="Status: Awaiting confirmation (type 'yes' or 'no')...", 
                                     font=("Arial", 9, "italic"), foreground="orange")
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # --- INPUT PARAMETERS ---
        input_frame = ttk.LabelFrame(main_frame, text="📊 Bed Dimensions & Cycles", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.length_var = tk.DoubleVar(value=220.0)
        self.width_var = tk.DoubleVar(value=220.0)
        self.height_var = tk.DoubleVar(value=220.0)
        self.cycles_var = tk.IntVar(value=9)
        self.zhop_var = tk.DoubleVar(value=2.0)

        params = [
            ("Printable X Length (mm):", self.length_var),
            ("Printable Y Width (mm):", self.width_var),
            ("Printable Z Height (mm):", self.height_var),
            ("Exercise Cycles:", self.cycles_var),
            ("Z-Hop Height (mm):", self.zhop_var)
        ]
        
        for i, (label_text, var) in enumerate(params):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            ent = ttk.Entry(input_frame, textvariable=var, width=15)
            ent.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            ent.bind('<KeyRelease>', lambda e: self.update_calculations())

        # --- SPEED PROFILE SECTION (Restored + New Fields) ---
        speed_frame = ttk.LabelFrame(main_frame, text="⚡ Speed Profile (mm/min)", padding="10")
        speed_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.print_speed_var = tk.DoubleVar(value=3000.0)
        self.travel_speed_var = tk.DoubleVar(value=6000.0)
        self.retraction_speed_var = tk.DoubleVar(value=1800.0)

        speeds = [
            ("Exercise (Print) Speed:", self.print_speed_var),
            ("Positioning (Travel) Speed:", self.travel_speed_var),
            ("Z / Retraction Speed:", self.retraction_speed_var)
        ]

        for i, (label_text, var) in enumerate(speeds):
            ttk.Label(speed_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
            ent = ttk.Entry(speed_frame, textvariable=var, width=15)
            ent.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            ent.bind('<KeyRelease>', lambda e: self.update_calculations())
            if i == 0: self.print_speed_entry = ent

        self.feedrate_status = ttk.Label(speed_frame, text="🔒 Safety Lock Active", 
                                        font=("Arial", 8, "italic"), foreground="red")
        self.feedrate_status.grid(row=0, column=2, padx=5)

        # --- CALCULATIONS & BUTTONS ---
        calc_frame = ttk.LabelFrame(main_frame, text="📈 Estimates", padding="10")
        calc_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.distance_label = ttk.Label(calc_frame, text="Total Travel Distance: 0.00 mm")
        self.distance_label.grid(row=0, column=0, padx=20)
        
        self.time_label = ttk.Label(calc_frame, text="Estimated Duration: 00:00:00")
        self.time_label.grid(row=0, column=1, padx=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.generate_btn = ttk.Button(button_frame, text="🚀 Generate G-Code", command=self.generate_gcode, state=tk.DISABLED)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🔄 Reset Values", command=self.reset_values).pack(side=tk.LEFT, padx=5)

        # Preview area
        self.preview_text = tk.Text(main_frame, height=12, width=90, font=("Courier", 8))
        self.preview_text.grid(row=7, column=0, columnspan=3, pady=10)

        # Internals
        self.safety_confirmed = False
        self.filament_installed = None

    def show_firmware_help(self):
        """Show detailed firmware identification guide - FULL TEXT RESTORED"""
        firmware_help = """
🖥️ HOW TO IDENTIFY YOUR PRINTER'S FIRMWARE
============================================

MARLIN 1.x - Classic Firmware
────────────────────────────
Features:
  • Older firmware version
  • Used on Prusa i3, Original Ender 3, etc.

How to check:
  1. Send M115 command via serial console
  2. Look for version output (e.g., "1.1.8")

MARLIN 2.x - Modern Firmware
────────────────────────────
Features:
  • Modern enhanced version (2.0+)
  • Used on newer Ender 3 models, CR-10, etc.

How to check:
  1. Send M115 command via serial console
  2. Look for version output (e.g., "2.0.7")

KLIPPER - High-Performance Firmware
────────────────────────────────────
Features:
  • Runs on separate host computer (Pi, etc.)
  • GROWING in popularity

How to check:
  1. Check if printer connected to Raspberry Pi/Linux
  2. Look for Mainsail, Fluidd, or Octoprint interface
"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Firmware Identification Guide")
        help_window.geometry("600x600")
        scrollbar = ttk.Scrollbar(help_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget = tk.Text(help_window, yscrollcommand=scrollbar.set, font=("Courier", 9), wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert(1.0, firmware_help)
        text_widget.config(state=tk.DISABLED)

    def on_firmware_changed(self):
        """Handle firmware selection change - FULL LOGIC RESTORED"""
        firmware = self.firmware_var.get()
        firmware_info_map = {
            "Marlin 1.x": "✅ Marlin 1.x selected - Classic firmware syntax",
            "Marlin 2.x": "✅ Marlin 2.x selected - Modern firmware with advanced features",
            "Klipper": "✅ Klipper selected - High-performance firmware system"
        }
        self.firmware_info.config(text=firmware_info_map.get(firmware, ""))
        self.update_ui_state()

    def check_filament_status(self):
        """Check user input for filament status - FULL LOGIC RESTORED"""
        user_input = self.filament_var.get().strip().lower()
        if user_input == "yes":
            self.filament_installed = True
            self.safety_confirmed = True
            self.print_speed_var.set(0.0)
            self.print_speed_entry.config(state=tk.DISABLED)
            self.status_label.config(text="⚠️ Filament Detected: Extruder protection active.", foreground="red")
            self.feedrate_status.config(text="🔒 Speed Locked (Safety)", foreground="red")
        elif user_input == "no":
            self.filament_installed = False
            self.safety_confirmed = True
            self.print_speed_entry.config(state=tk.NORMAL)
            self.status_label.config(text="✅ No Filament: Full exercise motion enabled.", foreground="green")
            self.feedrate_status.config(text="🔓 Speed Unlocked", foreground="green")
        else:
            self.safety_confirmed = False
            self.status_label.config(text="Status: Awaiting confirmation (type 'yes' or 'no')...", foreground="orange")
            self.feedrate_status.config(text="🔒 Safety Lock Active", foreground="red")
        
        self.update_ui_state()

    def update_ui_state(self):
        if self.safety_confirmed and self.firmware_var.get():
            self.generate_btn.config(state=tk.NORMAL)
        else:
            self.generate_btn.config(state=tk.DISABLED)
        self.update_calculations()

    def update_calculations(self):
        try:
            length = self.length_var.get()
            width = self.width_var.get()
            cycles = self.cycles_var.get()
            speed = self.print_speed_var.get()
            
            # Distance logic: sweeps + diagonal per cycle
            dist_per_cycle = (length + width) * 2 + math.sqrt(length**2 + width**2)
            total_dist = dist_per_cycle * cycles
            
            self.distance_label.config(text=f"Total Travel Distance: {total_dist:,.2f} mm")
            
            if speed > 0:
                mins = total_dist / speed
                self.time_label.config(text=f"Estimated Duration: {str(timedelta(minutes=mins)).split('.')[0]}")
            else:
                self.time_label.config(text="Estimated Duration: --:--:--")
        except:
            pass

    def generate_gcode(self):
        """RESTORED: Main generation logic with Windows fix"""
        # Explicitly fetch into local scope to prevent NameError on some OS environments
        firmware = self.firmware_var.get()
        zhop = self.zhop_var.get()
        l = self.length_var.get()
        w = self.width_var.get()
        h = self.height_var.get()
        c = self.cycles_var.get()
        p_speed = self.print_speed_var.get()
        t_speed = self.travel_speed_var.get()
        r_speed = self.retraction_speed_var.get()
        fil_inst = self.filament_installed

        try:
            if firmware == "Marlin 1.x":
                gcode = self.create_marlin1_gcode(l, w, h, c, p_speed, t_speed, r_speed, zhop, fil_inst)
            elif firmware == "Marlin 2.x":
                gcode = self.create_marlin2_gcode(l, w, h, c, p_speed, t_speed, r_speed, zhop, fil_inst)
            else:
                gcode = self.create_klipper_gcode(l, w, h, c, p_speed, t_speed, r_speed, zhop, fil_inst)

            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, gcode)
            
            path = filedialog.asksaveasfilename(defaultextension=".gcode", 
                                               title="Save Exercise G-Code",
                                               initialfile=f"AxisAthlete_{firmware.replace(' ', '_')}.gcode")
            if path:
                with open(path, 'w') as f:
                    f.write(gcode)
                messagebox.showinfo("Success", f"G-Code successfully generated for {firmware}!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate G-Code: {str(e)}")

    def create_marlin1_gcode(self, length, width, height, cycles, p_speed, t_speed, r_speed, zhop, filament_installed):
        g = [f"; AxisAthlete - Marlin 1.x", "G90 ; Absolute", "G28 ; Home"]
        if filament_installed: g.append("M18 E ; Disable Extruder")
        
        g.append(f"G0 Z{zhop} F{r_speed} ; Initial Z-Hop")
        g.append(f"G0 X10 Y10 F{t_speed} ; Initial Travel Position")
        
        for i in range(1, cycles + 1):
            g.append(f"; --- Cycle {i} ---")
            g.append(f"G0 X{length-10} F{p_speed} ; X Sweep")
            g.append(f"G0 Y{width-10} ; Y Sweep")
            g.append("G0 X10")
            g.append("G0 Y10")
            g.append(f"G0 X{length-10} Y{width-10} ; Diagonal Move")
            
            z_height = (height / cycles) * i
            g.append(f"G0 Z{z_height} F{r_speed} ; Layer Increment")
            g.append(f"G0 X10 Y10 F{p_speed} ; Return Travel")
            
        g.append("G28 ; Return Home")
        g.append("M84 ; Steppers Off")
        return "\n".join(g)

    def create_marlin2_gcode(self, length, width, height, cycles, p_speed, t_speed, r_speed, zhop, filament_installed):
        g = [f"; AxisAthlete - Marlin 2.x", "G90", "M117 AxisAthlete Start", "G28"]
        if filament_installed: g.append("M18 E")
        
        g.append(f"G0 Z{zhop} F{r_speed}")
        g.append(f"G0 X10 Y10 F{t_speed}")
        
        for i in range(1, cycles + 1):
            g.append(f"; --- Cycle {i} ---")
            g.append(f"G0 X{length-10} F{p_speed}")
            g.append(f"G0 Y{width-10}")
            g.append("G0 X10")
            g.append("G0 Y10")
            g.append(f"G0 X{length-10} Y{width-10}")
            
            z_height = (height / cycles) * i
            g.append(f"G0 Z{z_height} F{r_speed}")
            g.append(f"G0 X10 Y10 F{p_speed}")
            
        g.append("M117 Exercise Complete")
        g.append("G28\nM84")
        return "\n".join(g)

    def create_klipper_gcode(self, length, width, height, cycles, p_speed, t_speed, r_speed, zhop, filament_installed):
        # Corrected: Klipper uses mm/min, ensuring no extra multiplier is added erroneously
        g = [f"; AxisAthlete - Klipper", "G90", "G28"]
        if filament_installed: g.append("SET_STEPPER_ENABLE STEPPER=extruder ENABLE=0")
        
        g.append(f"G0 Z{zhop} F{r_speed}")
        g.append(f"G0 X10 Y10 F{t_speed}")
        
        for i in range(1, cycles + 1):
            g.append(f"; Cycle {i}")
            g.append(f"G0 X{length-10} F{p_speed}")
            g.append(f"G0 Y{width-10}")
            g.append("G0 X10")
            g.append("G0 Y10")
            g.append(f"G0 X{length-10} Y{width-10}")
            
            z_height = (height / cycles) * i
            g.append(f"G0 Z{z_height} F{r_speed}")
            g.append(f"G0 X10 Y10 F{p_speed}")
            
        g.append("G28\nM84")
        return "\n".join(g)

    def reset_values(self):
        """Reset all values to defaults - FULL LOGIC RESTORED"""
        self.length_var.set(220.0)
        self.width_var.set(220.0)
        self.height_var.set(220.0)
        self.cycles_var.set(9)
        self.zhop_var.set(2.0)
        self.print_speed_var.set(3000.0)
        self.travel_speed_var.set(6000.0)
        self.retraction_speed_var.set(1800.0)
        self.filament_var.set("")
        self.firmware_var.set("")
        self.preview_text.delete(1.0, tk.END)
        
        # Reset safety confirmation
        self.safety_confirmed = False
        self.filament_installed = None
        self.status_label.config(text="Status: Awaiting confirmation...", foreground="orange")
        self.print_speed_entry.config(state=tk.NORMAL)
        self.feedrate_status.config(text="🔒 Safety Lock Active", foreground="red")
        self.firmware_info.config(text="ℹ️ Select a firmware profile")
        self.update_ui_state()

if __name__ == "__main__":
    root = tk.Tk()
    app = AxisAthleteApp(root)
    root.mainloop()
