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
sys.path.append('../libs')

import numpy as np
from pylab import *
from scipy import stats

import metricslib
import tabulatelib
import gnuplot
from hv import HyperVolume

def compute(path_to_results, number_of_runs, objectives, results):
    #Let's find the global pareto front combining all runs
    x=[]
    y=[]
    for run in range (0,number_of_runs):
        for item in results[run][objectives[0]]:
            x.append(item)
        for item in results[run][objectives[1]]:
            y.append(item)

    global_pf = metricslib.pareto_frontier(x,y)

    gnuplot.plot_allruns(objectives, global_pf, results, path_to_results)

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
        front = [[results[run][objectives[0]][i], results[run][objectives[1]][i]] for i in range(len(results[run][objectives[0]]))]  
        hv_list.append(hyperVolume.compute(front))

    #Compute the quotient between the PF of each run and the global PF
    hyperVolume = HyperVolume(referencePoint)
    front = [[global_pf[0][i],global_pf[1][i]] for i in range(len(global_pf[0]))]
    hv_ideal_pf = hyperVolume.compute(front)
    
    hv_quotients_list=[x/float(hv_ideal_pf) for x in hv_list]

    # Print the results
    print ""
    print "########################"
    print "Generational Distance"
    print "########################"
    print "Min (best): %f" % np.min(np.array(gd_list))
    print "Mean      : %f" % np.mean(np.array(gd_list))
    print "Median    : %f" % np.median(np.array(gd_list))
    print "Std dev   : %f" % np.std(np.array(gd_list))
    (w,p_value) = stats.shapiro(gd_list)
    print "Shapiro-wilk test: p-value=%f w=%f" % (p_value,w)

    print ""
    print "########################"
    print "Spacing"
    print "########################"
    print "Min (best): %f" %np.min(np.array(spa_list))
    print "Mean      : %f" %np.mean(np.array(spa_list))
    print "Median    : %f" %np.median(np.array(spa_list))
    print "Std dev   : %f"%np.std(np.array(spa_list))
    (w,p_value) = stats.shapiro(spa_list)
    print "Shapiro-wilk test: p-value=%f w=%f" % (p_value,w)
    print ""

    print "########################"
    print "Spread"
    print "########################"
    print "Min (best): %f" %np.min(np.array(spr_list))
    print "Mean      : %f" %np.mean(np.array(spr_list))
    print "Median    : %f" %np.median(np.array(spr_list))
    print "Std dev   : %f"%np.std(np.array(spr_list))
    (w,p_value) = stats.shapiro(spr_list)
    print "Shapiro-wilk test: p-value=%f w=%f" % (p_value,w)

    print ""
    print "########################"
    print "Relative hypervolumes"
    print "########################"
    print "Max (best): %f"%np.max(np.array(hv_quotients_list))
    print "Mean      : %f"%np.mean(np.array(hv_quotients_list))
    print "Median    : %f"%np.median(np.array(hv_quotients_list))
    print "Std dev   : %f"%np.std(np.array(hv_quotients_list))
    (w,p_value) = stats.shapiro(hv_quotients_list)
    print "Shapiro-wilk test: p-value=%f w=%f" % (p_value,w)
    print ""
    print "You can find the plot at: %s%s"%(path_to_results,"GlobalPF.png")







