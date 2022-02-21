#A barebones Python script for generating G-code for the Recreator 3D
#Created by the Autotrude project https://wikifactory.com/@greenellipsis/autotrude/
#Released under the terms of the Creative Commons International 4.0 Attribution license (CC BY 4.0)
#Ver 0.1 added despool option
import PySimpleGUI as sg

#Change these slicer parameters as needed
action=1            # 1 - pultrude, 2 - despool
DespoolSpeed = 1200
ExtruderSpeed = 325   # mm/min
ExtruderDistance = 0.2  # per G-code command
Etotal = 60000         # total amount to extrude, in mm
NozzleTemp = 235          # nozzle temperature
NozzleTempPrime = 235     # nozzle temperature while priming
PrimingDistance = 200     # mm
start_gcode = "M302 P1 ;allow cold extrude\n" \
              "M83 ;extruder relative mode\n" \
              "M405 ;filament width sensor on\n" \
              "M503 E3000 ;max E feedrate\n" \
              "M75 ; start job timer\n"
stop_gcode = "M18 ;disable steppers\n" \
             "M77 ; stop job timer\n" \
            "M78 ; display jobs stats\n" \
             "M300 ; play tone\n" \
            "M117 T20 RECREATING FILAMENT\n" \
                ""
prime_end_gcode = "M0 ; wait for user\n"
periodic_gcode = "M407\n"
period = 5 #every 10 mm

# main
layout = [
    [sg.T('')]
]
window

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
    f.write(stop_gcode)
    f.close()


def pultrude():
    fname= f'gcode/{Etotal}@F{ExtruderSpeed}@S{NozzleTemp}.gcode'
    print("Writing " + fname + "...\n")
    f= open(fname,"w+")
    f.write(start_gcode)
    f.write("M109 S" + str(NozzleTempPrime) + "\n")
    f.write("G1 E0 F" + str(ExtruderSpeed) + " ;set default feed rate\n")
    Eposition = 0
    donePriming = False
    while Eposition <= Etotal:
        if not donePriming and Eposition > PrimingDistance :
            donePriming = True
            f.write("M104 S" + str(NozzleTemp) + "\n")
        f.write("G1 E" + str(ExtruderDistance)+"\n")
        Eposition += ExtruderDistance
        if Eposition % period < ExtruderDistance:
            f.write(periodic_gcode)
    f.write("M104 S0 ;turn off nozzle heater\n")
    f.write(stop_gcode)
    f.close()
    print("Done\n")

if action==1:
        pultrude()
elif action==2:
        despool()
else:
        print("unknown Function")
