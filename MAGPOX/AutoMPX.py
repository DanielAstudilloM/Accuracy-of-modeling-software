# Written By Daniel Astudillo

import os
import numpy as np
import shutil
import subprocess
import pathlib
import pandas as pd
import matplotlib.pyplot as plt


dir_path = pathlib.Path(__file__).parent.as_posix() 
print(dir_path)
os.chdir(dir_path)

def input_2(file):
    """Reads the composition and samples file and creates a variable containing the info to be written into a MAGPOX input file"""
    try:
        fileo=pd.read_excel(file,index_col=0)
    except:
        TypeError("wrong file type")
    # fileo=pd.read_csv(file,dtype='str',delimiter="\t")
    return (fileo)

def outread (a,b):
    """Reads XTL files and exctracts first appearances of minerals into res.txt"""
    if os.path.exists (str(a)+"/res.txt"):
        fileo=np.loadtxt(str(a)+"/xtl"+str(b)+".txt",dtype='str',delimiter="\t",unpack=False)
        x=fileo [1:,1:]
        x = np.where(x=='********',0,x)
        x=x.astype(np.float)
        # print (x)
        g=1
        l=0
        mat=[b,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for t in x[0,1:]:
            for f in x[0:,g]:
                # print (f)
                if f!=0:
                    mat[g]=x[l,0]
                    # g=g
                    break
                l=l+1
            g=g+1
            l=0
        filex=open(str(a)+"/res.txt","a")
        filex.write(str(mat[0])+"\t"+str(mat[1])+"\t"+str(mat[2])+"\t"+str(mat[3])+"\t"+str(mat[4])+"\t"+str(mat[5])+"\t"+str(mat[6])+"\t"+str(mat[7])+"\t"+str(mat[8])+"\n")
        filex.close()
    else:
        fileo=np.loadtxt(str(a)+"/xtl"+str(b)+".txt",dtype='str',delimiter="\t",unpack=False)
        x=fileo [1:,1:]
        x = np.where(x=='********',0,x)
        x=x.astype(np.float)
        # print (x)
        g=1
        l=0
        mat=[b,0,0,0,0,0,0,0,0,0,0,0]
        for t in x[0,1:]:
            for f in x[0:,g]:
                # print (f)
                if f!=0:
                    mat[g]=x[l,0]
                    # g=g
                    break
                l=l+1
            g=g+1
            l=0
        filex=open(str(a)+"/res.txt","x")
        filex.write("pressure\tforsterite\tXanorthite\twollastonite-cpx\tenstatite-cpx\twollastonite-opx\tenstatite-opx\twollastonite-pig\tenstatite-pig\n")
        filex.write(str(mat[0])+"\t"+str(mat[1])+"\t"+str(mat[2])+"\t"+str(mat[3])+"\t"+str(mat[4])+"\t"+str(mat[5])+"\t"+str(mat[6])+"\t"+str(mat[7])+"\t"+str(mat[8])+"\n")
        filex.close()

def outread_wfx (sample,pressure):
    """Reads WFX files and exctracts first appearances of minerals into res.txt"""
    if os.path.exists (str(sample)+"/res.txt"):
        fileo=np.loadtxt(str(sample)+"/wfx"+str(pressure)+".txt",dtype='str',delimiter="\t",unpack=False)
        results_no_cyc=fileo [1:,1:]
        results_no_cyc = np.where(results_no_cyc=='********',0,results_no_cyc)
        results_no_cyc = np.where(results_no_cyc=='********   ',0,results_no_cyc)
        results_no_cyc =results_no_cyc.astype(float)
        # print (x)
        g=1
        l=0
        mat=[pressure,0,0,0,0,0,0,0,0]
        for t in results_no_cyc[0,1:]:
            for f in results_no_cyc[0:,g]:
                # print (f)
                if f!=0:
                    mat[g]=results_no_cyc[l,0]
                    break
                l=l+1
            g=g+1
            l=0
        filex=open(str(sample)+"/res.txt","a")
        for value in mat:
            filex.write(str(value)+"\t")
        filex.write("0\n")
        filex.close()
    else:
        fileo=np.loadtxt(str(sample)+"/wfx"+str(pressure)+".txt",dtype='str',delimiter="\t",unpack=False)
        results_no_cyc = fileo [1:,1:]
        results_no_cyc = np.where(results_no_cyc=='********',0,results_no_cyc)
        results_no_cyc = np.where(results_no_cyc=='********   ',0,results_no_cyc)
        results_no_cyc = results_no_cyc.astype(np.float)
        g=1
        l=0
        mat=[pressure,0,0,0,0,0,0,0,0]
        for t in results_no_cyc[0,1:]:
            for f in results_no_cyc[0:,g]:
                # print (f)
                if f!=0:
                    mat[g]=results_no_cyc[l,0]
                    break
                l=l+1
            g=g+1
            l=0
        filex=open(str(sample)+"/res.txt","x")
        filex.write("pressure\tolivine\tplagioclase\tcpx\topx\tpig\tilm\tspinel\tqz\tzero\n")
        for value in mat:
            filex.write(str(value)+"\t")
        filex.write("0\n")
        filex.close()

def remover():
    """Removes the original MAGPOX result files"""
    if os.path.exists("INPUTER.txt"):
        os.remove("INPUTER.txt")
    if os.path.exists ("MAGPOX.XTL"):
        os.remove("MAGPOX.XTL")
    if os.path.exists ("MAGPOX.WFX"):
        os.remove("MAGPOX.WFX")
    if os.path.exists ("MAGPOX.LIQ"):
        os.remove("MAGPOX.LIQ")
    if os.path.exists ("MAGPOX.DAT"):
        os.remove("MAGPOX.DAT")

def init():
    """Removes old folders and input textfiles"""
    if os.path.exists("Results"):
        shutil.rmtree("Results")
    if os.path.exists("INPUTER.txt"):
        os.remove("INPUTER.txt")
    os.mkdir("Results")

def runner (File_Name,maxP,minP,inc,crx_rate=0.01,crx_max=0.99,sys="win",type="xtl"):
    """Main Algorithm for running MAGPOX and file processing"""
    fileo=input_2(File_Name)
    fileo = fileo.replace(0,0.0001)
    j=1
    init()
    for Sample in fileo.columns:
        os.mkdir("Results/"+str(Sample))
        Sample_Folder="Results/"+str(Sample)
        for Pressure in range(int(minP*10),maxP*10+int(inc*10),int(inc*10)):
            #Removing any remnant files
            remover()
            
            #Creating the MAGPOX readable Input file
            # Comps=input(File_Name,j)
            Comps=fileo.get(Sample)
            filex=open("INPUTER.txt","x")
            # filex.write("today"+"\n"+"2"+"\n"+str(Sample)+"\n"+str(Comps[0])+"\n"+str(Comps[1])+"\n"+str(Comps[2])
            # +"\n"+str(Comps[3])+"\n"+str(Comps[4])+"\n"+str(Comps[5])+"\n"+str(Comps[6])+"\n"+str(Comps[7])+"\n"+str(Comps[8])
            # +"\n"+str(Comps[9])+"\n"+str(Comps[10])+"\n"+str(crx_rate)+"\n"+str(crx_max)+"\n"+str(float(Pressure/10))+"\n"+"2")

            filex.write("today"+"\n"+"2"+"\n"+str(Sample)+"\n"+str(Comps['SIO2'])+"\n"+str(Comps['TIO2'])+"\n"+str(Comps['AL2O3'])
            +"\n"+str(Comps['CR2O3'])+"\n"+str(Comps['FEO'])+"\n"+str(Comps['MGO'])+"\n"+str(Comps['MNO'])+"\n"+str(Comps['CAO'])+"\n"
            +str(Comps['K2O'])+"\n"+str(Comps['NA2O'])+"\n"+str(Comps['FE2O3'])+"\n"+str(crx_rate)+"\n"+str(crx_max)+"\n"+str(float(Pressure/10))+"\n"+"2")
            filex.close()

            #Running MAGPOX
            if sys=="wsl":
                a=subprocess.Popen('wsl cd /mnt/'+dir_path.replace(":","")+'; ./a3.out',shell=True,stdout=subprocess.DEVNULL)
                a.wait()
            if sys=="linux":
                a=subprocess.Popen("./a3.out")
                a.wait()
            if sys=="win":
                line= "magpox2.exe"
                a=subprocess.Popen(line)
                a.wait()
            print("finished")

            #Copying Files to results folder on another format
            shutil.copy(dir_path+"/MAGPOX.XTL",dir_path+"/Results/"+str(Sample)+"/xtl"+str(Pressure)+".txt")
            xtl=open(dir_path+"/Results/"+str(Sample)+"/xtl"+str(Pressure)+".txt", "r",encoding="ISO-8859-1")
            data=xtl.read()
            data= data.replace(" ","")
            xtl.close()
            xtl=open(dir_path+"/Results/"+str(Sample)+"/xtl"+str(Pressure)+".txt","w")
            xtl.write(data)
            xtl.close()
            shutil.copy(dir_path+"/MAGPOX.LIQ",dir_path+"/Results/"+str(Sample)+"/liq"+str(Pressure)+".txt")
            shutil.copy(dir_path+"/MAGPOX.DAT",dir_path+"/Results/"+str(Sample)+"/dat"+str(Pressure)+".txt")
            shutil.copy(dir_path+"/MAGPOX.WFX",dir_path+"/Results/"+str(Sample)+"/wfx"+str(Pressure)+".txt")

            #Processing the Files
            if type=="xtl":
                outread(dir_path+"/"+Sample_Folder,Pressure)
            elif type=="wfx":
                outread_wfx(dir_path+"/"+Sample_Folder,Pressure)
        j=j+1
    remover()
    return (fileo,type)

def plot (run):
    if run[1] == "xtl":
        plot_xtl (run[0])
    elif run[1] == "wfx":
        plot_wfx(run[0])
    else:
        TypeError("Wrong plotting option")

def plot_xtl (file):
    
     fileo=file
     for Sample in fileo.columns:
        Sample_Folder=dir_path+"/Results/"+str(Sample)
        diagram_file= Sample_Folder+"/res.txt"
        diagram_dataframe=pd.read_csv(diagram_file,delimiter="\t")

        pressure=diagram_dataframe.get("pressure").astype(float)*0.1
        forsterite=diagram_dataframe.get("forsterite").astype(float)
        anorthite=diagram_dataframe.get("Xanorthite").astype(float)
        cpx=diagram_dataframe.get("wollastonite-cpx").astype(float)
        opx=diagram_dataframe.get("wollastonite-opx").astype(float)
        pig=diagram_dataframe.get("wollastonite-pig").astype(float)

        fig=plt.figure()
        plot1=fig.subplots()
        plot1.plot(pressure/10,forsterite,"ro",label="Olivine")
        plot1.plot(pressure/10,anorthite,"yo",label="Plagioclase")
        plot1.plot(pressure/10,cpx,"go",label="Cpx")
        plot1.plot(pressure/10,opx,"o",color="purple",label="Opx")
        plot1.plot(pressure/10,pig,"o",label="pig",color="orange")
        plot1.set_ylim(1000,1700)
        plot1.set_xlabel("Pressure (GPa)")
        plot1.set_ylabel("Temperature (°C)")
        plot1.set_title(Sample)
        fig.legend()
        fig.savefig(dir_path+"/Results/"+Sample+".png")
        plt.close(fig)

def plot_wfx (file):
     fileo=file
     for Sample in fileo.columns:
        Sample_Folder=dir_path+"/Results/"+str(Sample)
        diagram_file= Sample_Folder+"/res.txt"
        diagram_dataframe=pd.read_csv(diagram_file,delimiter="\t",na_values="nan")

        pressure=diagram_dataframe.get("pressure").astype(float)*0.1
        forsterite=diagram_dataframe.get("olivine").astype(float)
        anorthite=diagram_dataframe.get("plagioclase").astype(float)
        cpx=diagram_dataframe.get("cpx").astype(float)
        opx=diagram_dataframe.get("opx").astype(float)
        pig=diagram_dataframe.get("pig").astype(float)
        ilm=diagram_dataframe.get("ilm").astype(float)
        sp=diagram_dataframe.get("spinel").astype(float)
        qz=diagram_dataframe.get("qz").astype(float)

        fig=plt.figure()
        plot1=fig.subplots()
        plot1.plot(pressure/10,forsterite,"ro",label="Olivine")
        plot1.plot(pressure/10,anorthite,"yo",label="Plagioclase")
        plot1.plot(pressure/10,cpx,"go",label="Cpx")
        plot1.plot(pressure/10,opx,"o",color="purple",label="Opx")
        plot1.plot(pressure/10,pig,"o",color="orange",label="Pig")
        
        plot1.plot(pressure/10,sp,"o",color="magenta",label="Spinel")
        plot1.plot(pressure/10,qz,"o",color="blue",label="Quartz")
        plot1.plot(pressure/10,ilm,"o",color="grey",label="Ilm")

        plot1.set_ylim(1000,1700)
        plot1.set_xlabel("Pressure (GPa)")
        plot1.set_ylabel("Temperature (°C)")
        plot1.set_title(Sample)
        fig.legend()
        fig.savefig(dir_path+"/Results/"+Sample+"_wfx.png")
        plt.close(fig)
