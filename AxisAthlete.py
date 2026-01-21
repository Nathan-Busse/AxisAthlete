import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import os
from datetime import timedelta

class AxisAthleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AxisAthlete - 3D Printer Motion System Exercise Generator")
        self.root.geometry("800x1150")
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
        
        # Help button for firmware identification
        help_btn = ttk.Button(firmware_frame, text="❓ How to identify my firmware", 
                             command=self.show_firmware_help)
        help_btn.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Firmware info label
        self.firmware_info = ttk.Label(firmware_frame, text="ℹ️ Select a firmware to generate compatible G-Code",
                                      font=("Arial", 8, "italic"), foreground="darkblue")
        self.firmware_info.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # --- SAFETY CHECK SECTION ---
        safety_frame = ttk.LabelFrame(main_frame, text="⚠️ SAFETY CHECK - FILAMENT STATUS", padding="10")
        safety_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        safety_label = ttk.Label(safety_frame, 
                                text="Is filament currently installed in your 3D printer?",
                                font=("Arial", 10, "bold"))
        safety_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Instructions
        instructions_label = ttk.Label(safety_frame,
                                      text="Type 'yes' or 'no' in the field below:",
                                      font=("Arial", 9, "italic"), foreground="darkblue")
        instructions_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Filament status variable
        self.filament_var = tk.StringVar(value="")
        
        # Entry field for yes/no
        ttk.Label(safety_frame, text="Filament Status:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.filament_entry = ttk.Entry(safety_frame, textvariable=self.filament_var, width=15)
        self.filament_entry.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.filament_entry.bind('<KeyRelease>', lambda e: self.check_filament_status())
        
        # Status display
        self.status_label = ttk.Label(safety_frame, text="Status: Awaiting confirmation...", 
                                     font=("Arial", 9, "italic"), foreground="orange")
        self.status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Info box
        info_text = ttk.Label(safety_frame, 
                             text="ℹ️ For optimal results, remove filament before exercise.\n"
                                  "Store filament in an airtight container to prevent moisture absorption.",
                             font=("Arial", 8), justify=tk.LEFT, foreground="darkblue")
        info_text.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # --- INPUT SECTION ---
        input_frame = ttk.LabelFrame(main_frame, text="📊 Input Parameters", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Print Length
        ttk.Label(input_frame, text="Printable area (X-axis) in (mm):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.DoubleVar(value=220.0)
        self.length_entry = ttk.Entry(input_frame, textvariable=self.length_var, width=15)
        self.length_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.length_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Print Width
        ttk.Label(input_frame, text="Printable area (Y-axis) in (mm):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.DoubleVar(value=220.0)
        self.width_entry = ttk.Entry(input_frame, textvariable=self.width_var, width=15)
        self.width_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.width_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Print Height
        ttk.Label(input_frame, text="Printable area (Z-axis) in (mm):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.DoubleVar(value=220.0)
        self.height_entry = ttk.Entry(input_frame, textvariable=self.height_var, width=15)
        self.height_entry.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.height_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Number of Cycles
        ttk.Label(input_frame, text="Number of Exercise Cycles:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cycles_var = tk.IntVar(value=9)
        self.cycles_entry = ttk.Entry(input_frame, textvariable=self.cycles_var, width=15)
        self.cycles_entry.grid(row=3, column=1, sticky=tk.W, padx=5)
        self.cycles_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Feed Rate
        ttk.Label(input_frame, text="Feed Rate (mm/min):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.feedrate_var = tk.DoubleVar(value=100.0)
        self.feedrate_entry = ttk.Entry(input_frame, textvariable=self.feedrate_var, width=15, state=tk.DISABLED)
        self.feedrate_entry.grid(row=4, column=1, sticky=tk.W, padx=5)
        self.feedrate_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Feed Rate Status Label
        self.feedrate_status = ttk.Label(input_frame, text="🔒 Disabled (awaiting safety confirmation)", 
                                        font=("Arial", 8, "italic"), foreground="red")
        self.feedrate_status.grid(row=4, column=2, sticky=tk.W, padx=5)
        
        # Z Hop Distance
        ttk.Label(input_frame, text="Z Hop Distance (mm):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.zhop_var = tk.DoubleVar(value=2.0)
        self.zhop_entry = ttk.Entry(input_frame, textvariable=self.zhop_var, width=15)
        self.zhop_entry.grid(row=5, column=1, sticky=tk.W, padx=5)
        self.zhop_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # --- CALCULATIONS SECTION ---
        calc_frame = ttk.LabelFrame(main_frame, text="📈 Calculated Values", padding="10")
        calc_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Total Distance
        ttk.Label(calc_frame, text="Total Distance:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.distance_label = ttk.Label(calc_frame, text="0.00 mm", font=("Arial", 11, "bold"), foreground="blue")
        self.distance_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Estimated Time
        ttk.Label(calc_frame, text="Estimated Duration:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.time_label = ttk.Label(calc_frame, text="00:00:00", font=("Arial", 11, "bold"), foreground="green")
        self.time_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Line Count
        ttk.Label(calc_frame, text="Estimated G-Code Lines:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.lines_label = ttk.Label(calc_frame, text="0", font=("Arial", 11, "bold"), foreground="darkblue")
        self.lines_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # --- BUTTON SECTION ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        self.generate_btn = ttk.Button(button_frame, text="🚀 Generate Exercise", 
                                       command=self.generate_gcode, state=tk.DISABLED)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(button_frame, text="🔄 Reset", command=self.reset_values)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # --- PREVIEW SECTION ---
        preview_frame = ttk.LabelFrame(main_frame, text="📝 G-Code Preview", padding="10")
        preview_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Scrollbar for preview
        scrollbar = ttk.Scrollbar(preview_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.preview_text = tk.Text(preview_frame, height=10, width=85, 
                                     yscrollcommand=scrollbar.set, font=("Courier", 8))
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.preview_text.yview)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Track safety confirmation
        self.safety_confirmed = False
        self.filament_installed = None
        
        # Initial calculation
        self.update_calculations()
    
    def show_firmware_help(self):
        """Show detailed firmware identification guide"""
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
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Firmware Identification Guide")
        help_window.geometry("700x700")
        
        # Create text widget with scrollbar
        scrollbar = ttk.Scrollbar(help_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(help_window, yscrollcommand=scrollbar.set, 
                             font=("Courier", 9), wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(1.0, firmware_help)
        text_widget.config(state=tk.DISABLED)
    
    def on_firmware_changed(self):
        """Handle firmware selection change"""
        firmware = self.firmware_var.get()
        firmware_info_map = {
            "Marlin 1.x": "✅ Marlin 1.x selected - Classic firmware syntax",
            "Marlin 2.x": "✅ Marlin 2.x selected - Modern firmware with advanced features",
            "Klipper": "✅ Klipper selected - High-performance firmware system"
        }
        self.firmware_info.config(text=firmware_info_map.get(firmware, ""))
        self.update_generate_btn_state()
    
    def check_filament_status(self):
        """Check user input for filament status"""
        user_input = self.filament_var.get().strip().lower()
        if user_input == "yes":
            self.filament_yes()
        elif user_input == "no":
            self.filament_no()
        else:
            self.safety_confirmed = False
            self.filament_installed = None
            self.status_label.config(text="Status: Awaiting confirmation (type 'yes' or 'no')...", 
                                    foreground="orange")
            self.feedrate_entry.config(state=tk.DISABLED)
            self.feedrate_var.set(100.0)
            self.update_generate_btn_state()
    
    def filament_yes(self):
        """User confirms filament is installed"""
        self.filament_installed = True
        self.safety_confirmed = True
        self.feedrate_entry.config(state=tk.DISABLED)
        self.feedrate_var.set(0.0)
        self.feedrate_status.config(text="🔒 DISABLED - Extruder stepper disabled.", foreground="red")
        self.status_label.config(text="⚠️ Status: Filament detected. Extruder disabled.", foreground="red")
        self.update_generate_btn_state()
        self.update_calculations()
    
    def filament_no(self):
        """User confirms filament is NOT installed"""
        self.filament_installed = False
        self.safety_confirmed = True
        self.feedrate_entry.config(state=tk.NORMAL)
        self.feedrate_var.set(100.0)
        self.feedrate_status.config(text="✅ Enabled - Safe to operate", foreground="green")
        self.status_label.config(text="✅ Status: Filament removed. Safe to proceed.", foreground="green")
        self.update_generate_btn_state()
        self.update_calculations()
    
    def update_generate_btn_state(self):
        """Update generate button state"""
        if self.safety_confirmed and self.firmware_var.get():
            self.generate_btn.config(state=tk.NORMAL)
        else:
            self.generate_btn.config(state=tk.DISABLED)
    
    def update_calculations(self):
        """Update calculations when parameters change"""
        try:
            length = self.length_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            cycles = self.cycles_var.get()
            feedrate = self.feedrate_var.get()
            
            if length <= 0 or width <= 0 or height <= 0 or cycles <= 0 or (not self.filament_installed and feedrate <= 0):
                return
            
            distance_per_cycle = (2 * length) + (2 * width) + (2 * height)
            total_distance = distance_per_cycle * cycles
            
            if feedrate > 0:
                time_seconds = (total_distance / feedrate) * 60
                hours, minutes = divmod(int(time_seconds // 60), 60)
                seconds = int(time_seconds % 60)
                self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            else:
                self.time_label.config(text="N/A")
                
            self.distance_label.config(text=f"{total_distance:.2f} mm")
            self.lines_label.config(text=str((5 * cycles) + 15))
        except (tk.TclError, ValueError):
            pass
    
    def generate_gcode(self):
        """Generate G-Code based on user parameters"""
        firmware = self.firmware_var.get()
        if not firmware:
            messagebox.showerror("Firmware Required", "Please select a firmware first.")
            return
        
        if not self.safety_confirmed:
            messagebox.showerror("Safety Check Required", "Please confirm filament status.")
            return
            
        try:
            # Defined missing variables by getting them from GUI objects
            length = self.length_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            cycles = self.cycles_var.get()
            feedrate = self.feedrate_var.get()
            zhop = self.zhop_var.get()
            
            min_feed = 0.0 if self.filament_installed else 0.1
            if length <= 0 or width <= 0 or height <= 0 or cycles <= 0 or feedrate < min_feed:
                messagebox.showerror("Input Error", "Please ensure all dimensions are positive.")
                return            

            gcode = self.create_gcode(length, width, height, cycles, feedrate, zhop, 
                                     self.filament_installed, firmware)
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, '\n'.join(gcode.split('\n')[:25]))
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".gcode",
                filetypes=[("G-Code files", "*.gcode"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(gcode)
                
                msg = f"G-Code generated!\n\nFirmware: {firmware}\nFile: {os.path.basename(file_path)}"
                if self.filament_installed:
                    msg += "\n⚠️ Extruder motor is DISABLED."
                messagebox.showinfo("✅ Success", msg)
        
        except (tk.TclError, ValueError):
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields")
    
    def create_gcode(self, length, width, height, cycles, feedrate, zhop, filament_installed, firmware):
        if firmware == "Marlin 1.x":
            return self.create_marlin1_gcode(length, width, height, cycles, feedrate, zhop, filament_installed)
        elif firmware == "Marlin 2.x":
            return self.create_marlin2_gcode(length, width, height, cycles, feedrate, zhop, filament_installed)
        elif firmware == "Klipper":
            return self.create_klipper_gcode(length, width, height, cycles, feedrate, zhop, filament_installed)
    
    def create_marlin1_gcode(self, length, width, height, cycles, feedrate, zhop, filament_installed):
        gcode = ["; AxisAthlete - Marlin 1.x", "G90", "G28"]
        if filament_installed: gcode.append("M18 E")
        gcode.append(f"G0 X10 Y10 Z5 F{feedrate}")
        for c in range(1, cycles + 1):
            gcode.append(f"; Cycle {c}")
            gcode.append(f"G0 Z{height}")
            gcode.append(f"G0 X{length-10} Y{width-10}")
            gcode.append("G0 X10 Y10 Z5")
        gcode.append("G28\nM84")
        return '\n'.join(gcode)

    def create_marlin2_gcode(self, length, width, height, cycles, feedrate, zhop, filament_installed):
        gcode = ["; AxisAthlete - Marlin 2.x", "G90", "G28"]
        if filament_installed: gcode.append("M18 E")
        gcode.append(f"G0 X10 Y10 Z5 F{feedrate}")
        for c in range(1, cycles + 1):
            gcode.append(f"; Cycle {c}")
            gcode.append(f"G0 Z{height}")
            gcode.append(f"G0 X{length-10} Y{width-10}")
            gcode.append("G0 X10 Y10 Z5")
        gcode.append("G28\nM84")
        return '\n'.join(gcode)

    def create_klipper_gcode(self, length, width, height, cycles, feedrate, zhop, filament_installed):
        # Corrected: Klipper G-code commands use mm/min, not mm/s
        gcode = ["; AxisAthlete - Klipper", "G90", "G28"]
        if filament_installed: gcode.append("SET_STEPPER_ENABLE STEPPER=extruder ENABLE=0")
        gcode.append(f"G0 X10 Y10 Z5 F{feedrate}")
        for c in range(1, cycles + 1):
            gcode.append(f"; Cycle {c}")
            gcode.append(f"G0 Z{height}")
            gcode.append(f"G0 X{length-10} Y{width-10}")
            gcode.append("G0 X10 Y10 Z5")
        gcode.append("G28\nM84")
        return '\n'.join(gcode)
    
    def reset_values(self):
        self.length_var.set(220.0); self.width_var.set(220.0); self.height_var.set(220.0)
        self.cycles_var.set(9); self.feedrate_var.set(100.0); self.zhop_var.set(2.0)
        self.filament_var.set(""); self.firmware_var.set(""); self.preview_text.delete(1.0, tk.END)
        self.safety_confirmed = False; self.filament_installed = None
        self.status_label.config(text="Status: Awaiting confirmation...", foreground="orange")
        self.feedrate_entry.config(state=tk.DISABLED); self.update_calculations()

if __name__ == "__main__":
    root = tk.Tk()
    app = AxisAthleteApp(root)
    root.mainloop()
