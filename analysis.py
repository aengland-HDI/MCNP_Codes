###############################################################################
##
##    Goals: Retirve data from all the mesh tallies and plot dy, dz
##              as a function of smoothness
##
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from tabulate import tabulate
import pandas as pd
import pickle

# file = "C:\\Users\\alex.england\\Documents\\Project-3887\\Beam_Profile\\Beam_Profile_4.50_1.50.imsht"
# path = "C:\\Users\\alex.england\\Documents\\Project-3887\\Beam_Profile"
directory = "C:\\Users\\alex.england\\Documents\\Project-3887\\Server_Runs\\Beam_Profile"
X, Y, Z = 102, 26, 28
## initialization variables
dy, dz = [],[]

filename_pattern = re.compile(r'[-+]?\d*\.\d+|\d+')
for filename in os.listdir(directory):
    ## Pull information from filename, index 0 is dy and index 1 is dz
    floats = filename_pattern.findall(filename)
    dy.append(float(floats[0])), dz.append(float(floats[1]))

Delta_Y, min_dy, max_dy = max(dy)-min(dy)-1, min(dy), max(dz)
Delta_Z, min_dz, max_dz = max(dz)-min(dz)-1, min(dz), max(dz)
print(Delta_Y, min_dy, max_dy)
print(Delta_Z, min_dz, max_dz)
cols = Delta_Y+2
rows = Delta_Z+2
print(cols, rows)

# smoothness = pickle.load('smoothness.pickle')
# ratio = pickle.load('ratio.pickle')
# pDiff = pickle.load('pDiff.pickle')

## build an empty matrix of dy by dz
# smoothness = np.zeros((int(rows), int(cols)))
smoothness = np.zeros((int(X),int(rows),int(cols)))
ratio = np.zeros((int(X),int(rows),int(cols)))
pDiff =np.zeros((int(X),int(rows),int(cols)))

flag=0
## iterate over all the files and extract the data
mesh_tallies = {}
kill_flag = 0
for file in os.listdir(directory):
    ## Pull information from filename, index 0 is dy and index 1 is dz
    floats = filename_pattern.findall(file)
    col, row = int(float(floats[0])-min_dy), int(float(floats[1])-min_dz)
    if col < -1 or row < -1:
        print("BADDDDDDDDDD")
    elif col>cols or row>rows:
        print("BADDDDD")
    with open(directory +'\\'+ file, 'r') as file:
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
    #convert values to float
    for i in mesh_names:
        for j in range(0, len(mesh_tallies[i])):
            mesh_tallies[i][j] = [float(dat) for dat in mesh_tallies[i][j]]

        # dimensions of mesh tally

        nx, ny, nz = X, Y, Z
        x, tally_values, unc_values = [0], [], []
        # Need to get all the values for Y
        y,z = mesh_tallies[i][:(Y*Z):Z], mesh_tallies[i][:Z]
        y,z = np.array(y)[:,2], np.array(z)[:,3]
        for i in mesh_tallies[i]:
            if i[1] != x[-1]:
                x.append(i[1])
            tally_values.append(i[4])
            unc_values.append(i[5])
        tally_values = np.array(tally_values).reshape((nx, ny, nz))
        unc_values = np.array(unc_values).reshape((nx, ny, nz))

        ## Calculate the Standard Deviation of the Results as a function of distance
    for i in range(X):
        ## Calculate the Standard Deviation of the Results as a function of distance
        smoothness[i, row, col] = np.std(tally_values[i])
        # print(np.min(tally_values[i]))
        # Calculates the perCent ratio of Max to Min
        ratio[i, row, col] = 100*np.min(tally_values[i])/np.max(tally_values[i])
        ## Calculates the perCent difference
        pDiff[i, row, col] = 100*(np.max(tally_values[i])-np.min(tally_values[i]))/np.max(tally_values[i])
        # print(row, col, smoothness[i, row, col])
        # print(row, col, ratio[i, row, col])
        # print(row, col, pDiff[i, row, col])
        # print("Next")

## pickle extracted data
# pickle.dump(smoothness, 'smoothness.pickle')
# pickle.dump(ratio, 'ratio.pickle')
# pickle.dump(pDiff, 'pDiff.pickle')






# print('The smoothness deltas are dy=%.2f and dz=%.2f'%(min_index[1]+min_dy, min_index[0]+min_dz))
flag = 1E20
mins = []
for i in range(X):
    for j in range(int(rows)):
        for k in range(int(cols)):
            value = smoothness[i,j,k]
            if value<flag and value !=0:
                flag = value
                xxx,yyy,zzz = i,j,k
    mins.append(flag)

## Determine the optimal distance for the source: find the top 5 optimal distances at each x dist


# ratmask=[]
# pDiffmask = []
# for i in np.arange(0, X, 5):
#     mask = np.ma.masked_equal(ratio[i, :, :], 0)
#     mask_idx = np.unravel_index(np.argmax(mask), mask.shape)
#     ratmask.append([x[i], mask_idx[1]+min_dy, mask_idx[0]+min_dz, mask[mask_idx]])

#     mask = np.ma.masked_equal(pDiff[i, :, :], 0)
#     mask_idx = np.unravel_index(np.argmin(mask), mask.shape)
#     pDiffmask.append([x[i], mask_idx[1]+min_dy, mask_idx[0]+min_dz, mask[mask_idx]]) 


# ratio_max = pd.DataFrame(ratmask, columns=['Dist. from Source (cm)', 'Width (cm)', 'Height (cm)', 'Min/Max (%)'])
# pDiff_max = pd.DataFrame(pDiffmask, columns=['Dist. from Source (cm)', 'Width (cm)', 'Height (cm)', 'perCent Difference (%)'])
# # print(tabulate(ratio_max, headers='keys'))
# ratio_max.to_excel("Beam_Ratio.xlsx", index=False), pDiff_max.to_excel('Beam_pDiff.xlsx', index=False)



## Try to plot as a 3D figure with a cut
try:
    os.mkdir("Optimal_Plots\\")
    os.mkdir("Ratio\\")
    os.mkdir("pDiff\\")
except OSError as error:
    print(error)

for i in np.arange(0, X, 10):
#     # plt.figure()
#     # mask = np.ma.masked_equal(smoothness[i, :, :], 0)
#     # im = plt.imshow(mask, origin='lower')
#     # plt.yticks(np.arange(min_dz, max_dz, 4))
#     # plt.xticks(np.arange(0, cols, 5),[str(i+min_dy) for i in np.arange(0, cols, 5)])
#     # plt.title('Beam Smoothness at %.2f cm from Sources'%(x[i]))
#     # plt.ylabel("Increasing Height between Sources")
#     # plt.xlabel("Increasing Space between Center of Sources")
#     # plt.colorbar(im, label="Std. Deviation (mrem/hr)")
#     # plt.savefig("STD\\"+ "Beam_Smoothness_%.2fcm_STD.jpeg"%x[i])
#     # plt.show()

    plt.figure()
    mask = np.ma.masked_equal(ratio[i, :, :], 0)
    im = plt.imshow(mask, origin='lower')
    plt.yticks(np.arange(min_dz, max_dz, 4))
    plt.xticks(np.arange(0, cols, 5))
    plt.title('Beam Smoothness at %.2f cm from Sources'%(x[i]))
    plt.ylabel("Increasing Height between Sources")
    plt.xlabel("Increasing Space between Center of Sources")
    plt.colorbar(im, label="perCent Ratio of (%)")
    plt.savefig("Ratio\\"+ "Beam_Smoothness_%.2fcm_ratio.jpeg"%x[i])
    plt.close()

    plt.figure()
    mask = np.ma.masked_equal(pDiff[i, :, :], 0)
    im = plt.imshow(mask, origin='lower')
    plt.yticks(np.arange(min_dz, max_dz, 4))
    plt.xticks(np.arange(0, cols, 5))
    plt.title('Beam Smoothness at %.2f cm from Sources'%(x[i]))
    plt.ylabel("Increasing Height between Sources")
    plt.xlabel("Increasing Space between Center of Sources")
    plt.colorbar(im, label="perCent Difference (%)")
    plt.savefig("pDiff\\"+ "Beam_Smoothness_%.2fcm_pDiff.jpeg"%x[i])
    plt.close()

for i in np.arange(0, X, 5):
    plt.figure()
    mask = np.ma.masked_equal(tally_values[i, :, :], 0)
    im = plt.imshow(mask, origin='lower')
    plt.title('Beam Smoothness at %.2f cm from Sources'%(x[i]))
    plt.ylabel("Increasing Height between Sources")
    plt.xlabel("Increasing Space between Center of Sources")
    plt.colorbar(im, label="perCent Ratio of (%)")
    plt.savefig("Optimal_Plots\\"+ "Beam_Smoothness_%.2fcm.jpeg"%x[i])
    plt.close()