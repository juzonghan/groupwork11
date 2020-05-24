import numpy as np
import matplotlib.pyplot as plt
 
label = []
quant = []

def picture(label,quant):
    width = 0.5
    ind = np.linspace(0,6,4)
    fig = plt.figure(1)    # make a square figure
    ax  = fig.add_subplot(111)
    ax.bar(ind-width/2,quant,width,color='red')    
    ax.set_xticks(ind)    # Set the ticks on x-axis
    ax.set_xticklabels(label)
    ax.set_xlabel('Version')   #This two lines define the label
    ax.set_ylabel('Release time(timestamp)')
    ax.set_title('linux kernel version\'release time', bbox={'facecolor':'1', 'pad':3})   #This is the title.
    plt.grid(True)
    plt.show()
    plt.savefig("result.jpg")
    plt.close()
 
fh = open("time.txt","r").read()
output = eval(fh)
for i in output.keys():
    label.append(i)
    quant.append(output[i])
 
picture(label,quant)