#!/usr/bin/python3
"""
    ---SUPERMARINE---
    * Version 0.3b  *
    -----------------
    
    Create a mixer geometry blockMesh dictionary for use in 
    The OpenFOAM toolkits.

    Date:   07-2017
    Author: Gabriel Lemieux (gabriel.lemieux@usherbrooke.ca)

    TARGET : MIXER 
    
    -- LOG YOUR TWEAKS HERE ------------------------------
    Key         Description
    ------------------------------------------------------
    MOD1        Vertex adjustment was added

    ------------------------------------------------------ 
    --> Search the keu to find the modification 
    ------------------------------------------------------

    *Quick Introduction*

    DIVI :          Angular, Radial and Vertical divisions per block
    
    RQUAD :             Radius of each QUADran 
                    This parameter must be a list of at least two elements,
                    The first being the center hole/square section.

    NSEC :          The Number of SECtors to create
                    Must be a multiple of 4 (12,24 and 36 are useful multiple of 4!)

    HLAY :          Height of each LAYers 
                    This parameter must be a list of at least one element

    SHAFT :         Section on which the SHAFT exists
                    This parameter must be a list which as the same number of elements
                    of HLAY

    IMPELLERCUT :   Where to CUT for the IMPELLER
                    This parameter must be a NSEC by NCAR by NHLAY 3d matrix.
                    A 1 in a region means to cut that region for the impeller. 

    SQRRATIO :      The RATIO for the distance between the center SQuaRe region and the 
                    Outer cylinder.
                    Must be larger than 0 and smaller than 1.

"""
import numpy as np 
import sys

#Utility
#Convert degree to radian
toRad = lambda deg: deg*2*np.pi/360 

#Do an rotation of rad around the Z axis
rotz   = lambda vec, rad: np.dot(vec,np.array([
    [np.cos(rad),-np.sin(rad),    0],
    [np.sin(rad), np.cos(rad),    0],
    [          0,           0,    1]
]))

#--------------- SETTINGS --------------------#
## CHANGE THE SETTINGS HERE ##
## NEW-BRUNSWICK 3L REACTOR ##
DIVI        = [   5,  5, 20]
RQUAD       = [ 0.005, 0.01, 0.0350, 0.0615]
NSEC        = 24
HLAY        = [ 0.040, 0.060, 0.090,0.105,0.275]
SHAFT       = [  1, 1, 1,  1,  1]
LVLROT      = [  0, 0, 70, 70, 70, 70]
IMPELLERCUT = np.zeros((NSEC,len(RQUAD),len(HLAY)))
IMPELLERCUT[::(NSEC//3),[0,1],2] = 1
IMPELLERCUT[0:NSEC,0,2] = 1
SQRRATIO = 0.62112

"""
  ____                             __  __            _            
 / ___| _   _ _ __   ___ _ __     |  \/  | __ _ _ __(_)_ __   ___ 
 \___ \| | | | '_ \ / _ \ '__|____| |\/| |/ _` | '__| | '_ \ / _ \
  ___) | |_| | |_) |  __/ | |_____| |  | | (_| | |  | | | | |  __/
 |____/ \__,_| .__/ \___|_|       |_|  |_|\__,_|_|  |_|_| |_|\___|
             |_|                                                  
"""
#------ READ THE DOCUMENTATIONS BEFOR CHANGING THE CODE ---------#

nCad = len(RQUAD)

#-- CYLINDER VERTEX --#
# Create rotation unit vectors
cUnits = np.array([[1,0,0]])
for sector in range(0,NSEC-1):
    cUnits = np.append(cUnits, [rotz(cUnits[sector],toRad(360/NSEC))],axis=0)

# Multiply each units with each radius
# this create the vertex rings
vertex = np.empty([1,3]) #Create a dummy at 0
for radius in RQUAD:
    vertex = np.append(vertex, radius*cUnits,axis=0)

#Remove the dummy
vertex = np.delete(vertex,0,axis=0)

# Add HLAY to each base
# this create the ring layers
temp = vertex
for H in HLAY:
    vertex = np.append(vertex, temp+[0,0,H],axis=0)

#-- CYLINDER HEX --#
# This is the scafold use to link the
# the right points together 
hexSet = np.array([
    0, 1, 1+NSEC, NSEC, 0+NSEC*nCad,
    1+NSEC*nCad,1+NSEC+NSEC*nCad,NSEC+NSEC*nCad
    ])

#The last one is a bit different
hexSetLast = np.array([
    0, 1-NSEC, 1, NSEC, 
    0+NSEC*nCad,1+NSEC*(nCad-1),1+NSEC*nCad,NSEC*(nCad+1)
    ])
hexa = np.array([hexSet])
lastPos=0

# Apply the scafold
for H in range(0,len(HLAY)):
    for cadran in range(0,nCad-1):
        for sector in range(0,NSEC):
            if not (IMPELLERCUT[sector,cadran,H]==1):
                hexa = np.append(hexa,[(hexSet if sector<NSEC-1 else hexSetLast) + sector + cadran*NSEC + H*NSEC*nCad],axis=0)
hexa=np.delete(hexa,0,axis=0)

#-- CENTER VERTEX --#
offset = len(vertex) # Offset of the cylinder and the center
div    = int(NSEC/4) # Number of inner division required

# Generate an inner grid using four equidistant points around
# the cylinder 
for H in range(0,len(HLAY)+1):
    index = H*NSEC*nCad+np.arange(0,NSEC,NSEC/4,dtype=int)
    cvertex =vertex[index]
    r=[SQRRATIO,SQRRATIO,0]

    # Grid creation with rought interpolation
    xs =  np.array([r*cvertex[0] + t*(r*cvertex[1]-r*cvertex[0])/div for t in np.arange(0,div+1,1)])
    ys =  np.array([r*cvertex[0] + t*(r*cvertex[3]-r*cvertex[0])/div for t in np.arange(0,div+1,1)])
    grid = np.concatenate([xs + y + (0 if H==0 else [0,0,HLAY[H-1]]) for y in ys-ys[0]])
    vertex = np.append(vertex,grid,axis=0)

# Will be usefull to link the center vertex with the cylinder
# it return the vertex number using a simple x,y,z coordinate system
cGridId = lambda x,y,z: x+y*(div+1)+z*(div+1)**2+offset

#-- CENTER HEX --#
# Create the hex using the x,y,z coordinate
for H in range(0,len(HLAY)):
    if SHAFT[H]==0:
        for ii in range(0,div):
            for jj in range(0,div):
                bottom = np.array([ cGridId(*p) for p in [[ii,jj,H],[ii,jj+1,H],[ii+1,jj+1,H],[ii+1,jj,H]] ])
                top = np.array([ cGridId(*p) for p in [[ii,jj,H+1],[ii,jj+1,H+1],[ii+1,jj+1,H+1],[ii+1,jj,H+1]] ])
                points = np.append(bottom,top)
                hexa = np.append(hexa,[points],axis=0)

#-- LINK HEX --#
# Create an ordered list of coresponding points to link
# with the outer cylinder
reverse = lambda x:np.dot(x,[[0,1,0],[1,0,0],[0,0,1]])
ordered = [[p,0,0] for p in range(0,div+1)]
ordered = np.append(ordered, reverse(ordered[1:])+[div,0,0],axis=0)
ordered = np.append(ordered, np.flip(reverse(ordered[:-1]),axis=0),axis=0)

# Link the center region to the cylinder
for H in range(0,len(HLAY)):
    if SHAFT[H]==0:
        for sec in range(0,NSEC):
            inOne  = cGridId(*(ordered[sec]+[0,0,H]))
            inTwo  = cGridId(*(ordered[sec+(1 if sec<NSEC-1 else -sec)]+[0,0,H]))
            inThree= cGridId(*(ordered[sec]+[0,0,H+1]))
            inFour = cGridId(*(ordered[sec+(1 if sec<NSEC-1 else -sec)]+[0,0,H+1]))
            outOne = sec+H*NSEC*nCad
            outTwo = outOne+( 1 if sec<NSEC-1 else -sec)
            outThree=sec+(H+1)*NSEC*nCad
            outFour =outThree+( 1 if sec<NSEC-1 else -sec)
            hexa = np.append(hexa,[[inOne,inTwo,outTwo,outOne,inThree,inFour,outFour,outThree]],axis=0)

#-- ADJUSTEMENTS (ROTATION AND COMPANIES) --#
#-- LEVEL ROTATION --#
oCylId=lambda omega,r,z:omega+r*NSEC+z*NSEC*nCad
for kk in range(0,len(HLAY)):
    for jj in range(0,nCad):
        for ii in range(0,NSEC):
            ident = oCylId(ii,jj,kk+1)
            vertex[ident] = rotz(vertex[ident],toRad(LVLROT[kk]))

#-- CYLINDER ARCS --#
# Create a list of arc for the cylinder vertex
nEdges = NSEC*nCad*(len(HLAY)+1)
edges = []
for edge in range(0,nEdges):
    #The last one
    if np.mod(edge,NSEC)==NSEC-1:
        second = edge 
        first = edge - NSEC + 1
        vect = rotz(vertex[first],toRad(-360/(2*NSEC)))
        edges.append([first,second,vect[0],vect[1],vect[2]])
    else:
        first = edge  
        second = edge +1 
        vect = rotz(vertex[first],toRad(360/(2*NSEC)))
        edges.append([first,second,vect[0],vect[1],vect[2]])

#-- VERTICAL SPLINE --#
# This force the vertical lines to pass
# on the outer cylinder instead of behing a straight line
spedge = []
for H in range(0,len(HLAY)):
    for cadran in range(0,nCad):
        for sector in range(0,NSEC):
            first  = sector+cadran*NSEC+H*nCad*NSEC
            second = sector+cadran*NSEC+(H+1)*nCad*NSEC
            unitH = np.array([0,0,1])*(vertex[second]-vertex[first])/DIVI[2]
            fv     = vertex[first]*[1,1,0]
            sv     = vertex[second]*[1,1,0]
            if fv[0]!=sv[0] or fv[1]!=sv[1]:
                unitR  = (np.arccos(np.dot(sv,fv)/(np.linalg.norm(sv)*np.linalg.norm(fv))))/DIVI[2]
                iterp  = [rotz(vertex[first],p*unitR)+p*unitH for p in range(1,DIVI[2])]
                # Filter the edge witch isn't in an hex
                inHex=False
                for h in hexa:
                    if first in h and second in h:
                        inHex=True
                if inHex:
                    spedge.append([first,second,np.array(iterp)])

#-- WALLS PATCH --#
# Sides
wallsPatch = []
scafold = np.array([NSEC*(nCad-1),NSEC*(nCad-1)+1,NSEC*nCad+NSEC*(nCad-1)+1,NSEC*nCad+NSEC*(nCad-1)])
scafoldLast =np.array([NSEC*(nCad-1),1+NSEC*(nCad-1)-NSEC,1+NSEC*nCad+NSEC*(nCad-1)-NSEC,NSEC*nCad+NSEC*(nCad-1)])
for H in range(0,len(HLAY)):
    for sector in range(0,NSEC):
        wallsPatch.append( (scafold if sector<NSEC-1 else scafoldLast) +sector+(H*NSEC*nCad))

#-- SHAFT AND IMPELLER PATCH --#
shaftPatch = []
impelPatch =[]
scafold = np.array([0,1,NSEC*nCad+1,NSEC*nCad])
scafoldLast= np.array([0,1-NSEC,NSEC*nCad+1-NSEC,NSEC*nCad])
impScafolds= [
        np.array([0,NSEC,NSEC+NSEC*nCad,NSEC*nCad]),
        np.array([1,1+NSEC,1+NSEC+NSEC*nCad,1+NSEC*nCad]),
        np.array([0,NSEC,1+NSEC,1]),
        np.array([NSEC+NSEC*nCad,NSEC*nCad,1+NSEC*nCad,1+NSEC+NSEC*nCad]),
        np.array([NSEC,1+NSEC,1+NSEC+NSEC*nCad,NSEC+NSEC*nCad])
    ]

for H in range(0,len(HLAY)):
    for cadran in range(0,nCad):
        for sector in range(0,NSEC):
            if SHAFT[H]==1 and cadran==0 and IMPELLERCUT[sector,cadran,H]==0:
                shaftPatch.append((scafold if sector<NSEC-1 else scafoldLast) + sector + (H*NSEC*nCad))
                CutV = IMPELLERCUT[sector,cadran,H]
                if H < len(HLAY)-1:
                    if CutV!=IMPELLERCUT[sector,cadran,H+1]:
                        if sector<NSEC-1:
                            impelPatch.append(impScafolds[3]+sector+cadran*NSEC+(H*NSEC*nCad))
                        else:
                            adjust = [0,0,NSEC,NSEC];
                            impelPatch.append(impScafolds[3]+sector+cadran*NSEC+(H*NSEC*nCad)-adjust)
                if cadran<nCad-1:
                    if CutV!=IMPELLERCUT[sector,cadran+1,H]:
                        if sector<NSEC-1:
                            impelPatch.append(impScafolds[4]+sector+cadran*NSEC+(H*NSEC*nCad))
                        else:
                            adjust = [0,NSEC,NSEC,0];
                            impelPatch.append(impScafolds[4]+sector+cadran*NSEC+(H*NSEC*nCad)-adjust)
                if sector<NSEC-1:
                    if CutV!=IMPELLERCUT[sector+1,cadran,H]:
                        impelPatch.append(impScafolds[1]+sector+cadran*NSEC+(H*NSEC*nCad))
                elif sector == NSEC-1:
                    if int(CutV) != int(IMPELLERCUT[0,cadran,H]):
                        impelPatch.append(impScafolds[0]+0+cadran*NSEC+(H*NSEC*nCad))


#-- TOP AND BOTTOM PATCH --#
topPatch=[]
bottomPatch=[]
scafold = np.array([0,NSEC,NSEC+1,1])
scafoldLast= np.array([0,NSEC,1,1-NSEC])
for H in [0,len(HLAY)]:
    for cadran in range(0,nCad-1):
        for sector in range(0,NSEC):
            if H==0:
                bottomPatch.append( (scafold if sector<NSEC-1 else scafoldLast) +sector+NSEC*cadran+(H*NSEC*nCad))
            else:
                topPatch.append( (scafold if sector<NSEC-1 else scafoldLast) +sector+NSEC*cadran+(H*NSEC*nCad))

#-- CENTER TOP BOTTOM and IMPELLER/SHAFT --#
scafold = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0]])
for H in range(0,len(HLAY)+1):
    for ii in range(0,div):
        for jj in range(0,div):
            toAdd = [cGridId(*p) for p in (scafold+[ii,jj,H])]
            if (H==0 and SHAFT[0]==0):
                bottomPatch.append(toAdd)
            elif (H==len(HLAY) and SHAFT[len(HLAY)-1]==0):
                topPatch.append(toAdd)
            elif (H!=0) and (H!=len(HLAY)):
                if SHAFT[H-1] != SHAFT[H]:
                    shaftPatch.append(toAdd)

for H in range(0,len(HLAY)+1):
    for sec in range(0,NSEC):
        inOne  = cGridId(*(ordered[sec]+[0,0,H]))
        inTwo  = cGridId(*(ordered[sec+(1 if sec<NSEC-1 else -sec)]+[0,0,H]))
        outOne = sec+H*NSEC*nCad
        outTwo = outOne+( 1 if sec<NSEC-1 else -sec)
        if (H==0 and SHAFT[0]==0):
            bottomPatch.append([inOne,outOne,outTwo,inTwo])
        elif (H==len(HLAY) and SHAFT[len(HLAY)-1]==0):
            topPatch.append([inOne,outOne,outTwo,inTwo])
        elif (H!=0) and (H!=len(HLAY)):
            if SHAFT[H-1] != SHAFT[H]:
                shaftPatch.append([inOne,outOne,outTwo,inTwo])

#PRINT BM
#Header
blockMesh=[
"/*--------------------------------*- C++ -*----------------------------------*\\",
"| =========                 |                                                 |",
"| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |",
"|  \\    /   O peration     | Version:  2.3.0                                 |",
"|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |",
"|    \\/     M anipulation  |                                                 |",
"\*---------------------------------------------------------------------------*/",
"FoamFile",
"{",
"    version     2.0;",
"    format      ascii;",
"    class       dictionary;",
"    object      blockMeshDict;",
"}",
"// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //",
"",
"",
"convertToMeter = 1;"]

#Vertex
vtemp="({:20.10f}  {:20.10f}  {:20.10f})"
blockMesh+=["","vertices","("]
for v in vertex:
    blockMesh.append(vtemp.format(*v))
blockMesh+=[");"]

#Hex
btemp =  " hex ( {} {} {} {} {} {} {} {} )"
divtem = " ( {} {} {} ) ".format(*DIVI)
gradtem = " simpleGrading ( 1 1 1 )"

blockMesh+=[" ","blocks","("]
for h in hexa:
    out = btemp.format(*h)+divtem+gradtem
    blockMesh.append(out)

blockMesh+=[");"]
#Edge
arctem=" arc {} {} ( {} {} {} )"

blockMesh+=["","edges","("]
#arc
for b in edges:
    blockMesh.append(arctem.format(*b) )

#spline
splinetem = " spline {} {} ("
for b in spedge:
    blockMesh.append(splinetem.format(b[0],b[1]))
    for v in b[2]:
        blockMesh.append("    "+vtemp.format(*v))
    blockMesh+=["  )"]

blockMesh+=[");"]

#Patch
ftem=" ({} {} {} {})"
blockMesh+=["","boundary","("]
blockMesh+=["walls","{","type wall;","faces","("]
for w in wallsPatch:
    blockMesh.append(ftem.format(*w))
blockMesh+=[");","}"]

blockMesh+=["top","{","type wall;","faces","("]
for w in topPatch:
    blockMesh.append(ftem.format(*w))
blockMesh+=[");","}"]

blockMesh+=["bottom","{","type wall;","faces","("]
for w in bottomPatch:
    blockMesh.append(ftem.format(*w))
blockMesh+=[");","}"]

blockMesh+=["shaft","{","type wall;","faces","("]
for w in shaftPatch:
    blockMesh.append(ftem.format(*w))
blockMesh+=[");","}"]

blockMesh+=["impeller","{","type wall;","faces","("]
for w in impelPatch:
    blockMesh.append(ftem.format(*w))
blockMesh+=[");","}"]

blockMesh+=[");"]

#Print Out
bmDict = open('./constant/polyMesh/blockMeshDict','w')
for line in blockMesh:
    bmDict.write(line+'\n')
