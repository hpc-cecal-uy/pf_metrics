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

#   To run the example: 
        # python pf_metrics.py example/ 10 Price Coverage

# Notes:
#   -<path_to_results> is the folder where the files "job.*.front.stat" are located
#   -<number_of_runs> is the amount of jobs executed. e.g.: if number_of_runs is 4 you should have job.0.front.stat, ..., job.3.front.stat
#   -<objective_J_name> is the label for the axis corresponding to objective J in the plot

# IMPORTANT: THIS SCRIPT ASSUMES MINIMIZATION OF BOTH OBJECTIVES. YOU SHOULD MODIFY THESE BEHAVIOUR TO FIT YOUR NEEDS.

# The metrics are calculated using the formulas in  "Multiobjective optimization using Evolutionary Algorithms" from Kalyanmoy Deb.
# For the spread calculation, the euclidean distance is used.
# Hypervolumes are calculated using the code of Simon Wessing from TU Dortmund University found at https://ls11-www.cs.uni-dortmund.de/rudolph/hypervolume/start

# Please feel free to contact me at: renzom@fing.edu.uy

##############################################################
##############################################################
#AUXILIARY FUNCTIONS

import sys
sys.path.append('../libs')

import numpy as np
from pylab import *

import metricslib
from hv import HyperVolume

####################################
########## MAIN ####################

if __name__ == "__main__":

    if (len(sys.argv)<5):
        print "Not enough parameters. Usage: python {0} <path_to_results> <number_of_runs> <obj1_name> <obj2_name>".format(sys.argv[0])
        exit(-1)
    else:
        path_to_results=sys.argv[1]
        number_of_runs=int(sys.argv[2])
        objectives=[sys.argv[3],sys.argv[4]]
    

    #Initialize dictionary to parse the pareto fronts
    results= {}
    for run in range (0,number_of_runs):
        results[run]={}
        for obj in objectives:
            results[run][obj]=[]


    #Load the pareto fronts from the files
    for run in range(0,number_of_runs):
        path_to_file="%sjob.%d.front.stat" %(path_to_results,run)
        f=open (path_to_file)
        lines= f.readlines()
        for line in lines:
            tokens=line.split()
            results[run][objectives[0]].append(float(tokens[0]))
            results[run][objectives[1]].append(float(tokens[1]))
        f.close()

    # Define colors for plots
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(p) for p in np.linspace(0, 1, int(number_of_runs))]

    #Let's find the global pareto front combining all runs
    x=[]
    y=[]
    for run in range (0,number_of_runs):
        for item in results[run][objectives[0]]:
            x.append(item)
        for item in results[run][objectives[1]]:
            y.append(item)
        scatter(results[run][objectives[0]],results[run][objectives[1]],label="Run #%d"%run, color=colors[run])


    global_pf=metricslib.pareto_frontier(x,y)
    plot(global_pf[0],global_pf[1],color="black", linestyle=":", label="Global PF")
    grid(True)
    xlabel (objectives[0])
    ylabel (objectives[1])
    title ("Global PF")
    legend(loc=0,ncol=3 ,prop={'size':10},scatterpoints = 1)
    savefig("%s/GlobalPF.png"%path_to_results)

    #Now let's calculate some metrics

    gd_list=[]
    spa_list=[]
    spr_list=[]
    hv_list=[]

    #The reference point to calculate the hypervolume is the projection of the global PF ends
    max_objective_0 = max(np.array(global_pf[0]))
    max_objective_1 = max(np.array(global_pf[1]))
    referencePoint = [max_objective_0, max_objective_1]


    for run in range (0,number_of_runs):
        gd_list.append(metricslib.generational_distance(results[run][objectives[0]],results[run][objectives[1]],global_pf))
        spa_list.append(metricslib.spacing(results[run][objectives[0]],results[run][objectives[1]]))
        spr_list.append(metricslib.spread(results[run][objectives[0]],results[run][objectives[1]], global_pf))
        
        hyperVolume = metricslib.HyperVolume(referencePoint)
        front=[]
        for k in range(0, len(results[run][objectives[0]])):
            front.append([results[run][objectives[0]][k],results[run][objectives[1]][k]])
        hv_list.append(hyperVolume.compute(front))


    #Compute the quotient between the PF of each run and the global PF
    hyperVolume = HyperVolume(referencePoint)
    front=[]
    for k in range(0, len(global_pf[0])):
            front.append([global_pf[0][k],global_pf[1][k]])

    hv_ideal_pf= hyperVolume.compute(front)
    hv_quotients_list=[x/float(hv_ideal_pf) for x in hv_list]


    # Print the results
    print ""
    print "########################"
    print "Generational Distance"
    print ""
    print "Min (best): %f"%np.min(np.array(gd_list))
    print "Mean: %f"%np.mean(np.array(gd_list))
    print "Std: %f"%np.std(np.array(gd_list))
    print "########################"

    print ""
    print "########################"
    print "Spacing"
    print ""
    print "Min (best): %f" %np.min(np.array(spa_list))
    print "Mean: %f" %np.mean(np.array(spa_list))
    print "Std: %f"%np.std(np.array(spa_list))
    print "########################"
    print ""

    print "########################"
    print "Spread"
    print ""
    print "Min (best): %f" %np.min(np.array(spr_list))
    print "Mean: %f" %np.mean(np.array(spr_list))
    print "Std: %f"%np.std(np.array(spr_list))
    print "########################"

    print ""
    print "########################"
    print "Relative hypervolumes"
    print ""
    print "Max (best): %f"%np.max(np.array(hv_quotients_list))
    print "Mean: %f"%np.mean(np.array(hv_quotients_list))
    print "Std: %f"%np.std(np.array(hv_quotients_list))
    print "########################"
    print ""
    print "You can find the plot at: %s%s"%(path_to_results,"GlobalPF.png")









