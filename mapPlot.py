#http://bokeh.pydata.org/en/0.11.1/docs/gallery/choropleth.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox, ColumnDataSource
from bokeh.charts import Bar
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
#myPath=os.path.dirname(os.path.abspath(__file__))
myPath='/Users/agrant/Documents/UMN/python/bokeh'
rawData=pandas.read_csv(os.path.join(myPath,'Net_generation_for_electric_power.csv'),header=4)

#need to split the first column into two columns
#
#https://gist.github.com/bsweger/e5817488d161f37dcbd2
# Split delimited values in a DataFrame column into two new columns
#df['new_col1'], df['new_col2'] = zip(*df['original_col'].apply(lambda x: x.split(': ', 1)))

#first, delete rows without the semicolon

rawData=rawData[rawData.description.str.find(':')>0]

rawData['location'], rawData['fuel']=zip(*rawData['description'].apply(lambda x: x.split(' : ',1)))
del rawData['description']
del rawData['units']
del rawData['source key']
#%%
#need to identify the index column .... that's maybe not going to work here
#oh, it has some index already. just leave that as is

#create a column data source that will be updated in the on_selection_change :)
#do I do my pandas slicing first and make a columndatasource of that? or can i do pandas actions on the CDS?

#http://stackoverflow.com/questions/27642179/bokeh-widget-to-select-a-group-from-dataframe
#looks like I update the CDS WITH the new groupby within the update widget, so I'll just make placeholder CDS for now


fuelByLoc=rawData.groupby(['location','fuel'])
#rawByLoc=rawData.groupby('location').sum()

rawByLoc=rawData.groupby('location')
rawByFuel=rawData.groupby('fuel')
fuelByLoc_2=rawByLoc['fuel'].mean()

#http://bconnelly.net/2013/10/summarizing-data-in-python-with-pandas/


#http://chrisalbon.com/python/pandas_apply_operations_to_groups.html
groupbyFuel=rawData['fuel'].groupby(rawData['location'])

#i think the problem is i have 3 dimensions--I want to collapse across time first? there's something I don't get here



#%%
#take the average of each row

#%%
#do it the old fashioned way
fuelTypes=pandas.unique(rawData['fuel'].ravel())
for iS,thisState in enumerate(stateNames):
    thisData=rawData.loc[rawData['location']==thisState]
    for iF, thisFuel in enumerate(fuelTypes):
        thisFuelData=thisData.loc[thisData['fuel']==thisFuel]
        thisMean=thisFuelData.mean()
       
       
       
#%%

    
#try taking the mean across the date columns
colNames=rawData.columns
colNames=colNames[:-2]
rawData[colNames].mean(axis=1) 
#gives me all NaNs
    
#fuelData=ColumnDataSource()
#create the bar chart
#figFuel=figure(plot_width=400, plot_height=200)
plotFuel=Bar(fuelByLoc['United States'])
figs=HBox(children=[plotMap,plotFuel])
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