#recreate selection histogram bokeh demo

import numpy
from bokeh.models import BoxSelectTool, LassoSelectTool, Paragraph
from bokeh.plotting import figure, hplot, vplot

#create 3 data sets: normal distro diff params
x1=numpy.random.normal(loc=3, size=1000)*100
y1=numpy.random.normal(loc=7, size=1000)*10

x2=numpy.random.normal(loc=36, size=800)*50
y2=numpy.random.normal(loc=8, size=800)*10

x3=numpy.random.normal(loc=7, size=500)*10
y3=numpy.random.normal(loc=2, size=500)*10

x=numpy.concatenate((x1,x2,x3))
y=numpy.concatenate((y1,y2,y3))

TOOLS="pan, wheel_zoom, box_select, lasso_select"

#create a scatter plot

scatterFig=figure(tools=TOOLS, plot_width=600, plot_height=600, title=None,
              min_border=10,min_border_left=50)
scatterPlot=scatterFig.scatter(x,y,size=3,color="blue",alpha=0.6)

scatterFig.select(BoxSelectTool).select_every_mousemove=False
scatterFig.select(LassoSelectTool).select_every_mousemove=False

#create the horizontal histogram
hHist, hEdges=numpy.histogram(x,bins=30)
hZeros=numpy.zeros(len(hEdges)-1)
hMax=max(hHist)*1.1

LINE_ARGS=dict(color="blue",line_color=None)

