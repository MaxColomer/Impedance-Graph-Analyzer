import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog
import pandas as pd
import matplotlib.figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

window=tk.Tk()
window.title("Impedance Graph Analyzer")

yList = [y/2 for y in range(21)] #lists for x-y axis ticks
xComb = [x for x in range(14)]
yComb = [y/2 for y in range(11)]
def browseFiles(): #prompts user to select CSV files to analyze
    global fileList
    global folderName
    fileList = filedialog.askopenfilenames(initialdir = r"C:\Users\maxwe\Downloads", title = "Select your CSV files", filetypes = [("CSV Files","*.csv")])
    browseLbl.config(text="CSV Files Selected")
    folderName, a, b = fileList[0].rpartition("/") 


def browseMoreFiles(): #prompts user to select NPZ files to analyze
    global npzList
    npzList = filedialog.askopenfilenames(initialdir = r"C:\Users\maxwe\Downloads", title = "Select your NPZ files", filetypes = [("NPZ files", "*.npz")])
    npzLbl.config(text="NPZ Files Selected")


def removenan(regions,impedancemod, impedance): #removes Not A Number values from CSV files
    i=0
    for value in impedance:
        if value == 'nan':
            i=1+i
        else:
            regions.append(i)
            impedancemod.append(float(value))
            i=1+i



def analyze(): #main analysis script
    resultFolder = fileList[0].split("_")[0] + "_CombinedGraphs"
    if not os.path.exists(resultFolder):
        os.mkdir(resultFolder) #make an output folder for figures
    ax.clear()
    ax2.clear()
    ax3.clear()
    i=0
    for file in fileList: 
        #read data from CSV files to be plotted
        regions = [x for x in range(28)]
        df = pd.read_csv(file)
        column_names = df.columns.tolist()
        column_dict = {col:df[col].tolist() for col in column_names}

        topLarge = column_dict[" topLargeRegion"][:-1]
        Z_earTop = float(column_dict[" topLargeRegion"][-1])
        legendLabel=file.split("_")[-2]
        #clean up data removing NAN values
        tLmod=[]
        tLRmod=[]
        removenan(tLRmod,tLmod,topLarge)
        tSmod=[]
        tSRmod=[]
        removenan(tSRmod, tSmod, column_dict[" topSmallRegion"])
        tSCmod=[]
        tSCRmod=[]
        removenan(tSCRmod,tSCmod, column_dict[" smallRegionCombinedTop "])

        colors = plt.cm.tab10(np.linspace(0, 1, len(fileList)))
        #plot the data with distinct colors for each run
        ax.plot(tLRmod,tLmod,label=f"{legendLabel}", color=colors[i])
        ax.plot(i,Z_earTop,'o', color=colors[i])
        ax.set_xlabel("Module Regions")
        ax.set_ylabel("Thermal Impedance (Z)")
        ax.set_xticks(regions)
        ax.set_yticks(yList)
        ax.set_title("Top Large Regions")
        ax.grid(True)
        canvas.draw()
        fig.savefig(resultFolder + "/Top_Large_Regions")

        ax2.plot(tSRmod,tSmod,label=f"{legendLabel}", color=colors[i])
        ax2.set_xlabel("Module Regions")
        ax2.set_ylabel("Thermal Impedance (Z)")
        ax2.set_xticks(regions)
        ax2.set_yticks(yList)
        ax2.set_title("Top Small Regions")
        ax2.grid(True)
        canvas2.draw()
        fig2.savefig(resultFolder + "\\Top_Small_Regions")

        ax3.plot(tSCRmod,tSCmod,label=f"{legendLabel}", color=colors[i])
        ax3.set_xlabel("Module Regions")
        ax3.set_ylabel("Thermal Impedance (Z)")
        ax3.set_xticks(xComb)
        ax3.set_yticks(yComb)
        ax3.set_title("Top Small Regions Combined")
        ax3.grid(True)
        canvas3.draw()
        fig3.savefig(resultFolder + "\\Top_Small_Regions_Combined")
        i=i+1

    ax.legend(loc="lower right")
    canvas.draw()
    ax2.legend(loc="lower right")
    canvas2.draw()
    ax3.legend(loc="lower right")
    canvas3.draw()
    i=0
    a=1
    for file in npzList:
        #read data from NPZ files to be shown on table
        legendLabel=file.split("_")[-1].split(".")[0]
        allFiles = np.load(file)
        thermalData = np.transpose(allFiles['thermo_data'])
        set_temp=thermalData[0][0]
        chiller_temp = round(np.average(thermalData[1]),2)
        t_In = round(np.average(thermalData[2]),2)
        t_Out = round(np.average(thermalData[3]),2)
        ambient = round(np.average(thermalData[4]),2)
        boxTemp = round(np.average(thermalData[5]),2)
        #display NPZ data on table
        imageNumLbl = tk.Label(master=tableFrame, text=f"{legendLabel}",font=("Times New Roman",12))
        imageNumLbl.grid(row=a,column=0,pady=2.5)
        setTempLbl = tk.Label(master=tableFrame, text=f"{set_temp}",font=("Times New Roman",12))
        setTempLbl.grid(row=a,column=1,pady=2.5)
        chillTempLbl = tk.Label(master=tableFrame, text=f"{chiller_temp}",font=("Times New Roman",12))
        chillTempLbl.grid(row=a,column=2,pady=2.5)
        tInLbl = tk.Label(master=tableFrame, text=f"{t_In}",font=("Times New Roman",12))
        tInLbl.grid(row=a,column=3,pady=2.5)
        tOutLbl = tk.Label(master=tableFrame, text=f"{t_Out}",font=("Times New Roman",12))
        tOutLbl.grid(row=a,column=4,pady=2.5)
        ambientLbl = tk.Label(master=tableFrame, text=f"{ambient}",font=("Times New Roman",12))
        ambientLbl.grid(row=a,column=5,pady=2.5)
        boxTempLbl = tk.Label(master=tableFrame, text=f"{boxTemp}",font=("Times New Roman",12))
        boxTempLbl.grid(row=a,column=6,pady=2.5)
        a=a+1

################## Tkinter Formatting Stuff ##############################
fileFrame = tk.Frame(master=window)
fileFrame.pack()

browseBtn = tk.Button(master=fileFrame, text="Select CSV Files", command=browseFiles,bg="#70bdfd")
browseLbl = tk.Label(master=fileFrame, text="No files selected")
browseBtn.grid(row=0,column=0)
browseLbl.grid(row=0,column=1)

npzBtn = tk.Button(master=fileFrame, text="Select NPZ Files", command=browseMoreFiles, bg="#a165e0")
npzLbl = tk.Label(master=fileFrame, text="No files selected")
npzBtn.grid(row=0,column=2)
npzLbl.grid(row=0,column=3)
analyzeBtn = tk.Button(master=fileFrame, text="Run Analysis", command=analyze, bg="#57f042")
analyzeBtn.grid(row=0,column=4)


graphFrame = tk.Frame(master=window)
graphFrame.pack()

fig = matplotlib.figure.Figure(figsize=(8.5,6))
ax = fig.add_subplot()
canvas = FigureCanvasTkAgg(fig, master=graphFrame)
canvas.get_tk_widget().grid(row=0,column=0,padx=10)
toolbar = NavigationToolbar2Tk(canvas, graphFrame, pack_toolbar = False)
toolbar.update()
toolbar.grid(row=1,column=0,sticky="n")

fig2 = matplotlib.figure.Figure(figsize=(8.5,6))
ax2 = fig2.add_subplot()
canvas2 = FigureCanvasTkAgg(fig2, master=graphFrame)
canvas2.get_tk_widget().grid(row=0,column=1,padx=10)
#toolbar2 = NavigationToolbar2Tk(canvas2, graphFrame, pack_toolbar = False)
#toolbar2.update()
#toolbar2.grid(row=1,column=1)

fig3 = matplotlib.figure.Figure(figsize=(7,3))
ax3 = fig3.add_subplot()
canvas3 = FigureCanvasTkAgg(fig3, master=graphFrame)
canvas3.get_tk_widget().grid(row=2,column=0,padx=10,sticky="n")
#toolbar3 = NavigationToolbar2Tk(canvas3, graphFrame, pack_toolbar = False)
#toolbar3.update()
#toolbar3.grid(row=3,column=0)

tableFrame = tk.Frame(master=graphFrame)
tableFrame.grid(row=2,column=1, sticky="n")

imgLbl = tk.Label(master=tableFrame, text="Image #",font=("Times New Roman",18))
imgLbl.grid(row=0,column=0,padx=7.5)
setTLbl = tk.Label(master=tableFrame, text="Set T",font=("Times New Roman",18))
setTLbl.grid(row=0,column=1,padx=7.5)
chilTLbl = tk.Label(master=tableFrame, text="Chiller T",font=("Times New Roman",18))
chilTLbl.grid(row=0,column=2,padx=7.5)
TInLbl = tk.Label(master=tableFrame, text="T In",font=("Times New Roman",18))
TInLbl.grid(row=0,column=3,padx=7.5)
TOutLbl = tk.Label(master=tableFrame, text="T Out",font=("Times New Roman",18))
TOutLbl.grid(row=0,column=4,padx=7.5)
AmbientLbl = tk.Label(master=tableFrame, text="Ambient",font=("Times New Roman",18))
AmbientLbl.grid(row=0,column=5,padx=7.5)
BoxT = tk.Label(master=tableFrame,text="Box T",font=("Times New Roman",18))
BoxT.grid(row=0,column=6,padx=7.5)


window.mainloop()
