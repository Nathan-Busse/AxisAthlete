; ========================================
; AxisAthlete - Motion System Exercise
; Firmware: Marlin 2.x
; 3D Printer Firmware Testing & Calibration
; ========================================
; Build Dimensions: 220.0mm (X) x 220.0mm (Y) x 220.0mm (Z)
; Exercise Cycles: 9
; Feed Rate: 0.0 mm/min
; Z-Hop Distance: 2.0 mm
; 
; Purpose: Extended motion testing for:
;   - Stepper motor endurance
;   - Mechanical stress testing
;   - Firmware stability verification
;   - Calibration & tuning
; 
; ⚠️ FILAMENT PROTECTION MODE ENABLED ⚠️
;   - Extruder stepper motor: DISABLED
;   - Extruder will NOT move
;   - No filament extrusion
;   - XYZ axes exercise only
; ========================================

G90 ; Absolute positioning
G28 ; Home all axes
G0 F0.0 ; Set feedrate

; *** EXTRUDER STEPPER DISABLED FOR PROTECTION ***
M18 E ; Disable extruder stepper motor

G0 X10 Y10 Z5 F0.0 ; Move to start position

; --- Exercise Cycle 1 of 9 ---
M117 CYCLE 1 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 2 of 9 ---
M117 CYCLE 2 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 3 of 9 ---
M117 CYCLE 3 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 4 of 9 ---
M117 CYCLE 4 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 5 of 9 ---
M117 CYCLE 5 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 6 of 9 ---
M117 CYCLE 6 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 7 of 9 ---
M117 CYCLE 7 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 8 of 9 ---
M117 CYCLE 8 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; --- Exercise Cycle 9 of 9 ---
M117 CYCLE 9 OF 9
; Z-Axis Movement
G0 Z10
G0 Z55
G0 Z110
G0 Z165
G0 Z210
G0 Z165
G0 Z110
G0 Z55
G0 Z10
; X-Axis Movement
G0 X10
G0 X55
G0 X110
G0 X165
G0 X210
G0 X165
G0 X110
G0 X55
G0 X10
; Y-Axis Movement
G0 Y10
G0 Y55
G0 Y110
G0 Y165
G0 Y210
G0 Y165
G0 Y110
G0 Y55
G0 Y10
; Diagonal Movement (XY)
G0 X210 Y210
G0 X10 Y10
G0 X210 Y10
G0 X10 Y210
G0 X10 Y10 Z10 F0.0

; ========================================
; Exercise Complete
; ========================================
G0 Z20 F0.0 ; Raise Z
G28 ; Return home
M84 ; Disable stepper motors
M117 AxisAthlete Complete!
; End of G-Code