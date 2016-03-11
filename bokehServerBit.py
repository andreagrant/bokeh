# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:14:52 2016

@author: agrant
"""

#making a little server version
#http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server-applications

import numpy

from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, vplot

#create plot without any data but define the ranges
myPlot = figure(x_range(0,100), y_range(0,100), toolbar_location=None)
#configure the plot stylings
myPlot.border_fill_color = 'black'
myPlot.background_fill_color = 'green'
myPlot.outline_line_color = None
myPlot.grid.grid_line_color=None