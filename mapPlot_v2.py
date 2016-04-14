#http://bokeh.pydata.org/en/0.11.1/docs/gallery/choropleth.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox,VBox, ColumnDataSource
from bokeh.charts import Bar
from bokeh.io import curdoc, hplot
import csv
import os
import numpy

#del states["AK"]
state_xs=[states[code]["lons"] for code in states]
state_ys=[states[code]["lats"] for code in states]

#strip out that "eastern" bit of alaska that I don't need
stateNames=[states[code]["name"] for code in states]
AKind=stateNames.index('Alaska')
akY=state_ys[AKind]
akX=state_xs[AKind]
keepX=[]
keepY=[]
for (x,y) in zip(akX,akY):
    if x<0:
        keepX.append(x)
        keepY.append(y)
    else:
        keepX.append(numpy.nan)
        keepY.append(numpy.nan)
state_xs[AKind]=keepX
state_ys[AKind]=keepY

plotMap = figure(toolbar_location="right",plot_width=800,plot_height=650,tools="tap")
plotMap.patches(state_xs,state_ys,fill_alpha=0.5,line_color="black",line_width=2,line_alpha=0.3,name="states")

#add a bar chart of the data

#first, get the data
#eventually, use the API to pull it from 
#http://www.eia.gov/electricity/data.cfm#consumption
#electricity generation by state and fuel type, monthly, for residential gen only
myPath=os.path.dirname(os.path.abspath(__file__))
#myPath='/Users/agrant/Documents/UMN/python/bokeh/'
#maybe someday I can learn pandas, but a week of hacking at this dataset with
#pandas has only infuriated me. Taking the easy way out of doing it by hand
inFile='Net_generation_for_electric_power.csv'
#%%
#read in the data
rawInput=[]
with open(os.path.join(myPath,inFile),'r') as f:
    fileReader=csv.reader(f)
    rowNum=0
    for row in fileReader:
        if rowNum>3:
            rawInput.append(row)
        else:
            toss=row
        rowNum+=1

numRows=len(rawInput)
numCols=len(rawInput[0])

#extract locations and fuels
getDataRowCount=len([i[0] for i in rawInput if i[0].find(':')>0])
location=[]
fuel=[]
monthlyData=numpy.zeros((getDataRowCount,numCols-3))
dataMean=numpy.zeros((getDataRowCount,1))
iR=0
for line in rawInput:
    if line[0].find(':')>0:
        location.append(line[0].split(' : ')[0])
        fuel.append(line[0].split(' : ')[1])
        for j,item in enumerate(line):
            if j>2:
                if item=='':
                    monthlyData[iR,j-3]=numpy.nan
                elif item=='NM':
                    monthlyData[iR,j-3]=numpy.nan
                elif item=='--':
                    monthlyData[iR,j-3]=numpy.nan
                elif item=='---':
                    monthlyData[iR,j-3]=numpy.nan
                else:
                    monthlyData[iR,j-3]=numpy.float(item)
        iR+=1
dataMean=numpy.nanmean(monthlyData,1)
dataPercent=numpy.zeros((getDataRowCount,1))
locList=list(set(location))
fuelTypes=list(set(fuel))
#need to get percentage (or per capita)
locTotals={}
for thisLoc in locList:
    #find the rows with this location    
    locInds=[i for i,item in enumerate(location) if item==thisLoc]
    #get the all-fuel total
    for iInd in locInds:
        if fuel[iInd]=='all fuels':
            thisTotal=dataMean[iInd]
            locTotals[thisLoc]=thisTotal
    for iInd in locInds:
        dataPercent[iInd]=100*dataMean[iInd]/thisTotal


#%%
#find US row indices
inds=[i for i,item in enumerate(location) if item=='United States']
theseFuels=[fuel[i] for i in inds]
USData=[100*d/locTotals['United States'] for d in dataMean[inds]]

#print(inds,USData)
stateData=[0 for d in USData]
fuels_US=[c+":0.1" for c in theseFuels]
fuels_state=[c+":0.5" for c in theseFuels]
fuelData=ColumnDataSource(data=dict(fuels=fuels_state,amount=stateData,amountHalf=[d/2 for d in stateData]))

#create the bar chart
figFuel=figure(plot_width=650, plot_height=650,title='Residential electricity generation by fuel type',
               x_range=theseFuels,y_range=[0,100],y_axis_label='Percent of all generation')
figFuel.rect(x=fuels_US,y=[d/2 for d in USData],width=0.4, height=USData,color="SlateGray",alpha=0.6)#silver
figFuel.rect(x='fuels',y='amountHalf',width=0.4, height='amount',source=fuelData,color="blue",alpha=1.0)
figFuel.xaxis.major_label_orientation = numpy.pi/3
figFuel.xaxis.axis_label_text_font_size = "18pt"

#figs=HBox(children=[figFuel,plotMap])
#figs=HBox(figFuel,plotMap)
figs=hplot(figFuel,plotMap)# this worked!!!! :)

#this below makes two copies of the map :(
#curdoc().add_root(HBox(children=[figs],width=1200))

#now, to figure out which state is selected
#https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/XGvStBxaz_M
def on_selection_change(attr, old, new):
    thisInd=new['1d']['indices']
    if len(thisInd)>0:
        print thisInd
        thisState=stateNames[thisInd[0]]
        print thisState
        inds=[i for i,item in enumerate(location) if item==thisState]
        theseData=[]
        for d in dataMean[inds]:
            if numpy.isnan(d):
                theseData.append(0)
            else:
                theseData.append(100*d/locTotals[thisState])
        print(theseData)
        fuelData.data['amount']=theseData
        fuelData.data['amountHalf']=[d/2 for d in theseData]
    else:
        print "all USA"
        inds=[i for i,item in enumerate(location) if item=='United States']
        fuelData.data['amount']=[0 for d in dataMean[inds]]
        fuelData.data['amountHalf']=[0 for d in dataMean[inds]]
    
renderer=plotMap.select(dict(name="states"))
patches_ds=renderer[0].data_source

patches_ds.on_change('selected',on_selection_change)