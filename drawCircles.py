from bokeh.plotting import Figure
from bokeh.models import BoxSelectTool, ColumnDataSource, HBox
from bokeh.io import curdoc
import numpy

#x0,y0=numpy.meshgrid(1,1,indexing='xy')
#circleSource=ColumnDataSource(data={'x':[numpy.ravel(x0)*10.0],'y':[numpy.ravel(y0)*10.0]})

x0=numpy.random.rand(10)
y0=numpy.random.rand(10)
circleSource=ColumnDataSource(data=dict(x=x0*10.0,y=y0*10.0))

p=Figure(x_range=[-10,10], y_range=[0,10], plot_width=400, plot_height=400,tools="crosshair, box_select, wheel_zoom")
#p.circle('x','y',source=circleSource,size=10,color="navy")
p.scatter(x0,y0,size=10,color="navy")
p.select(BoxSelectTool).select_every_mousemove = False


p2=Figure(x_range=[-10,10], y_range=[0,10], plot_width=400, plot_height=400,tools="crosshair, box_select, wheel_zoom")
p2.scatter('x','y',source=circleSource,size=10,color="navy",name="scatter")
p2.select(BoxSelectTool).select_every_mousemove = False
renderer = p2.select(dict(name="scatter"))
scatter_ds = renderer[0].data_source

figs=HBox(children=[p,p2])
curdoc().add_root(HBox(children=[figs],width=800))

def updateSelection(attrname, old, new):
    inds=numpy.array(new['1d']['indices'])
    #print(inds)
    numpy.savetxt('selInds.txt',inds,fmt='%d')
    
    
#p2.on_change('selected',updateSelection)
scatter_ds.on_change('selected', updateSelection)