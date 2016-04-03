#http://bokeh.pydata.org/en/0.11.1/docs/gallery/choropleth.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox, ColumnDataSource
from bokeh.io import curdoc
import pandas
import os

#del states["AK"]
state_xs=[states[code]["lons"] for code in states]
state_ys=[states[code]["lats"] for code in states]

stateNames=[states[code]["name"] for code in states]

plotMap = figure(toolbar_location="right",plot_width=1100,plot_height=800,tools="tap")
plotMap.patches(state_xs,state_ys,fill_alpha=0.5,line_color="black",line_width=2,line_alpha=0.3,name="states")

#add a bar chart of the data

#first, get the data
#eventually, use the API to pull it from 
#http://www.eia.gov/electricity/data.cfm#consumption
#electricity generation by state and fuel type, monthly, for residential gen only
myPath=os.path.dirname(os.path.abspath(__file__))
rawData=pandas.read_csv(os.path.join(myPath,'Net_generation_for_electric_power.csv'),header=4)

#need to split the first column into two columns
#
#https://gist.github.com/bsweger/e5817488d161f37dcbd2
# Split delimited values in a DataFrame column into two new columns
#df['new_col1'], df['new_col2'] = zip(*df['original_col'].apply(lambda x: x.split(': ', 1)))


#need to identify the index column .... that's maybe not going to work here

#create a column data source that will be updated in the on_selection_change :)
#fuelData=ColumnDataSource()
#create the bar chart
plotFuel=figure(plot_width=400, plot_height=200)

figs=HBox(children=[plotMap])
#this below makes two copies othe map :(
#curdoc().add_root(HBox(children=[figs],width=1200))

#now, to figure out which state is selected
#https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/XGvStBxaz_M
def on_selection_change(attr, old, new):
    thisInd=new['1d']['indices']
    if len(thisInd)>0:
        print thisInd
        thisState=stateNames[thisInd[0]]
        print thisState
    else:
        print "all USA"
    
renderer=plotMap.select(dict(name="states"))
patches_ds=renderer[0].data_source

patches_ds.on_change('selected',on_selection_change)