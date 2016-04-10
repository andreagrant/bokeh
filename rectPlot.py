#http://bokeh.pydata.org/en/0.8.1/tutorial/solutions/gallery/olympics.html

from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as states
from bokeh.models import HBox, ColumnDataSource
from bokeh.charts import Bar
from bokeh.io import curdoc
import csv
import os
import numpy


#add a manually created bar chart of the data

#first, get the data
#eventually, use the API to pull it from 
#http://www.eia.gov/electricity/data.cfm#consumption
#electricity generation by state and fuel type, monthly, for residential gen only
#myPath=os.path.dirname(os.path.abspath(__file__))
myPath='/Users/agrant/Documents/UMN/python/bokeh/'
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
#        monthlyData[iR,:]=numpy.array(line[3:],dtype=numpy.float)
        iR+=1
dataMean=numpy.mean(monthlyData,1)

locList=list(set(location))
fuelTypes=list(set(fuel))
#%%
#find US row indices
inds=[i for i,item in enumerate(location) if item=='United States']
theseFuels=[fuel[i] for i in inds]
USData=dataMean[inds]
#USData[numpy.where(numpy.isnan(USData))]=-99
fuelData=ColumnDataSource(data=dict(fuels=theseFuels,amount=USData))
#create the bar chart
figFuel=figure(plot_width=800, plot_height=400,title='Residential electricity generation by fuel type',
               x_range=theseFuels,y_range=[0,max(USData)])
#plotFuel=Bar(fuelData,'fuels',values='amount')
figFuel.rect(x=theseFuels,y=USData/2,width=0.4, height=USData,color="black",alpha=0.6)
#figFuel.xgrid.grid_line_color=None
#figFuel.axis.major_label_text_font_size="8pt"
#figFuel.axis.major_label_standoff = 0
figFuel.xaxis.major_label_orientation = numpy.pi/3
#figFuel.xaxis.major_label_standoff = 6
#figFuel.xaxis.major_tick_out = 0

figs=HBox(children=[figFuel])

#this below makes two copies othe map :(
#curdoc().add_root(HBox(children=[figs],width=1200))

#now, to figure out which state is selected
#https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/XGvStBxaz_M
