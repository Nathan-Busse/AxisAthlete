6# ⚙️ AxisAthlete

## 3D Printer Motion System Exercise Generator

A comprehensive Python application for generating firmware-specific G-Code to exercise and stress-test 3D printer motion systems. Perfect for firmware validation, calibration, and mechanical endurance testing.

---

## 🎯 Purpose

AxisAthlete provides extended motion testing for 3D printers to:

- **Test Stepper Motor Endurance**: Run continuous motion cycles to validate stepper motor performance under extended use
- **Mechanical Stress Testing**: Exercise all axes simultaneously to identify mechanical issues, backlash, or binding
- **Firmware Stability Verification**: Ensure your printer's firmware handles complex motion sequences reliably
- **Calibration & Tuning**: Fine-tune acceleration, jerk, and feedrate settings with controlled test patterns
- **Pre-Print Validation**: Verify all motion axes are functioning correctly before critical prints

---

## ✨ Features

### 🖥️ Multi-Firmware Support
- **Marlin 1.x** - Classic firmware with traditional G-Code syntax
- **Marlin 2.x** - Modern firmware with advanced features and enhanced commands
- **Klipper** - High-performance firmware system with optimized motion planning

### 🛡️ Safety Features
- **Filament Protection Mode**: Automatically disables extruder stepper when filament is set as present by the user.
- **Feed Rate Controls**: Automatically locks feed rate when filament is present to prevent unwanted extrusion


### 📊 Real-Time Calculations
- **Total Distance Calculation**: Computes total movement distance across all cycles
- **Estimated Duration**: Calculates expected runtime based on feed rate and distance
- **Line Count Estimation**: Shows estimated G-Code line count for file size planning

### 📈 Customizable Parameters
- **Build Dimensions**: Define your printer's printable area (X, Y, Z axes)
- **Exercise Cycles**: Specify number of test cycles (supports 1-1000+ cycles)
- **Feed Rate Control**: Adjustable movement speed (when safe to do so)
- **Z-Hop Distance**: Configure Z-axis hop for future compatibility

### 📝 G-Code Preview
- Real-time preview of generated G-Code
- First 25 lines displayed for quick validation
- Total line count for reference

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation

```bash
# Clone or download the repository
cd exercise_printer

# Run the application
python [printer_motion_system_exercise_gcode_generator.py](http://_vscodecontentref_/0)
