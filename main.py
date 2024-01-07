#System Resource Monitor
#By Nick Conn

from tkinter import *
from psutil import disk_partitions,disk_usage,virtual_memory,cpu_percent
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = Tk()
window.geometry("900x900")
window.title("System Resource Monitor by Nick Conn")
window.configure(bg='#161a1d')

cpuCounter = 0
ramCounter = 0
cpuX =[]
cpuY = []
ramX = []
ramY = []



#Function to display the CPU Information
def get_cpu_info():
    cpu_use=cpu_percent(interval=1)
    #print('{} %'.format(cpu_use))
    global cpuCounter
    cpuCounter += 1
    cpuY.append(cpu_use)
    cpuX.append(cpuCounter)
    ct = datetime.datetime.now()
    date_time = ct.strftime("%m/%d/%Y %H:%M:%S")
    cpuFileOutput = date_time + '   CPU USE: ' + str(cpu_use) + '% \n'
    
    with open("systemresourcelog.txt", 'a') as f:
        f.write(cpuFileOutput)

    cpu_label.config(text='{} %'.format(cpu_use))
    cpu_label.after(1000,get_cpu_info)

#Function to convert bytes to GB
def bytes_to_gb(bytes):
    one_gb=1073741824 #num bytes in a gb
    gb=bytes/one_gb
    gb='{0:.1f}'.format(gb)
    return gb

#Function to display the RAM information
def get_ram_info():
    ram_use=virtual_memory()
    #print(ram_use)
    ram_use=dict(ram_use._asdict())
    for key in ram_use:
        if key != 'percent':
            ram_use[key]=bytes_to_gb(ram_use[key])
    #print(ram_use)

    global ramCounter
    ramCounter += 1
    ramY.append(ram_use['percent'])
    ramX.append(ramCounter)

    ct = datetime.datetime.now()
    date_time = ct.strftime("%m/%d/%Y %H:%M:%S")
    ramFileOutput = date_time + '   RAM USE: ' + str(ram_use['percent']) + '% \n'
    
    with open("systemresourcelog.txt", 'a') as f:
        f.write(ramFileOutput)

    ram_label.config(text='{} GB / {} GB ({} %)'.format(ram_use["used"],ram_use["total"],ram_use["percent"]))
    ram_label.after(1000, get_ram_info)

data = disk_partitions(all=False)

#Gets names of disk drives
def get_disk_names():
    return [i.device for i in data]

def details(disk_name):
    for i in data:
        if i.device == disk_name:
            return i
        
def disk_info(disk_name):
    disk_info = {}
    try:
        usage=disk_usage(disk_name)
        disk_info['Disk']=disk_name
        disk_info['Total']=f"{bytes_to_gb(usage.used+usage.free)} GB"
        disk_info['Used']=f"{bytes_to_gb(usage.used)} GB"
        disk_info['Free']=f"{bytes_to_gb(usage.free)} GB"
        disk_info['Percent']=f"{usage.percent} %"
    except PermissionError:
        print("Permission Error while attempting to read disk:", disk_name)
        pass
    except FileNotFoundError:
        pass
    info=details(disk_name)
    disk_info.update({"Disk": info.device})
    return disk_info

def all_disk_info():
    return_all=[]
    for i in get_disk_names():
        return_all.append(disk_info(i))
    return return_all








# MAIN TITLE
title_program = Label(window, text="System Resource Monitor", font="Terminal 40 bold", fg="#e5383b", bg="#161a1d")
title_program.place(x=110, y=20)


# CPU TITLE
cpu_title_label=Label(window, text='CPU Usage: ', font="arial 24 bold", fg='#e5383b', bg="#161a1d")
cpu_title_label.place(x=20, y=155)
# CPU Percentage
cpu_label=Label(window, bg='black', font="arial 30 bold", fg='#e5383b', width=20)
cpu_label.place(x=230, y=150)

#CPU DISPLAY 
get_cpu_info()



fig = plt.Figure(figsize = (7, 2),dpi = 100)
# adding the subplot
plot1 = fig.add_subplot(111)
# plotting the graph
plot1.plot(cpuX, cpuY)
# creating the Tkinter canvas
# containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master = window)  

canvas.draw()
# placing the canvas on the Tkinter window
canvas.get_tk_widget().place(x=120, y=225)


def updateCPU(i):

    plt.cla()
    plot1.plot(cpuX,cpuY)

ani=FuncAnimation(fig=fig,func=updateCPU,interval=200)




# RAM TITLE
ram_title_label=Label(window, text='RAM Usage: ', font="arial 24 bold", fg='#e5383b', bg="#161a1d")
ram_title_label.place(x=20, y=455)
# RAM Percentage
ram_label=Label(window, bg='black', font="arial 30 bold", fg='#e5383b', width=20)
ram_label.place(x=230, y=450)

#RAM DISPLAY
get_ram_info()

fig1 = plt.Figure(figsize = (7, 2),dpi = 100)
# adding the subplot
plot2 = fig1.add_subplot(111)
# plotting the graph
plot2.plot(ramX, ramY)
# creating the Tkinter canvas
# containing the Matplotlib figure
canvas1 = FigureCanvasTkAgg(fig1, master = window)  

canvas1.draw()
# placing the canvas on the Tkinter window
canvas1.get_tk_widget().place(x=120, y=525)

def updateRam(i):

    plt.cla()
    plot2.plot(ramX,ramY)

ani1=FuncAnimation(fig=fig1,func=updateRam,interval=200)


# DISK TITLE
disk_title_label=Label(window, text='Disk Usage: ', font="arial 24 bold", fg='#e5383b', bg="#161a1d")
disk_title_label.place(x=20, y=755)
# DISK Percentage
disk_label=Label(window, bg='black', font="arial 20 bold", fg='#e5383b')
disk_label.place(x=230, y=760)

info=all_disk_info()
info1=info[0]
print(info)
for key in info:
    print(key)

disk_label.config(text='Disk: {} {} free / {} total'.format(info1["Disk"],info1["Free"],info1["Total"]))


window.mainloop()