import numpy as np
import pandas as pd
import multiprocessing as mp
import os
import platform
import pathlib
import shutil as sh
import subprocess

dir_path = pathlib.Path(__file__).parent.parent.as_posix() 
bin_folder = dir_path + "/bin/"
src_folder = dir_path + "/src/"
results_folder = dir_path + "/results/"
op_system = platform.system()

def Auto_build(source,temp,pressure,mp="optimal"):

    """Automates the creation of building files to be processed through vertex by using a template file 
    and the 'build.exe' command
    
    Input: 
        source: tab delimited file with all samples to be used and their composition in columns.
                First column must contain all element names and first row all sample names.

        temp: list with initial and final temperature for modelling, ex: [1000,2000]

        pressure: list with initial and final pressures for modelling in bar, ex [1,30000]

        mp : type of multiprocessing, default "optimal". Options are:
                 "optimal": for having as much instancesas possible without intereference from each other and minimal from os
                 "intense": for having as much instances as cores in the CPU
                 "single": for a single instance.
                 int: manually define the number of instances you want to open, should not be higher than amount of compositions.

    
    Return:
        names2: List of file names produced, corresponding to the sample names (without spaces) as txt files"""

    # Reading input file
    source_file = pd.read_csv(source,delimiter="\t",index_col=0)
    ind = source_file.index
    cols = source_file.columns

    # Current template asks for SiO2, TiO2, Al2O3, Cr2O3, FeO, MnO, MgO, CaO, Na2O, K2O
    # Testing availability or mistakes.
    
    if ("SiO2" in ind and "TiO2" in ind and "Al2O3" in ind and "Cr2O3" in ind and "FeO" in ind
     and "MnO" in ind and "MgO" in ind and "CaO" in ind and "Na2O" in ind and "K2O" in ind):
        print("All components present, continuing")
    else:
        print("One or more components are missing or mispelled, check source file")
        return
    
    sio2 = source_file.loc["SiO2"]
    elements = source_file.loc["SiO2":"K2O"]
   
    # Importing template directories: fh= first half, sh = second half, elements go between
    template_1_fh = open(dir_path+"/templates/template1_first_half.txt","r")
    fh = template_1_fh.read().replace("temp1",str(temp[0])).replace("temp2",str(temp[1])).replace("pressure1",str(pressure[0])).replace("pressure2",str(pressure[1]))
    template_1_sh = open(dir_path+"/templates/template2_second_half.txt","r")
    sec_h = template_1_sh.read()
    template_1_sh.close()
    template_1_fh.close()

    # Starting loop for writing input files
    for i, val in enumerate(cols):
        val2 = val.replace(" ","")
        if os.path.exists(str(val2)+".txt"):
            os.remove(str(val2)+".txt")
        
        c_file = open(str(val2)+".txt","w")
        c_file.write(str(val2)+"\n")
        c_file.write(fh+"\n")

        for t in elements[val]:
            c_file.write(str(t)+"\n")

        
        c_file.write(sec_h)
        c_file.close()
    
    names = cols+".txt"
    names = names.tolist()

    names2 = []
    for n in names:
        n2 = n.replace(" ","")
        names2.append(n2)

    echo_file_mover(names2, folder="bin")

    for l in names2:
        build_command(l)

    batcher (names2,multiprocessing=mp)

    return(names2)

def build_command(file):
    """Runs a command on cmd that executes the perple_x build
    with automatic input from a constructed file
    
    input: file: must be a string with the name of the file"""
    

    if os.path.exists(bin_folder + file.replace(".txt",".dat")):
        os.remove(bin_folder + file.replace(".txt",".dat"))

    ring = "cd " + bin_folder + "&& build <"+str(file)
    subprocess.run(ring,shell=True,stdout=subprocess.DEVNULL)

def batcher(source, multiprocessing = "optimal"):
    """Creates batch or bash files from which we can process all compositions with multiple instances of vertex
    Input
        source: directory of file with compositions
        multiprocessing: type of multiprocessing, default "optimal". Options are:
                 "optimal": for having as much instancesas possible without intereference from each other and minimal from os
                 "intense": for having as much instances as cores in the CPU
                 "single": for a single instance.
                 int: manually define the number of instances you want to open, should not be higher than amount of compositions."""
    
    # Cpu core count and multiprocessing definitions
    cores =os.cpu_count()
    if multiprocessing == "optimal":
        if cores == 1 or cores == 2:
            c = 0
        elif cores == 3 or cores == 4:
            c = 1
        elif cores == 5 or cores == 6:
            c = 2
        elif cores == 7:
            c = 3
        elif cores >= 8:
            c = cores - 4
    if multiprocessing == "intense":
        c = cores-1
    if multiprocessing == "single":
        c = 0
    
    if type(multiprocessing) == int:
        c = multiprocessing

    # File writing
    if "Windows" in op_system:
        if os.path.exists(bin_folder+"runner.bat"):
                os.remove(bin_folder+"runner.bat")
        filey = open(bin_folder+"runner.bat","x")
        filey.write("cd " + bin_folder + "\n")
        for v in range(c+1):
            if os.path.exists(bin_folder+"batch"+ str(v+1) + ".bat"):
                os.remove(bin_folder+"batch"+ str(v+1) + ".bat")
            filex = open(bin_folder+"batch"+ str(v+1) + ".bat","x")
            filex.close()
            filey.write("start "+'''"'''+"batch"+ str(v+1) + ".bat"+'''" '''+"batch"+ str(v+1) + ".bat\n")
        counter = 1
        for h in source:
            counter = counter + 1
            if counter <= c+1 and counter > 1:
                filex = open(bin_folder+"batch"+ str(counter) + ".bat","a")
                filex.write("echo "+ h.replace(".txt","") + " |vertex\n")
                filex.close()

            else:
                counter = 1
                filex = open(bin_folder+"batch"+ str(counter) + ".bat","a")
                filex.write("echo "+ h.replace(".txt","") + " |vertex\n")
                filex.close()
        filey.close()
    else:
        if os.path.exists(bin_folder+"runner.sh"):
                os.remove(bin_folder+"runner.sh")
        filey = open(bin_folder+"runner.sh","x")
        filey.write("#!/bin/sh\n" + "cd " + bin_folder + "\n")
        for v in range(c+1):
            if os.path.exists(bin_folder+"batch"+ str(v+1) + ".sh"):
                os.remove(bin_folder+"batch"+ str(v+1) + ".sh")
            filex = open(bin_folder+"batch"+ str(v+1) + ".sh","x")
            filex.write("#!/bin/sh")
            filex.close()
            filey.write("start "+'''"'''+"batch"+ str(v+1) + ".sh"+'''" '''+"batch"+ str(v+1) + ".sh\n")
        counter = 1
        for h in source:
            counter = counter + 1
            if counter <= c+1 and counter > 1:
                filex = open(bin_folder+"batch"+ str(counter) + ".sh","a")
                filex.write("echo "+ h.replace(".txt","") + " |vertex\n")
                filex.close()
            else:
                counter = 1
                filex = open(bin_folder+"batch"+ str(counter) + ".sh","a")
                filex.write("echo "+ h.replace(".txt","") + " |vertex\n")
                filex.close()
        filey.close()
        
def echo_file_mover(source,folder="results"):
    """Moves the files generated by the Auto_build function to the results or bin folders
    
    Input:
        source: Return of the Auto_build function.
        folder: Either "results" or "bin" for the corresponding folder
    Return
        No return"""
    
    if folder=="results":
        copying_folder = results_folder
    elif folder == "bin":
        copying_folder = bin_folder
    else:
        print("location not available")

    for echo_file in source:
        # Removing file on copy location
        if os.path.exists(copying_folder+echo_file):
            os.remove(copying_folder+echo_file)

        # copying file
        sh.copy(echo_file,copying_folder)

        # removing file on main location
        os.remove(echo_file)

def mover (source, destination):
    """Moves perple_x files from build and vertex functions from source to destination
        
    Input
        source: composition name
        destination: Folder path
        
    Returns
        No return"""

    folder= destination + source +"/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_extensions = [".tof",".arf",".blk",".plt",".tim",".dat","_auto_refine.txt","_seismic_data.txt",".txt"]
    for i in file_extensions:
        if os.path.exists(bin_folder + str(source) + i):
            sh.copy(bin_folder + str(source) + i, folder)
    for i in file_extensions:
        if os.path.exists(bin_folder + str(source) + i):
            os.remove(bin_folder + str(source) + i)

def runner():
    if "Windows" in op_system:
        subprocess.call("cd " + bin_folder + "&& call runner.bat",shell=True)
    else:
        subprocess.call("bash " + bin_folder + "runner.sh",shell=True)