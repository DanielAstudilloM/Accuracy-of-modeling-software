Instructions

For this script to work please first check that all the requirements are met.

You need a modified build of the MELTS-batch build in the MELTS repository (https://gitlab.com/ENKI-portal/xMELTS) that defaults calculations to the pMELTS engine. For copyright reasons we are not allowed to share the modified files but it is a simple procedure:

    1) Obtain access to the MELTS repository (https://gitlab.com/ENKI-portal/xMELTS) and download its contents
    2) Got to the sources folder and find the interface.c file. Open with a text editor, ideally one that enumerates lines (e.g. Notepad++)
    3) Modify the file by commenting (adding // to the beggining of the line) lines 2181 and 2182 and remove the comment from lines 2187 and 2188.
    4) Follow the instrucions on the readme file of the MELTS repository in order to create the MELTS-batch build.
    5) The resulting executable file needs to be moved to the folder where the python script of this work is located.

To run the script, you need to put your compositions into a tab delimited file, like the one in the example of compositions.txt. Be careful of putting things in the right order as this version won't tell you if there is an error in the input data. Oxygen fugacities are: 
    "iw" for IW buffer
    "coh" for CCO buffer
    "fmq" for QFM buffer
    "nno" for NNO buffer
    "hm" for HM buffer
No offsets work with this version

In the script you need to change line 340 for the values you would like to use (in the structure of the comment in lines 337-338). 

You need to run the script through a windows console (either cmd or powershell) and it should automatically run all of the compositions in the provided set, if WSL is properly set up.