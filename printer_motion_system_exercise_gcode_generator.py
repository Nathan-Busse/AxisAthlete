import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import os
from datetime import timedelta

class AxisAthleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AxisAthlete - 3D Printer Motion System Exercise Generator")
        self.root.geometry("700x850")
        self.root.resizable(False, False)
        
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
        
        # --- INPUT SECTION ---
        input_frame = ttk.LabelFrame(main_frame, text="📊 Input Parameters", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
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
        self.feedrate_entry = ttk.Entry(input_frame, textvariable=self.feedrate_var, width=15)
        self.feedrate_entry.grid(row=4, column=1, sticky=tk.W, padx=5)
        self.feedrate_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # Z Hop Distance
        ttk.Label(input_frame, text="Z Hop Distance (mm):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.zhop_var = tk.DoubleVar(value=2.0)
        self.zhop_entry = ttk.Entry(input_frame, textvariable=self.zhop_var, width=15)
        self.zhop_entry.grid(row=5, column=1, sticky=tk.W, padx=5)
        self.zhop_entry.bind('<KeyRelease>', lambda e: self.update_calculations())
        
        # --- CALCULATIONS SECTION ---
        calc_frame = ttk.LabelFrame(main_frame, text="📈 Calculated Values", padding="10")
        calc_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
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
        button_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        generate_btn = ttk.Button(button_frame, text="🚀 Generate Exercise", command=self.generate_gcode)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(button_frame, text="🔄 Reset", command=self.reset_values)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # --- PREVIEW SECTION ---
        preview_frame = ttk.LabelFrame(main_frame, text="📝 G-Code Preview", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Scrollbar for preview
        scrollbar = ttk.Scrollbar(preview_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.preview_text = tk.Text(preview_frame, height=12, width=85, 
                                     yscrollcommand=scrollbar.set, font=("Courier", 8))
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.preview_text.yview)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Initial calculation
        self.update_calculations()
    
    def update_calculations(self):
        """Update calculations when parameters change"""
        try:
            length = self.length_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            cycles = self.cycles_var.get()
            feedrate = self.feedrate_var.get()
            
            # Validate inputs
            if length <= 0 or width <= 0 or height <= 0 or cycles <= 0 or feedrate <= 0:
                return
            
            # Calculate total distance (rectangular path per cycle + Z movements)
            # X-axis: 2 passes (back and forth)
            # Y-axis: 2 passes (back and forth)
            # Z-axis: up and down movements
            distance_per_cycle = (2 * length) + (2 * width) + (2 * height)
            total_distance = distance_per_cycle * cycles
            
            # Calculate time (in minutes, then convert to seconds)
            time_minutes = total_distance / feedrate
            time_seconds = time_minutes * 60
            
            hours = int(time_seconds // 3600)
            minutes = int((time_seconds % 3600) // 60)
            seconds = int(time_seconds % 60)
            
            # Calculate estimated lines (4 corners per cycle + header/footer)
            lines_per_cycle = 5  # 4 corners + Z-hop
            estimated_lines = (lines_per_cycle * cycles) + 15  # +15 for header/footer
            
            # Update labels
            self.distance_label.config(text=f"{total_distance:.2f} mm ({total_distance/1000:.2f} m)")
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.lines_label.config(text=str(estimated_lines))
            
        except (tk.TclError, ValueError):
            pass
    
    def generate_gcode(self):
        """Generate G-Code based on user parameters"""
        try:
            length = self.length_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            cycles = self.cycles_var.get()
            feedrate = self.feedrate_var.get()
            zhop = self.zhop_var.get()
            
            # Validate inputs
            if length <= 0 or width <= 0 or height <= 0 or cycles <= 0 or feedrate <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            # Generate G-Code
            gcode = self.create_gcode(length, width, height, cycles, feedrate, zhop)
            
            # Display preview
            self.preview_text.delete(1.0, tk.END)
            preview_lines = gcode.split('\n')[:25]
            self.preview_text.insert(tk.END, '\n'.join(preview_lines))
            self.preview_text.insert(tk.END, f"\n\n... ({len(gcode.split(chr(10)))} total lines)")
            
            # Save file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".gcode",
                filetypes=[("G-Code files", "*.gcode"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(gcode)
                
                messagebox.showinfo("✅ Success", 
                                  f"Exercise G-Code generated successfully!\n\n"
                                  f"File: {os.path.basename(file_path)}\n"
                                  f"Location: {os.path.dirname(file_path)}")
        
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields")
    
    def create_gcode(self, length, width, height, cycles, feedrate, zhop):
        """Create G-Code string for motion system exercise"""
        gcode = []
        
        # Header
        gcode.append("; ========================================")
        gcode.append("; AxisAthlete - Motion System Exercise")
        gcode.append("; 3D Printer Firmware Testing & Calibration")
        gcode.append("; ========================================")
        gcode.append(f"; Build Dimensions: {length}mm (X) x {width}mm (Y) x {height}mm (Z)")
        gcode.append(f"; Exercise Cycles: {cycles}")
        gcode.append(f"; Feed Rate: {feedrate} mm/min")
        gcode.append(f"; Z-Hop Distance: {zhop} mm")
        gcode.append("; ")
        gcode.append("; Purpose: Extended motion testing for:")
        gcode.append(";   - Stepper motor endurance")
        gcode.append(";   - Mechanical stress testing")
        gcode.append(";   - Firmware stability verification")
        gcode.append(";   - Calibration & tuning")
        gcode.append("; ========================================")
        gcode.append("")
        
        # Initialize
        gcode.append("G90 ; Absolute positioning")
        gcode.append("G21 ; Metric units")
        gcode.append("G28 ; Home all axes")
        gcode.append(f"F{feedrate} ; Set feed rate")
        gcode.append("")
        
        # Starting position
        start_x, start_y, start_z = 10.0, 10.0, 5.0
        current_x, current_y, current_z = start_x, start_y, start_z
        
        gcode.append(f"G0 X{current_x} Y{current_y} Z{current_z} ; Move to start position")
        gcode.append("")
        
        # Cycles
        for cycle in range(1, cycles + 1):
            gcode.append(f"; --- Exercise Cycle {cycle} of {cycles} ---")
            gcode.append(f"M117 CYCLE {cycle} OF {cycles}")
            
            # Z-Axis Exercise
            gcode.append("; Z-Axis Movement")
            z_positions = [10, 55, 110, 165, 210, 165, 110, 55, 10]
            for z in z_positions:
                gcode.append(f"G0 Z{z}")
            
            # X-Axis Exercise
            gcode.append("; X-Axis Movement")
            x_positions = [10, 55, 110, 165, 210, 165, 110, 55, 10]
            for x in x_positions:
                gcode.append(f"G0 X{x}")
            
            # Y-Axis Exercise
            gcode.append("; Y-Axis Movement")
            y_positions = [10, 55, 110, 165, 210, 165, 110, 55, 10]
            for y in y_positions:
                gcode.append(f"G0 Y{y}")
            
            # Diagonal Exercise (XY plane)
            gcode.append("; Diagonal Movement (XY)")
            gcode.append("G0 X210 Y210")
            gcode.append("G0 X10 Y10")
            gcode.append("G0 X210 Y10")
            gcode.append("G0 X10 Y210")
            gcode.append("G0 X10 Y10")
            
            # Return to start position
            gcode.append("G0 X10 Y10 Z10")
            gcode.append("")
        
        # Finalization
        gcode.append("; ========================================")
        gcode.append("; Exercise Complete - Return to Home")
        gcode.append("; ========================================")
        gcode.append("G0 Z20 ; Raise Z for safety")
        gcode.append("G28 ; Return to home position")
        gcode.append("M84 ; Disable stepper motors (motors relax)")
        gcode.append("M117 AxisAthlete Exercise Complete!")
        gcode.append("")
        gcode.append("; End of G-Code")
        
        return '\n'.join(gcode)
    
    def reset_values(self):
        """Reset all values to defaults"""
        self.length_var.set(220.0)
        self.width_var.set(220.0)
        self.height_var.set(220.0)
        self.cycles_var.set(9)
        self.feedrate_var.set(100.0)
        self.zhop_var.set(2.0)
        self.preview_text.delete(1.0, tk.END)
        self.update_calculations()

def main():
    root = tk.Tk()
    app = AxisAthleteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()