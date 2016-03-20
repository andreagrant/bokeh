#recreate selection histogram bokeh demo

import numpy
from bokeh.models import BoxSelectTool, LassoSelectTool, Paragraph
from bokeh.plotting import figure, hplot, vplot

#create 3 data sets: normal distro diff params
x1=numpy.random.normal(loc=3, size=1000)*20
y1=numpy.random.normal(loc=7, size=1000)*10

x2=numpy.random.normal(loc=6, size=800)*50
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

hFig=figure(toolbar_location=None, plot_width=scatterFig.plot_width, plot_height=200,
            x_range=scatterFig.x_range, y_range=(-hMax,hMax), title=None,
            min_border=10, min_border_left=50)
hFig.xgrid.grid_line_color=None

hFig.quad(bottom=0, left=hEdges[:-1],right=hEdges[1:],top=hHist,color="white",line_color="blue")
#what are these? the selected and unselected points?
hh1=hFig.quad(bottom=0,left=hEdges[:-1],right=hEdges[1:],top=hZeros,alpha=0.5,**LINE_ARGS)
hh2=hFig.quad(bottom=0,left=hEdges[:-1],right=hEdges[1:],top=hZeros,alpha=0.1,**LINE_ARGS)

#create the vertical histogram
vHist, vEdges=numpy.histogram(y,bins=30)
vZeros=numpy.zeros(len(vEdges)-1)
vMax=max(vHist)*1.1

toolbarHeight=42 #adjust toolbar height :(

vFig=figure(toolbar_location=None, plot_width=200, plot_height=scatterFig.plot_height+toolbarHeight-10,
            x_range=(-vMax,vMax), y_range=scatterFig.y_range, title=None,
            min_border=10, min_border_top=toolbarHeight)
vFig.ygrid.grid_line_color=None
vFig.xaxis.major_label_orientation = -numpy.pi/2.0

vFig.quad(left=0, bottom=vEdges[:-1],top=hEdges[1:],right=vHist,color="white",line_color="blue")
#what are rhese? the selected and unselected points?
vh1=vFig.quad(left=0,bottom=vEdges[:-1],top=vEdges[1:],right=vZeros,alpha=0.5,**LINE_ARGS)
vh2=vFig.quad(left=0,bottom=vEdges[:-1],top=vEdges[1:],right=vZeros,alpha=0.1,**LINE_ARGS)

vFig.min_border_top=80
vFig.min_border_left=0
hFig.min_border_top=10
hFig.min_border_right=10
scatterFig.min_border_right=10
layout=vplot(hplot(scatterFig,vFig),hplot(hFig,Paragraph(width=200)),width=800,height=800)

def update(attr,old,new):
    inds=numpy.array(new['1d']['indices'])
    numpy.savetxt('testselect.txt',inds)
    if len(inds)==0 or len(inds)==len(x):
        hHist1,hHist2=hZeros,hZeros
        vHist1,vHist2=vZeros,vZeros
    else:
        negInds=numpy.ones_like(x,dtype=numpy.bool)
        negInds[inds]=False
        hHist1, _ =numpy.histogram(x[inds],bins=hEdges)
        vHist1, _ =numpy.histogram(y[inds],bins=vEdges)
        hHist2, _ =numpy.histogram(x[negInds],bins=hEdges)
        vHist2, _ =numpy.histogram(y[negInds],bins=vEdges)
    hh1.data_source.data["top"] = hHist1
    hh2.data_source.data["top"] = -hHist2
    vh1.data_source.data["right"] = vHist1
    vh2.data_source.data["right"] = -vHist2

scatterPlot.data_source.on_change('selected',update)











                        