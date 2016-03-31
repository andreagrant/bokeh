#http://bokeh.pydata.org/en/0.11.1/docs/gallery/choropleth.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox
from bokeh.io import curdoc

#del states["AK"]
state_xs=[states[code]["lons"] for code in states]
state_ys=[states[code]["lats"] for code in states]

plotMap = figure(toolbar_location="right",plot_width=1100,plot_height=800,tools="tap")
plotMap.patches(state_xs,state_ys,fill_alpha=0.5,line_color="black",line_width=2,line_alpha=0.3)

figs=HBox(children=[plotMap])
#curdoc().add_root(HBox(children=[figs],width=1200))

