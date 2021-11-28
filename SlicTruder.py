#A barebones Python script for generating G-code for the Recreator 3D
#Created by the Autotrude project https://wikifactory.com/@greenellipsis/autotrude/
#Released under the terms of the Creative Commons International 4.0 Attribution license (CC BY 4.0)
#Ver 0.1 added despool option

#Change these slicer parameters as needed
action=1              # 1 - pultrude, 2 - despool
DespoolSpeed = 1200
ExtruderSpeed = 300*0.55   # mm/min
ExtruderDistance = 0.1  # per G-code command
Etotal = 60000         # total amount to extrude, in mm
NozzleTemp = 220          # nozzle temperature
start_gcode = "M302 P1 ;allow cold extrude\n" \
              "M83 ;extruder relative mode\n"

def despool():
    fname= "DS" + str(Etotal) + "@F" + str(DespoolSpeed) + ".gcode"
    f= open(fname,"w+")
    f.write(start_gcode)
    f.write("M117 Despooling\n")
    f.write("G1 E0 F" + str(ExtruderSpeed) + " ;set default feed rate\n")
    Eposition = 0
    while Eposition <= Etotal:
        f.write("G1 E-" + str(ExtruderDistance)+"\n")
        Eposition += ExtruderDistance
    f.write("M300 ; play tone\n")
    f.write("M18 ;disable steppers\n")
    f.close()


def pultrude():
    fname= str(Etotal) + "@F" + str(ExtruderSpeed) + "@S" + str(NozzleTemp) + ".gcode"
    f= open(fname,"w+")
    f.write(start_gcode)
    f.write("M109 S" + str(NozzleTemp) + "\n")
    f.write("M117 RECREATING FILAMENT\n")
    f.write("G1 E0 F" + str(ExtruderSpeed) + " ;set default feed rate\n")
    f.write("M83 ;extruder relative mode\n")
    Eposition = 0
    while Eposition <= Etotal:
        f.write("G1 E" + str(ExtruderDistance)+"\n")
        Eposition += ExtruderDistance
    f.write("M300 ; play tone\n")
    f.write("M104 S0 ;turn off nozzle heater\n")
    f.write("M18 ;disable steppers\n")
    f.close()

if action==1:
        pultrude()
elif action==2:
        despool()
else:
        print("unknown Function")
