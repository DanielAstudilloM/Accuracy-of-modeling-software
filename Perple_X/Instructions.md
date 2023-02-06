Instructions

Make sure you have all requirements installed. All Perple_X files need to be contained in the bin folder.
To get the Perple_X software go to https://www.perplex.ethz.ch/

Data and samples should go in the compositions.txt file in that format. You can put as many samples as you want and it will automatically detect oxide compositions for SiO2, TiO2, Al2O3, FeO, MgO, MnO, Cr2O3, CaO, Na2O, K2O. Any additional data in the file will be ignored. Avoid using special characters for sample names and spaces will not be used for the results names.

If you wish to have different setups for the build function, you have to modify the template to be the exact input you would use in it. On the template folder, template_fh_descriptions.txt has the description of all possible answers for the build function. template1_first_half.txt should contain all your answers up until the input of concentrations of components. Do not modify the temp1, temp2, pressure1 and pressure 2 steps, you will define them within the function.
template2_second_half.txt contains all that comes after the concentrations, the existing file contains excluded phases and solution phases already, they can be added or removed following the ones already there.

You can freely add as much components as Perple_x will allow, we don't recommend removing the existing ones, try setting them to 0 in the compositions.txt file instead. If you wish to remove them, you will also need to modify the Auto_build function in the Autoperplex.py file to ignore that component. Feel free to contact me if you wish to do so.

We realize that the template setup is complicated and we are currently reverse engineering the logic of the build function in order to include the answers within the function. It will be available in a new version soon.

To run the program run the run_script.py from the main folder, modify the file, temperature and pressure variables in the script to use your files and pressure/temperature conditions. After calculations are finished, use the save_script.py to save your data to the results folder. Notice that the save script requires the same input as the running script, modifying the composition file or the conditions will result in build files (.dat) that don't correspond to the used ones saved to the folder.

Also note that if you repeat the sample names after you already ran them once, your previous data will be deleted. Move your results before doing that.

On the src folder there is a psser.bat script that can be copied to the bin folder which will run the pssect command with all the samples within the script, modify it to include all your sample names in the same format as the examples, copy it to the bin folder and run it to get all phase diagrams. You must do this before using the save script as all the data needs to be on the bin folder.