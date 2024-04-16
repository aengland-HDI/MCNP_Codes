import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

file = "C:\\Users\\alex.england\\Documents\\Project-3887\\Server_Runs\\Beam_Profile\\Beam_Profile_23.50_22.50.imsht"
X, Y, Z = 102, 26, 28
mesh_tallies = {}

with open(file, 'r') as file:
    lines = file.readlines()

    # loop through lines to find tally
    for i,line in enumerate(lines):
        if line.find('Mesh Tally Number') != -1:
            mesh_name = line[25:28]
            mesh_data = []

            for j in range(i+12, len(lines)):
                k=0
                if not lines[j].isspace():
                    tally_data = lines[j].split()
                    mesh_data.append(tally_data)
                else:
                    break
            mesh_tallies[mesh_name] = mesh_data

# Data pulled into dictionary

mesh_names = mesh_tallies.keys()
print(mesh_names)
plott = 0
#convert values to float
for i in mesh_names:
    for j in range(0, len(mesh_tallies[i])):
        mesh_tallies[i][j] = [float(dat) for dat in mesh_tallies[i][j]]

    # dimensions of mesh tally

    nx, ny, nz = X, Y, Z
    x, y, z, tally_values, unc_values = [], [], [], [], []
    x= [0]

    for i in mesh_tallies[i]:
        if i[1] != x[-1]:
                x.append(i[1])
        tally_values.append(i[4])
        unc_values.append(i[5])
    tally_values = np.array(tally_values).reshape((X, Y, Z))
    
    ratio = np.zeros([X,Y,Z])
    perDiff = np.zeros([X,Y,Z])

    for i in range(X):
        ratio[i] = 100*tally_values[i]/np.max(tally_values[i])
        perDiff[i] = 100*(np.max(tally_values[i])-tally_values[i])/np.max(tally_values[i])

for i in np.arange(0, X, 5):
    plt.figure()
    mask = np.ma.masked_equal(ratio[i, :, :], 0)
    im = plt.imshow(mask, origin='lower')
    plt.title('Beam Smoothness at %.2f cm from Sources'%(x[i]))
    plt.ylabel("Increasing Height between Sources")
    plt.xlabel("Increasing Space between Center of Sources")
    plt.colorbar(im, label="perCent Ratio of (%)")
    plt.savefig("Optimal_Plots\\"+ "Beam_Smoothness_%.2fcm_ratio.jpeg"%x[i])
    plt.close()





