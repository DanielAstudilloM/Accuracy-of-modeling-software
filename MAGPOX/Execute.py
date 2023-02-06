import AutoMPX as AM

# Conditions (see runner function)
pmin=1
pmax=30
inc=1
file="template.xlsx"

# Steps and max crystallization are defaulted to 0.01 and 0.99 in the runner function, 
# they can be adjusted by changing the default values of crx_rate and crx_max default values of the runner function
# For Example: runner (fle,pmax,pmin,inc,crx_rate=0.05,crx_max=0.7)

# Change sys value for: wsl for windows subsystem for linux, win for windows (with windows executable which doesn't work so far)
# and linux if using linux (only tested on ubuntu)

# It is also plotting the first appearance of phases using the reported endmember data. You can choose to do it through
# the modal abundance report which will give slightly different values but will also show ilmenite, spinel and silica.
# To do this change the type value of the runner function from xtl to wfx.

x = AM.runner(file,pmax,pmin,inc,sys="wsl",type= "wfx")
AM.plot(x)

