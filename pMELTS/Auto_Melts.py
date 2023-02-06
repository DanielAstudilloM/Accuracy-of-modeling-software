import numpy as np
import shutil
import os
import time
import subprocess
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import psutil
import time

import pathlib

dir_path = pathlib.Path(__file__).parent.as_posix() 

def plotter(file,folder):
    File_array=np.loadtxt(dir_path+"/"+file,delimiter="\t",dtype="str")
    colors=["b","g","r","c","m","y","k","w"]
    labels=["Olivine","Opx","Cpx","Garnet","Spinel","Plg"]
    for v in File_array[0,1:]:
        direct=folder+"/"+str(v)
        Result_array=np.loadtxt(direct+"/res.txt",delimiter="\t",dtype="str")
        plote = Figure(figsize=(6,6))
        ax=plote.add_subplot()
        # ax.set_ylim(1000,1500)
        # ax.set_xlim(0,15)
        colorcount=0
        for g in range(len(Result_array[0,1:])):
            Pressure=Result_array[1:,0].astype(float)
            Pressure=Pressure.tolist()
            temperatures=Result_array[1:,g+1].astype(float)
            temperatures=temperatures.tolist()
            l=(i for i,p in enumerate(temperatures) if p==0)
            l=list(l)
            count=0
            for r in l:
                temperatures.pop(r-count)
                Pressure.pop(r-count)
                count=count+1
            print(Pressure,temperatures)

            x=Pressure
            y=temperatures
            
            
            ax.plot(x, y, colors[colorcount]+"o",label=labels[colorcount])
            ax.plot(x,y,"black")
            ax.set_ylabel("Temperature °C")
            ax.set_xlabel("Pressure (GPa)")
            colorcount=colorcount+1
        plote.legend()
        plote.suptitle(v)
        plote.savefig(folder+"/"+str(v)+".png",bbox_inches="tight")

def resser (file,Pressure,r,savefolder="Results"):
    """Creates the res.txt file that is read for plotting the results. It finds the the temperature of appearance of each
        mineral at each pressure and puts it on a tab delimited file."""

    fileo=np.loadtxt(dir_path+"/"+file,delimiter="\t",dtype="str")
    for d in fileo[0,1:]:
        inp = savefolder+"/"+str(d)+"/"
        l = 0
        plotmat = [0,0,0,0,0,0,0]
        acpx=[]
        aopx=[]
        aol=[]
        aspi=[]
        agar=[]
        pres=[]
        afeld=[]
        for v in range(Pressure[0],Pressure[1],r):
            pres.append(v/1000)
            # Append Clinopyroxene results
            cpx=inp+"clinopyroxene"+str(v)+".tbl"
            if os.path.exists(cpx):
                a=np.loadtxt (cpx,delimiter=",",dtype="str")
                acpx.append(a[1,1])
            else:
                acpx.append(0)
            # Append Orthopyroxene results
            opx=inp+"orthopyroxene"+str(v)+".tbl"
            if os.path.exists(opx):
                a=np.loadtxt (opx,delimiter=",",dtype="str")
                aopx.append(a[1,1])
            else:
                aopx.append(0)
            # Append Olivine results
            ol=inp+"olivine"+str(v)+".tbl"
            if os.path.exists(ol):
                a=np.loadtxt (ol,delimiter=",",dtype="str")
                aol.append(a[1,1])
            else:
                aol.append(0)
            # Append garnet results
            gar=inp+"garnet"+str(v)+".tbl"
            if os.path.exists(gar):
                a=np.loadtxt (gar,delimiter=",",dtype="str")
                agar.append(a[1,1])
            else:
                agar.append(0)
            # Append spinel results
            spi=inp+"spinel"+str(v)+".tbl"
            if os.path.exists(spi):
                a=np.loadtxt (spi,delimiter=",",dtype="str")
                aspi.append(a[1,1])
            else:
                aspi.append(0)
            # Append Feldspar results
            feld=inp+"feldspar"+str(v)+".tbl"
            if os.path.exists(feld):
                a=np.loadtxt (feld,delimiter=",",dtype="str")
                afeld.append(a[1,1])
            else:
                afeld.append(0)
            l=l+1
        # Construct data matrix
        plotmat[3]=acpx
        plotmat[1]=aol
        plotmat[2]=aopx
        plotmat[0]=pres
        plotmat[4]=agar
        plotmat[5]=aspi
        plotmat[6]=afeld

        # File writing
        outfile=open(inp+"res.txt","w")
        outfile.write("P\tOl\tOpx\tCpx\tGar\tSpi\tFeld"+"\n")
        outfile.close()
        for x in range (len(pres)):
            for y in range (7):
                if y!= 6:
                    outfile=open(inp+"res.txt","a")
                    outfile.write(str(plotmat[y][x])+"\t")
                    outfile.close()
                if y== 6:
                    outfile=open(inp+"res.txt","a")
                    outfile.write(str(plotmat[y][x]))
                    outfile.close()
            outfile=open(inp+"res.txt","a")
            outfile.write("\n")
            outfile.close()

def input(g,file):
    """Reads the input file and creates a matrix with all of the components"""
    mat=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    fileo=np.loadtxt(file,dtype='str',delimiter="\t",unpack=False)
    n=0
    for c in fileo[:,0]:
        fr=fileo[n,g]
        if c in["SiO2","sio2"]:
            if float(fr) in[0,0.0,0.00]:
                mat[0]=0.0001
            else:
                mat[0]=float(fileo[n,g])
        if c in["TiO2","tio2"]:
            if float(fr) in[0,0.0,0.00]:
                mat[1]=0.0001
            else:
                mat[1]=float(fileo[n,g])
        if c in["Al2O3","al2o3"]:
            if float(fr) in[0,0.0,0.00]:
                mat[2]=0.0001
            else:
                mat[2]=float(fileo[n,g])
        if c in["Cr2O3","cr2o3"]:
            if float(fr) in[0,0.0,0.00]:
                mat[3]=0.0001
            else:
                mat[3]=float(fileo[n,g])
        if c in["FeO","feo"]:
            if float(fr) in[0,0.0,0.00]:
                mat[4]=0.0001
            else:
                mat[4]=float(fileo[n,g])
        if c in["MgO","mgo"]:
            if float(fr) in[0,0.0,0.00]:
                mat[5]=0.0001
            else:
                mat[5]=float(fileo[n,g])
        if c in["MnO","mno"]:
            if float(fr) in[0,0.0,0.00]:
                mat[6]=0.0001
            else:
                mat[6]=float(fileo[n,g])
        if c in["CaO","cao"]:
            if float(fr) in[0,0.0,0.00]:
                mat[7]=0.0001
            else:
                mat[7]=float(fileo[n,g])
        if c in["K2O","k20"]:
            if float(fr) in[0,0.0,0.00]:
                mat[8]=0.0001
            else:
                mat[8]=float(fileo[n,g])
        if c in["Na2O","na2o"]:
            if float(fr) in[0,0.0,0.00]:
                mat[9]=0.0001
            else:
                mat[9]=float(fileo[n,g])
            #Fe2O3
        if c in["fO2","FO2"]:
            mat[14]=str(fileo[n,g]).lower()
        mat[10]=0.0001
        mat[11]=0.0001
        mat[12]=0.0001
        mat[13]=0.0001

        n=n+1
    return (mat)

def remover():
    """Removes tbl files for all phases"""

    file_list = ["melts.out","olivine.tbl","clinopyroxene.tbl","orthopyroxene.tbl","spinel.tbl","melts-liquid.tbl",
                "rhm-oxide.tbl","feldspar.tbl","garnet.tbl","leucite-ss.tbl","sphene.tbl","quartz.tbl","aenigmatite.tbl",
                "filen-out.xml","whitlockite.tbl","alloy-solid.tbl","kalsilite-ss.tbl","nepheline-ss.tbl","ortho-oxide.tbl",
                "rutile.tbl"]

    for file in file_list:
        if os.path.exists(dir_path+"/"+file):
            os.remove(dir_path+"/"+file)

def mover(e,v):
    """Moves all tbl files for all phases into the results folder"""

    file_list = ["olivine","clinopyroxene","orthopyroxene","spinel","melts-liquid",
                "rhm-oxide","feldspar","garnet","leucite-ss","sphene","quartz","aenigmatite",
                "filen-out","whitlockite","alloy-solid","kalsilite-ss","nepheline-ss","ortho-oxide",
                "rutile"]
                
    if os.path.exists(dir_path+"/melts.out"):
        shutil.copy(dir_path+"/melts.out",str(e)+"/melts"+str(v)+".out")
    if os.path.exists(dir_path+"/filen-out.xml"):
        shutil.copy(dir_path+"/filen-out.xml",str(e)+"/filen-out"+str(v)+".xml")

    for file in file_list:

        if os.path.exists(dir_path+"/"+file+".tbl"):
            shutil.copy(dir_path+"/"+file+".tbl",str(e)+"/"+file+str(v)+".tbl")
    
def AutoMelts(File,Pressure,Temp,r,savefolder="Results"):
    """Writes the xml file required by the MELTSbatch file and then runs the automated process"""
    # print(File)
    fileo=np.loadtxt(File,dtype='str',delimiter="\t",unpack=False)
    if os.path.exists(dir_path+"/"+savefolder):
        shutil.rmtree(dir_path+"/"+savefolder)
    j=1
    os.mkdir(dir_path+"/"+savefolder)
    for d in fileo[0,1:]:
        os.mkdir(dir_path+"/"+savefolder+"/"+str(d))
        e=dir_path+"/"+savefolder+"/"+str(d)
        for v in range(Pressure[0],Pressure[1],r):
            remover()
            comp= input(j,File)
            sio=comp[0]
            tio=comp[1]
            alo=comp[2]
            f3=comp[10]
            cro=comp[3]
            feo=comp[4]
            mno=comp[6]
            mgo=comp[5]
            nio=comp[11]
            coo=comp[12]
            cao=comp[7]
            ko=comp[8]
            nao=comp[9]
            po=comp[13]
            fo2=comp[14]
            #modifiers
            ho=0
            t1=Temp[0]
            t2=Temp[1]
            dt=10
            p1=v
            p2=v
            fug=fo2
            off="0"
            a="""<MELTSinput>
                <initialize>
                    <SiO2>"""+str(sio)+"""</SiO2>
                    <TiO2>"""+str(tio)+"""</TiO2>
                    <Al2O3>"""+str(alo)+"""</Al2O3>
                    <Fe2O3>"""+str(f3)+"""</Fe2O3>
                    <Cr2O3>"""+str(cro)+"""</Cr2O3>
                    <FeO>"""+str(feo)+"""</FeO>
                    <MnO>"""+str(mno)+"""</MnO>
                    <MgO>"""+str(mgo)+"""</MgO>
                    <NiO>"""+str(nio)+"""</NiO>
                    <CoO>"""+str(coo)+"""</CoO>
                    <CaO>"""+str(cao)+"""</CaO>
                    <Na2O>"""+str(nao)+"""</Na2O>
                    <K2O>"""+str(ko)+"""</K2O>
                    <P2O5>"""+str(po)+"""</P2O5>
                    <H2O>"""+str(ho)+"""</H2O>
                </initialize>
                <calculationMode>equilibrate</calculationMode>
                <title>asd</title>
                <constraints>
                    <setTP>
                        <initialT>"""+str(t1)+"""</initialT>
                        <finalT>"""+str(t2)+"""</finalT>
                        <incT>"""+str(dt)+"""</incT>
                        <initialP>"""+str(p1)+"""</initialP>
                        <finalP>"""+str(p2)+"""</finalP>
                        <fo2Path>"""+str(fug)+"""</fo2Path>
                        <fo2Offset>"""+str(off)+"""</fo2Offset>
                    </setTP>
                </constraints>
            </MELTSinput>"""

            filen=open(dir_path+"/filen.xml","w")
            filen.write(a)
            filen.close()
            p = subprocess.Popen('wsl cd /mnt/'+dir_path.replace(":","")+'; ./Melts-batch filen.xml',shell=True)
            for _ in range(15):
                if p.poll() is not None:
                    break
                time.sleep(1)
            else:
                p = psutil.Process(p.pid)
                for child in p.children(recursive=True): 
                    child.kill()
                p.kill()
            p.wait(timeout=15)
            
            mover(e,v)
        j=j+1


def runner (File, initial_P, final_P, initial_T, final_T, resolution,Folder="results"):
    
    AutoMelts(dir_path+"/"+File, [initial_P,final_P], [initial_T,final_T],resolution,savefolder=Folder)
    remover()
    resser(File,[initial_P,final_P],resolution,savefolder=dir_path+Folder)
    plotter(File,dir_path+Folder)
 
# Composition file name, initial pressure, final pressure, initial temperature, final temperature, resolution (pressure range),
# and folder to save resulting files to.

runner("compositions.txt",0,10000,1700,1100,1000,Folder="compositions")
