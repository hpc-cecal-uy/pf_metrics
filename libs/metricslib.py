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


##############################################################
##############################################################
#INSTRUCTIONS

# Script to plot the global Pareto front and calculate generational distance, spread, spacing and relative hypervolume based on the pareto fronts output from ECJ (http://cs.gmu.edu/~eclab/projects/ecj/).
# USAGE:
# python pf_metrics.py <path_to_results> <number_of_runs> <objective_1_name> <objective_2_name>

# 	To run the example: 
		# python pf_metrics.py example/ 10 Price Coverage

# Notes:
# 	-<path_to_results> is the folder where the files "job.*.front.stat" are located
# 	-<number_of_runs> is the amount of jobs executed. e.g.: if number_of_runs is 4 you should have job.0.front.stat, ..., job.3.front.stat
# 	-<objective_J_name> is the label for the axis corresponding to objective J in the plot

# IMPORTANT: THIS SCRIPT ASSUMES MINIMIZATION OF BOTH OBJECTIVES. YOU SHOULD MODIFY THESE BEHAVIOUR TO FIT YOUR NEEDS.

# The metrics are calculated using the formulas in  "Multiobjective optimization using Evolutionary Algorithms" from Kalyanmoy Deb.
# For the spread calculation, the euclidean distance is used.
# Hypervolumes are calculated using the code of Simon Wessing from TU Dortmund University found at https://ls11-www.cs.uni-dortmund.de/rudolph/hypervolume/start

# Please feel free to contact me at: renzom@fing.edu.uy

##############################################################
##############################################################
#AUXILIARY FUNCTIONS

import numpy as np
from hv import HyperVolume
import sys
from math import sqrt

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
	return p_frontX, p_frontY


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

def distance_to_closest_neighbor_spread(x,y,X,Y):
	if (len(X)!=len(Y)):
		raise Exception("ERROR: X and Y must have the same length")
	min_distance=euclidean_distance(x,y,X[0],Y[0])
	for i in range(1,len(X)):
		distance=euclidean_distance(x,y,X[i],Y[i])
		if (distance<min_distance):
			min_distance=distance
	return min_distance

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
	number_of_points=len(X)
	list_of_distances=[]
	for i in range(0,len(X)):
		list_of_distances.append(distance_to_closest_neighbor_spacing(X[i],Y[i], [a for a in X[:i]+X[i+1:]], [b for b in Y[:i]+Y[i+1:]]))
	average_distance=np.mean(np.array(list_of_distances))
	sum=0
	for d in list_of_distances:
		sum+=((d-average_distance)*(d-average_distance))
	return sqrt(sum/float(number_of_points))


def spread(X,Y,PF):
	if (len(X)!=len(Y)):
		raise Exception("ERROR: X and Y must have the same length")
	number_of_points=len(X)
	list_of_distances=[]
	for i in range(0,len(X)):
		list_of_distances.append(distance_to_closest_neighbor_spread(X[i],Y[i], [a for a in X[:i]+X[i+1:]], [b for b in Y[:i]+Y[i+1:]]))
	average_distance=np.mean(np.array(list_of_distances))
	sum=0
	for d in list_of_distances:
		sum+=abs(d-average_distance)

	argmin_objective_0=np.argmin(np.array(PF[0]))
	argmin_objective_1=np.argmin(np.array(PF[1]))
	distance_to_pf_extreme_0=distance_to_closest_neighbor_spread(PF[0][argmin_objective_0], PF[1][argmin_objective_0], X,Y)
	distance_to_pf_extreme_1=distance_to_closest_neighbor_spread(PF[0][argmin_objective_1], PF[1][argmin_objective_1], X,Y)

	spread = (distance_to_pf_extreme_0 + distance_to_pf_extreme_1 + sum)/float(distance_to_pf_extreme_0+distance_to_pf_extreme_1+(number_of_points*average_distance))
	return spread
