#http://bokeh.pydata.org/en/0.11.1/docs/gallery/choropleth.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox
from bokeh.io import curdoc

#del states["AK"]
state_xs=[states[code]["lons"] for code in states]
state_ys=[states[code]["lats"] for code in states]

stateNames=[states[code]["name"] for code in states]

plotMap = figure(toolbar_location="right",plot_width=1100,plot_height=800,tools="tap")
plotMap.patches(state_xs,state_ys,fill_alpha=0.5,line_color="black",line_width=2,line_alpha=0.3,name="states")

figs=HBox(children=[plotMap])
#curdoc().add_root(HBox(children=[figs],width=1200))

#now, to figure out which state is selected

def on_selection_change(attr, old, new):
    thisInd=new['1d']['indices']
    print thisInd
    thisState=stateNames[thisInd[0]]
    print thisState
    
renderer=plotMap.select(dict(name="states"))
patches_ds=renderer[0].data_source

patches_ds.on_change('selected',on_selection_change)