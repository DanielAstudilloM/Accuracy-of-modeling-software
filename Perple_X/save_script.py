import src.Autoperplex as AP
import os


# Input pressure in bars
initial_pressure = 1
final_pressure = 30000

# input temperature in K
initial_temp = 1273
final_temp = 2073

# File with stored compositions (see instructions)
file_name = "compositions.txt"

# setup
temps = [initial_temp,final_temp]
pressures = [initial_pressure,final_pressure]

# Building
source = AP.Auto_build(file_name, temps, pressures, mp="optimal")
# mover function
for echo_file in source:
    AP.mover(echo_file.replace(".txt",""),AP.results_folder)