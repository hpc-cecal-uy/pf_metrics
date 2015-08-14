# Copyright 2015 Renzo Massobrio
# Facultad de Ingenieria, UdelaR

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from math import sqrt

import numpy as np
from hv import HyperVolume

def normalize_front(refFront, approxFront):
    """
    This function normalizes the approximated Pareto front (approxFront)
    in the range [0,1] using the reference Pareto front (refFront).
    """
    minX = refFront[0][0]
    maxX = refFront[0][0]
    minY = refFront[1][0]
    maxY = refFront[1][0]
    
    for i in range(len(refFront[0])):
        if minX > refFront[0][i]:
            minX = refFront[0][i]
        if maxX < refFront[0][i]:
            maxX = refFront[0][i]

        if minY > refFront[1][i]:
            minY = refFront[1][i]
        if maxY < refFront[1][i]:
            maxY = refFront[1][i]

    normApproxFrontX = []
    normApproxFrontY = []

    for i in range(len(approxFront[0])):
        normApproxFrontX.append((approxFront[0][i] - minX) / (maxX - minX))
        normApproxFrontY.append((approxFront[1][i] - minY) / (maxY - minY))

    return (normApproxFrontX, normApproxFrontY)
    
def pareto_frontier(Xs, Ys, maxX = False, maxY = False):
    # Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
    # Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]
    # Loop through the sorted list
    for pair in myList[1:]:
        if maxY:
            if pair[1] >= p_front[-1][1]:
                p_front.append(pair)
        else:
            if pair[1] <= p_front[-1][1]:
                p_front.append(pair)

    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]

    #Borro los elementos repetidos del frente
    copia_pfX=list(p_frontX)
    copia_pfY=list(p_frontY)
    for i,(a,b) in enumerate(zip(copia_pfX[1:],copia_pfY[1:])):
        if (a==copia_pfX[i] and b==copia_pfY[i]):
            p_frontX.remove(a)
            p_frontY.remove(b)   

    return (p_frontX, p_frontY)

def euclidean_distance(x1,y1,x2,y2):
    return (sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)))

def distance_to_front(x,y,PF):
    if (len(PF[0])!=len(PF[1])):
        raise Exception("ERROR: Pareto front must have same X and Y dimensions")
    min_distance= euclidean_distance(x,y,PF[0][0],PF[1][0])
    for i in range(1,len(PF[0])):
        dist=euclidean_distance(x,y,PF[0][i],PF[1][i])
        if (dist<min_distance):
            min_distance=dist
    return min_distance


def generational_distance(X,Y,PF):
    if (len(X)!=len(Y)):
        raise Exception("ERROR: X and Y must have the same length")
    number_of_points=len(X)
    total_distance=0
    for i in range(0,number_of_points):
        total_distance+=distance_to_front(X[i],Y[i],PF)
    return sqrt(total_distance)/float(number_of_points)

def distance_to_closest_neighbor_spacing(x,y,X,Y):
    if (len(X)!=len(Y)):
        raise Exception("ERROR: X and Y must have the same length")
    min_distance=abs(x-X[0])+abs(y-Y[0])
    for i in range(1,len(X)):
        distance=abs(x-X[i])+abs(y-Y[i])
        if (distance<min_distance):
            min_distance=distance
    return min_distance

def spacing (X,Y):
    if (len(X)!=len(Y)):
        raise Exception("ERROR: X and Y must have the same length")

    #XY = sorted([[X[i], Y[i]] for i in range(len(X))], reverse=False)
    XY = [[X[i], Y[i]] for i in range(len(X))]
        
    number_of_points=len(X)
    list_of_distances=[]
    for i in range(0,len(X)):
        list_of_distances.append(distance_to_closest_neighbor_spacing(XY[i][0],XY[i][1], [a[0] for a in XY[:i]+XY[i+1:]], [b[1] for b in XY[:i]+XY[i+1:]]))
        
    average_distance=np.mean(np.array(list_of_distances))
    sum=0
    for d in list_of_distances:
        sum+=((d-average_distance)*(d-average_distance))
    return sqrt(sum/float(number_of_points))

def spread(X,Y,PF):
    if (len(X)!=len(Y)):
        raise Exception("ERROR: X and Y must have the same length")

    XY = sorted([[X[i], Y[i]] for i in range(len(X))], reverse=False)

    number_of_points=len(X)
    list_of_distances=[]
    for i in range(1,len(X)-1):
        list_of_distances.append(euclidean_distance(XY[i][0],XY[i][1],XY[i+1][0],XY[i+1][1]))
    average_distance=np.mean(np.array(list_of_distances))
    suma=0
    for d in list_of_distances:
        suma+=abs(d-average_distance)

    argmin_objective_0=np.argmin(np.array(PF[0]))
    argmin_objective_1=np.argmin(np.array(PF[1]))
    distance_to_pf_extreme_0=euclidean_distance(PF[0][argmin_objective_0], PF[1][argmin_objective_0], XY[0][0],XY[0][1])
    distance_to_pf_extreme_1=euclidean_distance(PF[0][argmin_objective_1], PF[1][argmin_objective_1], XY[-1][0],XY[-1][1])
    spread = (distance_to_pf_extreme_0 + distance_to_pf_extreme_1 + suma)/float(distance_to_pf_extreme_0+distance_to_pf_extreme_1+(number_of_points*average_distance))
    return spread
