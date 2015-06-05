#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gnuplot.py
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

import numpy as np
from pylab import *

def plot_allruns(objectives, global_pf, results, path_to_results):
    # Define colors for plots
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(p) for p in np.linspace(0, 1, len(results))]

    for run in range(len(results)):
        scatter(results[run][objectives[0]],results[run][objectives[1]],label="Run #%d"%run, color=colors[run])
    
    plot(global_pf[0],global_pf[1],color="black", linestyle=":", label="Global PF")
    grid(True)
    xlabel (objectives[0])
    ylabel (objectives[1])
    title ("Global PF")
    legend(loc=0,ncol=3 ,prop={'size':10},scatterpoints = 1)
    savefig("%s/GlobalPF.png"%path_to_results)

