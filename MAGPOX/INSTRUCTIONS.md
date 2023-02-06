INSTRUCTIONS

The script is designed to automate running the MAGPOX program for any amount of compositions desired.

**WARNING!! THIS VERSION CONTAINS NO ERROR HANDLING MECHANISMS AND SHOULD DATA BE PROVIDED TO IT IN A WAY THAT IS NOT THE SPECIFIED IN THE PROVIDED EXAMPLES YOU MAY NOT BE WARNED OR NOTIFIED ABOUT MISTAKES IN THE CALCULATIONS. BEWARE OF THE ORDER THE COMPONENT COLUMNS IN THE EXAMPLES AS IT MUST REMAIN AS PRESENTED, OTHERWISE THE PROGRAM WILL THINK IT IS GETTING A DIFFERENT COMPOSITION. DO NOT ADD ADDITIONAL DATA OR COMPONENTS.**

This script requires an executable file for a modified version of MAGPOX. Since we cannot distribute the code for copyright reasons, we provide instructions on how to modify the original publicly available files and how to compile the executable file.

The program and compilation should be done on any Linux system (including WSL) or mac (untested). Check the REQUIREMENTS.md file for information of required python libraries and fortran compilers required for running the program.

0.- Download all files from this repository into a folder.

1.- Download the SPICES suite of programs from https://www.lpi.usra.edu/lunar/tools/crystallizationcalculation/

2.- Follow the directories to reach ../SPICE_Programs/Programs/MAGPOX and copy the magpox.f90 file into the folder where the python script is located. No other file is needed.

3.- Open the magpox.f90 file with a text editor, preferably Notepad++ or similar, or IDE. Make sure you can see the line numbers.

4.- After line 33 ("WRITE(6,3330)") add a new line with the following: OPEN(UNIT=9,FILE='INPUTER.txt',ACCESS='SEQUENTIAL',STATUS='OLD'). Delete this same command from line 43 (initially 42) as well as the CLOSE(9) from line 51 (initially 51). Do not leave empty lines when deleting.

5.- Replace line 49 for: READ(9,3333) inp

6.- Change the "READ(5," part of lines 56, 70, 74, 77, 79 and 81 for "READ(9,", just change the 5 for 9, do not modify any other part of the lines.

7.- After line 81 add a new line with the following: CLOSE(9)

8.- You are now ready to compile the program, save your changes on the same file or change the name if you desire to keep the original, but keep the .f90 extension. If using the recommended compiler, gfortran, you only need to use the console of your system. Go to the directory where the modified MAGFOX version is located and do the following command: "gfortran magpox.f90 -o a3.out" (ignore the "). If you saved the modified file with a different name, replace magfox.f90 for the name of your file. This should create an executable file named a3.out, the script will call this file to run the program.

13.-You may now run the program. As default it will fractionate at steps of 1% crystallization increments until 99 % crystallization is done at 2 bars of pressure. You may modify the the Execute.py for crystallization step in line 4, endpoint in line 5 and pressure in line 6 (in bars). Additional options from the program are comented in the code.

14.- Make sure all files from this repository and the executable a3.out file are all located in the same folder. Make sure all python libraries required are installed. You are now ready to run the program, you may do so from the console by typing: python3 automagfox.py in linux, or python automagfox.py from Windows.

15.- Once the program is finished, a new Results folder will appear with the results of each sample on their own folder named after the names in the comp.txt file. MAGPOX returns 4 text files: the dat file contains a summary of all the process; the liq file shows the evolution of the liquid composition; the xtl file shows the endmember composition of crystal phases, the wfx file shows the abundances of crystalline phases. **WARNING: RUNNING THE PROGRAM A SECOND TIME WILL ERASE THE PREVIOUS RESULTS FOLDER, IF YOU WISH TO SAVE YOUR DATA YOU WILL NEED TO MANUALLY MOVE IT INTO ANOTHER FOLDER.**