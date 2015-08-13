#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pf_gather.py
#  
#  Copyright 2015 Santiago Iturriaga - INCO <siturria@saxo.fing.edu.uy>
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
sys.path.append('../libs')
import generic_pf_metrics

def load_ecj_results(path_to_results, number_of_runs):
    results = [[],[]]
    
    for run in range(number_of_runs):
        path_to_file = "{0}job.{1}.front.stat".format(path_to_results,run)
        f = open (path_to_file)
        lines = f.readlines()
        
        for line in lines:
            tokens = line.split()
            results[0].append(float(tokens[0]))
            results[1].append(float(tokens[1]))
        f.close()

    return results

def main():
    if len(sys.argv) < 3:
        print("Not enough arguments. Usage: {0} <num runs> <result path 1> <result path 2> <result path 3> ...".format(sys.argv[0]))
        exit(-1)   

    num_runs = int(sys.argv[1])
    results_paths = [[],[]]

    for p in range(2, len(sys.argv)):
        aux_results = load_ecj_results(sys.argv[p], num_runs)
        results_paths[0] = results_paths[0] + aux_results[0]
        results_paths[1] = results_paths[1] + aux_results[1]

    generic_pf_metrics.gather_pf(results_paths)
        
    return 0

if __name__ == '__main__':
    main()

