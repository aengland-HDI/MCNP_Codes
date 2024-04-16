import numpy as np
import pandas as pd
from prettytable import PrettyTable 
from tabulate import tabulate
import sys

bash = open('beam_macro.bat', 'w')
b_start = ['@ PATH C:\MCNP62\MCNP_CODE\\bin;%PATH%',
           '@ set DATAPATH=C:\MCNP62\MCNP_DATA', 
           '@ set DISPLAY=localhost: 0',
           'chdir C:\Work\Project-3887-main\Beam_Profile\Inputs \n']
bash.write('\n'.join(b_start))
runs = 0
## Set the distance and y here
for DY in np.arange(4.5, 24.5, 1):
    runs=runs+1
    for DZ in np.arange(1.5, 23.5, 1):
        runs=runs+1
        print(DY, DZ)
        master_file = "C:\\Users\\alex.england\\Documents\\Project-3887\\Beam_Profile\\Master.i"
        filename = 'Beam_Profile_%.2f_%.2f.i' %(DY, DZ)

        if DZ <= 2*0.556:
            # delete the cell and surface card corresponding
            # or throw a error
            print(DZ)
            print("HOUSTON WE HAVE A PROBLEM!!")
            sys.exit('DZ cannot be equal or less than 0')
        if DY <= 2*2.223:
            # delete the cell and surface card corresponding
            # or throw a error
            print(DY,2*2.223 )
            print("HOUSTON WE HAVE A PROBLEM!!")
            sys.exit('DY cannot be equal or less than 0')

        ## Geometry Constants
        Max_Z = 14.605  # cm
        Max_Y = 13.335  # cm
        Source_Height = 2.972
        Cladding_Height = 3.680
        Steel_Bottom = 0.793
        Height_Top = 35.116
        Tungsten_IHeight = 0.876

        Geom_H = Max_Z+10.106
        Geom_W = Max_Y+10.106

        Source_Radius = 0.991
        Cladding_Radius = 1.173
        Inner_Radius_Holder = 1.186
        Outer_Radius_Holder = 1.339
        Tungsten_IRadius = 1.123
        Tungsten_ORadius = 1.829
        Inner_Radius_Rod = 1.918
        Outer_Radius_Rod = 2.223

        Radii = [Source_Radius, Cladding_Radius, Cladding_Radius, Inner_Radius_Holder, Outer_Radius_Holder, Tungsten_IRadius, Tungsten_ORadius, Inner_Radius_Rod, Outer_Radius_Rod]
        Height = [Source_Height, Cladding_Height, DZ-0.556-0.152]

    ######################################################
    ##          Meat and Potatoes of the Code           ##
    ######################################################


        print('Creating New Input File based on the Parameters ...\n Filename:%s \n\n' %(filename))

        Values = pd.DataFrame(columns=['Sources', 'Cladding'])

        # Top/Bottom Source L->R
        Sources = np.array([[0,0,0,0],[0,0,0,0]], dtype=float)

        # Changing the Y-Coordinates 
        Sources[0, [1,3]] = np.add( Sources[0, [1,3]], DY/2)
        Sources[0, [0,2]] = np.subtract( Sources[0, [0, 2]], DY/2)
        # Changing Z Coordinates
        Sources[1, [0,1]] = np.add( Sources[1, [0,1]], DZ/2)
        Sources[1, [2,3]] = np.subtract( Sources[1, [2,3]], DZ/2)
        Values['Sources']=Sources.tolist()



        Cladding = Sources
        # Changing the Y-Coordinates 
        Cladding[0, [1,3]] = Sources[0, [1,3]]
        Cladding[0, [0,2]] = Sources[0, [0,2]]
        # Changing Z Coordinates
        Cladding[1, [0,1]] = np.subtract( Cladding[1, [0,1]],0.152)
        Cladding[1, [2,3]] = np.add(Cladding[1, [2,3]], 0.556)
        Values['Cladding'] = Cladding.tolist()
        print(Values['Cladding'])

        ## Changing Dimensions of Source Holder and adding Spacer

        Spacer = np.array([[Sources[0, 0],Sources[0, 1]], [ Cladding[1, 2], Cladding[1, 2]]])
        Air_Gap_SR = np.array([[Sources[0, 0],Sources[0, 1]], [ Cladding[1, 2]-Cladding_Height-0.0254, Cladding[1, 2]-Cladding_Height-0.0254] ])
        Source_Rod = np.array([[Sources[0, 0],Sources[0, 1]], [ Cladding[1, 2]-Cladding_Height-0.0254-0.793, Cladding[1, 2]-Cladding_Height-0.0254-0.793] ])
        Values['Spacer'] = Spacer.tolist()
        Values['Air_Gap_In'] = Air_Gap_SR.tolist()
        Values['Source_Rod'] = Source_Rod.tolist()

        Height.append((Cladding[1, 0]+Cladding_Height)-(Cladding[1, 2]-Cladding_Height)+0.0254+Tungsten_IHeight)
        Height.append((Cladding[1, 0]+Cladding_Height)-(Cladding[1, 2]-Cladding_Height)+0.0254+0.793+Tungsten_IHeight)

        ## Tungsten Sits directly on top of the sources
        Tungsten_SR = np.array([[Sources[0, 0],Sources[0, 1]],[Cladding[1, 0]+Cladding_Height, Cladding[1, 0]+Cladding_Height]])
        Tungsten = np.array([[Sources[0, 0],Sources[0, 1]],[Cladding[1, 0]+Cladding_Height+Tungsten_IHeight, Cladding[1, 0]+Cladding_Height+Tungsten_IHeight]])
        Values['Tungsten_Inner'] = Tungsten_SR.tolist()
        Values['Tungsten'] = Tungsten.tolist()
        Height.append(Tungsten_IHeight)
        Height.append(Max_Z-Cladding[1, 0]+Cladding_Height+Tungsten_IHeight)

        ## Source RODS PT 2
        Air_Region = np.array([[Sources[0, 0],Sources[0, 1]],[-Geom_H+0.254, -Geom_H+0.254]])
        Source_Rods = np.array([[Sources[0, 0],Sources[0, 1]],[-Geom_H, -Geom_H]])
        Values['Air_Rods'] = Air_Region.tolist()
        Values['Source_Rods_Outer'] = Source_Rods.tolist()

        Height.append(2*Geom_H-2*0.254)
        Height.append(2*Geom_H)

        Source_Points = Sources
        Source_Points[1, [0,1]] = np.add(Source_Points[1, [0,1]], 0.5*Source_Height)
        Source_Points[1, [2,3]] = np.subtract(Source_Points[1, [2,3]], 0.5*Source_Height)


        if Sources[1,0]+Source_Height/2 > Max_Z:
            print("HOUSTON WE HAVE A PROBLEM!!")
            sys.exit('DZ is too much, exceeds Beam Chamber Height, must be less than 23.51cm')

        if Sources[0,1]+Source_Radius > Max_Y:
            print("HOUSTON WE HAVE A PROBLEM!!")
            sys.exit('DY is too much, exceeds Beam Chamber Width, must be less than 24.61cm')

        ## Writing new input file

        new_file = open('Inputs\\'+filename, 'w')
        master = open(master_file, 'r')

        surface_line = "c                       Surface Cards"

        for line in master:
            if line.strip() == surface_line:
                break
            new_file.write(line)
        new_file.write(surface_line + '\nc\nc -------------------------------------------------------------------\n')

        ## Define Source Rods Assembly
        s=10
        k=0
        ## Write Surface Cards
        for name in Values.columns:
            print(name)
            new_file.write("c    %s\nc\n" %name)
            Object = Values[name]
            R = Radii[k]
            dz = Height[k]
            k=k+1
            for i in range(len(Object.loc[0])):
                x = 0.0
                y = Object.iloc[0][i]
                z = Object.iloc[1][i]
                if i == 2:
                    dz = -dz
                SUR = '%d  RCC %.3f %.3f %.3f 0.0 0.0 %.3f %.3f     $ %s\n' %(s,x,y,z,dz,R, name)
                new_file.write(SUR)
                s = s+1

        Rem_Geom = ['c\nc\nc\n80 RPP -2.223 102 -13.335 13.335 -14.605 14.605   $ Inner Beam',
                    '81 RPP -3.121 102.898 -14.233 14.233 -15.503 15.50    $ SS Liner',
                    '82 RPP -10 113 -24.339 24.339 -25.609 25.609 $ Lead\n']
        new_file.write('\n'.join(Rem_Geom))

        new_file.write('c\nc    Void\nc\n99  RPP -15 115 -26 26 -26 26\n\n')
        new_file.write('c -------------------------------------------------------------------\n')
        ## Write Data Cards
        start_line = "c                       Data Cards"
        kill_line = 'c Setting Center of Source Points'
        print_flag = False
        for line in master:
            if line.strip() == start_line:
                print_flag=True
            if line.strip() == kill_line:
                new_file.write(kill_line+'\n')
                print_flag=False
            if print_flag:
                new_file.write(line)

        #Writing Source Locations

        x = 0
        y1, y2, y3, y4 = Source_Points[0,0], Source_Points[0,1], Source_Points[0,2], Source_Points[0,3],
        z1, z2, z3, z4 = Source_Points[1,0], Source_Points[1,1], Source_Points[1,2], Source_Points[1,3],
        line = 'SI2 L %.3f %.3f %.3f  %.3f %.3f %.3f  %.3f %.3f %.3f  %.3f %.3f %.3f\n'%(x, y1, z1, x, y2, z2, x, y3, z3, x, y4, z4)
        new_file.write(line)
        new_file.write('SP2 0.25 0.25 0.25 0.25\n')

        start_line = 'SP2 0.25 0.25 0.25 0.25'
        flag = False
        master = open(master_file, 'r')
        for line in master:
            if flag:
                new_file.write(line)
            if line.strip() == start_line:
                flag=True


        new_file.close()
        master.close()
        bash.write('mcnp6 name=%s tasks 24\n'%(filename))
        bash.write('move %smsht ..\Mesh_Tallies\ \n'%filename)
        y,z=0,0
print(runs)