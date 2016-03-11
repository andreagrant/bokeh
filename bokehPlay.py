# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:32:34 2016

@author: agrant
"""

from bokeh.plotting import figure, output_file, show

#make some data
x=[1,2,3,4,5]
y=[5,23,6,87,4]

#output to static html
output_file("lines.html",title="line plot example")

#create a plot
p=figure(title="simple line example", x_axis_label='x', y_axis_label='y')

#add a line rendering object iwth legend and thickness set
p.line(x,y,legend="temp", line_width=2)

#show the results
show(p)