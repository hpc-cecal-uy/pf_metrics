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


############################################################################################################################
# INSTRUCTIONS
# 
# Script to plot the global Pareto front and calculate generational distance, spread, spacing and relative hypervolume based
# on the pareto fronts output from ECJ (http://cs.gmu.edu/~eclab/projects/ecj/).
# 
# USAGE:
# python pf_metrics.py <path_to_results> <number_of_runs> <objective_1_name> <objective_2_name>
# 
# To run the example: 
# python pf_metrics.py example/ 5 Price Coverage
# 
# Notes:
# 	-<path_to_results> is the folder where the files "job.*.front.stat" are located
# 	-<number_of_runs> is the amount of jobs executed. e.g.: if number_of_runs is 4 you should have job.0.front.stat, ..., job.3.front.stat
# 	-<objective_J_name> is the label for the axis corresponding to objective J in the plot
# 
# IMPORTANT: THIS SCRIPT ASSUMES MINIMIZATION OF BOTH OBJECTIVES. YOU SHOULD MODIFY THESE BEHAVIOUR TO FIT YOUR NEEDS.
# 
# The metrics are calculated using the formulas in  "Multiobjective optimization using Evolutionary Algorithms" from Kalyanmoy Deb.
# For the spread calculation, the euclidean distance is used.
#
# Hypervolumes are calculated using the code of Simon Wessing from TU Dortmund University found at:
#    https://ls11-www.cs.uni-dortmund.de/rudolph/hypervolume/start
# 
# Please feel free to contact me at: renzom@fing.edu.uy
# 
############################################################################################################################

import sys
from os import path

sys.path.append('../libs')
import generic_pf_metrics

def load_ecj_results(path_to_results, objectives, number_of_runs):
    #Initialize dictionary to parse the pareto fronts
    results = []
    
    for run in range (0,number_of_runs):
        results.append([])

        for no in range(len(objectives)):
            results[run].append([])
    
    for run in range(0,number_of_runs):
        path_to_file = path.join(path_to_results, "job.{0}.front.stat".format(run))

        with open(path_to_file) as f:
            for line in f:
                tokens = line.split()

                for no in range(len(objectives)):
                    results[run][no].append(float(tokens[no]))

    return results

####################################
########## MAIN ####################

def main():
    ref_pf_file = None
    normalize = None
    
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Not enough parameters. Usage:")
        print(" - python {0} <path_to_results> <number_of_runs> <normalize> <obj1_name> <obj2_name>".format(sys.argv[0]))
        print(" - python {0} <reference pf> <path_to_results> <number_of_runs> <normalize> <obj1_name> <obj2_name>".format(sys.argv[0]))
        exit(-1)
    else:
        if len(sys.argv) == 6:
            path_to_results = sys.argv[1]
            number_of_runs = int(sys.argv[2])
            normalize = sys.argv[3].strip().lower()           
            objectives = [sys.argv[4], sys.argv[5]]
        else:
            ref_pf_file = sys.argv[1]
            path_to_results = sys.argv[2]
            number_of_runs = int(sys.argv[3])
            normalize = sys.argv[4].strip().lower()
            objectives = [sys.argv[5], sys.argv[6]]
                
    #Load the pareto fronts from the files
    results = load_ecj_results(path_to_results, objectives, number_of_runs)

    generic_pf_metrics.compute(ref_pf_file, path_to_results, number_of_runs, objectives, results, normalize)

if __name__ == "__main__":
    main()
