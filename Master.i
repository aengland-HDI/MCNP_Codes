Master Input for Beam Profile
c -------------------------------------------------------------------
c
c   x axis is the beam line
c   y axis is beam width
c   z axis is height
c   center is middle point of source capsules
c
c -------------------------------------------------------------------
c
c                       Cell Cards
c
c -------------------------------------------------------------------
c       Tally Cells
1 1 -0.001205 -99
c
c       Source  and Rod Assemblies
101 7 -8.86 -10:-11:-12:-13                $ Sources
102 5 -8.0  (-14 10):(-15 11):(-16 12):(-17 13) $ Cladding surrounding Source
103 5 -8.0  -18:-19                            $ Spacers
104 5 -8.0  (-22 20 24):(-23 21 25)                   $ Source Rods
105 17 -19.28 -24:-25:-26:-27                $ Tungsten
106 5 -8.0 (-30 28 26):(-31 29 27)           $ Steel Rods
c
200 5 -8.0 (-81 80 30 31)     $ Steel Liner
201 14 -11.35 -82 81 30 31          $ Lead Shield
c
9999    0    99      $ Void Region 

c -------------------------------------------------------------------
c
c                       Surface Cards
c
c -------------------------------------------------------------------
c
c Source 
c 
10   RCC 0 -4.45 2.959 0 0 2.972 0.991       $ Source Volume 1
11   RCC 0 4.45 2.959 0 0 2.972 0.9906       $ Source Volume 2
12   RCC 0 -4.45 -2.959 0 0 -2.972 0.9906    $ Source Volume 3
13   RCC 0 4.45 -2.959 0 0 -2.972 0.9906     $ Source Volume 4
c
c Source Cladding
c
14   RCC 0 -4.45 2.807 0 0 3.680 1.173       $ Cladding
15   RCC 0 4.45 2.807 0 0 3.680 1.173        $ Cladding
16   RCC 0 -4.45 -2.403 0 0 -3.680 1.173     $ Cladding
17   RCC 0 4.45 -2.403 0 0 -3.680 1.173      $ Cladding
c
c Source Spacers
c
18   RCC 0 -4.45 -2.6047 0 0 5.2095 1.1734
19   RCC 0 4.45 -2.6047 0 0 5.2095 1.1734
c
c Source Rod
c
20   RCC 0 -4.45 -7.1539 0 0 13.4391 1.186
21   RCC 0 -4.45 -7.3063 0 0 13.7439 1.339
22   RCC 0 4.45 -7.1539 0 0 13.4391 1.186
23   RCC 0 4.45 -7.3063 0 0 13.7439 1.3389
c
c Source Tubes and Assembly
c
24   RCC 0 -4.45 6.4376 0 0 30 1.829
25   RCC 0 4.45 6.4376 0 0 30 1.829
26   RCC 0 -4.45 -19 0 0 68 1.918
27   RCC 0 4.45 -19 0 0 68 1.918
28   RCC 0 -4.45 -20  0 0 70 2.223
29   RCC 0 4.45 -20 0 0 70 2.223
c
c
99  RPP -100 200 -100 100 -100 100

c -------------------------------------------------------------------
c
c                       Data Cards
c
c -------------------------------------------------------------------
c
MODE P
NPS 3E8
PRINT 10 60 110
PRDMP J 5e7 0 1
RAND 97008386995783
c
IMP:P 1 8R 0
c
c
c Materials
c --------------------------------------------------
m1     $ =Dry Air= with 0.001205 g/cc 
     6000        -0.000124     $ Nat-C
     7014        -0.7555268    $ Nat-N 
     8016        -0.231781     $ Nat-O
     18000       -0.012827     $ Nat-Ar 
m4    $ =Steel= with 7.820000 g/cc 
      6000       -0.005        $ Nat-C
     26000       -0.995        $ Nat-Fe
c Ref: http://www.pnl.gov/main/publications/
m5    $ =Stainless steel 316= with 8.000000 g/cc 
      6000       -0.000410     $ Nat-C
     14000       -0.005070     $ Nat-Si
     15031       -0.000230     $ Nat-P 
     16000       -0.000150     $ Nat-S
     24000       -0.170000     $ Nat Cr 
     25055       -0.010140     $ Nat-Mn
     26000       -0.669000     $ Nat-Fe
     28000       -0.120000     $ Nat-Ni
     42000       -0.025000     $ Nat-Mo 
c http://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf
m6    $ =Aluminum= with 2.700000 g/cc 
     13027       -1            $ Nat-Al
c Reference: PNNL-15870 Rev. 1, March 2011
m7    $ =Cobalt (Co)= with 8.860000 g/cc 
     27000       -1            $ Nat-Co
c http://www.rsc.org/periodic-table/element/27/cobalt
m12   $ =ANSI Type 04 Ordinary Concrete= with 2.350000 g/cc 
c http://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf
     1001        -0.0055       $ Nat-H
     8016        -0.4983       $ Nat-O
     14000       -0.3157       $ Nat-Si
     13027       -0.0455       $ Nat-Al
     26000       -0.0123        $ Nat-Fe
     20000       -0.0826       $ Nat-Ca
     19000       -0.0192       $ Nat-K
     11023       -0.0170       $ Nat-Na
     12000       -0.0026       $ Nat-Mg
     16000       -0.0013       $ Nat-S
m13 $ =Iron= with 7.874000 g/cc 
c http://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf
     26056       -0.95         $ Fe-56
     26054       -0.05         $ Fe-54      
mt13 fe56.12t
m14 $ =Lead= with 11.350000 g/cc 
c http://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf
     82000       -1.0          $ Nat-Pb
m17 $ W
     74000      1
c
c Source Term
c --------------------------------------------------
SDEF PAR=2
     ERG=D1
     POS=D2
     AXS=0 0 1
     RAD=D3
     EXT=D4
c
c
SI1 L 1.1732  1.3325	$ Cobalt-60 gammas
SP1 D 0.49969 0.50031
c Setting Center of Source Points
SI2 L 0 4.45 4.445  0 -4.45 4.445  0 4.45 -4.445  0 -4.45 -4.445
SP2 0.25 0.25 0.25 0.25		
c
SI3 L 0 0.9906	 $ Isotropic Radial Sampling
SP3 -21 1
c
SI4 L -1.4859 1.4869	$ Isotopic Axial Sampling	
SP4 -21 0
c ------------------------------------------------------------------------
c                   Tallies/Variance Reduction
c ------------------------------------------------------------------------
c F9994:P 1
c FM9994 6.39e+11 $ 23629.9 Ci * 3.7E10 Bq/Ci * 2 photons per disintegration * 3600 sec/hr * 1E-7 mrem/pSv   
c WWG 9994 0 0 $ Last zero means half the avg source weight used for lower window bound
c c
c MESH GEOM=xyz REF=0 0 0 ORIGIN=-100 -100 -100  
c      IMESH = -32 0 103 130 200
c      IINTS = 2 32 50 30 2
c      JMESH = -45 45 100
c      JINTS = 2 100 2
c      KMESH = -45 52 100 
c      KINTS = 2 110 5
c c
c WWP:P 5 3 5 0 -1 J J J
c
FMESH14:p GEOM=XYZ ORIGIN=0 -13.335 -14.605
     imesh=102 iints=102
     jmesh=13.335 jints=26
     kmesh=14.605 kints=28
     OUT=COL
FM14  6.39e+11 $ 23629.9 Ci * 3.7E10 Bq/Ci * 2 photons per disintegration * 3600 sec/hr * 1E-7 mrem/pSv
FC14 FMESH Tally Spanning the Beam Chamber     
c
c Photon Flux-to-Dose Rate Conversion Factors $ [pSv-cm^2]
c Extracted from ICRP 116 Dose Conversion Coefficients
DE0 1.00E-02 1.50E-02 2.00E-02 3.00E-02 4.00E-02 5.00E-02
     6.00E-02 7.00E-02 8.00E-02 1.00E-01 1.50E-01 2.00E-01
     3.00E-01 4.00E-01 5.00E-01 5.11E-01 6.00E-01 6.62E-01
     8.00E-01 1.00E+00 1.12E+00 1.33E+00 1.50E+00 2.00E+00
     3.00E+00 4.00E+00 5.00E+00 6.00E+00 6.13E+00 8.00E+00
     1.00E+01 1.50E+01 2.00E+01 3.00E+01 4.00E+01 5.00E+01
     6.00E+01 8.00E+01 1.00E+02 1.50E+02 2.00E+02 3.00E+02
     4.00E+02 5.00E+02 6.00E+02 8.00E+02 1.00E+03 1.50E+03
     2.00E+03 3.00E+03 4.00E+03 5.00E+03 6.00E+03 8.00E+03
     1.00E+04
DF0 0.0337 0.0664 0.0986 0.1580 0.1990 0.2260 0.2480
     0.2730 0.2970 0.3550 0.5280 0.7210 1.1200 1.5200
     1.9200 1.9600 2.3000 2.5400 3.0400 3.7200 4.1000
     4.7500 5.2400 6.5500 8.8400 10.8000 12.7000 14.4000
     14.6000 17.6000 20.6000 27.7000 34.4000 46.1000 56.0000
     64.4000 71.2000 82.0000 89.7000 102.0000 111.0000 121.0000
     128.0000 133.0000 136.0000 142.0000 145.0000 152.0000 156.0000
     161.0000 165.0000 168.0000 170.0000 172.0000 175.0000