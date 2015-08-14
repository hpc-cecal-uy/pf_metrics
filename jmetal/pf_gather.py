#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pf_gather.py
#
#  This script loads a set of jMetal solutions from different
#  experiments and computes the aggregated Pareto front.
#
#  Copyright 2015 Santiago Iturriaga
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
from os import path

sys.path.append('../libs')
import generic_pf_metrics

def load_jmetal_results(path_to_results, num_objectives, num_runs):
    results = []
    
    for no in range(num_objectives):
        results.append([])
    
    for run in range(num_runs):
        path_to_file = path.join(path_to_results, "FUN.{0}".format(run))

        with open(path_to_file) as f:
            lines = f.readlines()
            
            for line in lines:
                tokens = line.split()

                for no in range(num_objectives):
                    results[no].append(float(tokens[no]))

    return results

def main():
    if len(sys.argv) < 4:
        print("This script loads a set of jMetal solutions from different experiments and computes the aggregated Pareto front.")
        print("Not enough arguments. Usage: {0} <num runs> <num obj> <result path 1> <result path 2> <result path 3> ...".format(sys.argv[0]))
        exit(-1)   

    num_runs = int(sys.argv[1])
    num_objectives = int(sys.argv[2])
    
    points = []
    for no in range(num_objectives):
        points.append([])

    for p in range(3, len(sys.argv)):
        aux_points = load_jmetal_results(sys.argv[p], num_objectives, num_runs)

        for no in range(num_objectives):
            points[no] = points[no] + aux_points[no]

    generic_pf_metrics.print_non_dominated(points)
        
    return 0

if __name__ == '__main__':
    main()

