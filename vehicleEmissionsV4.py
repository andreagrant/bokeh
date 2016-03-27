import numpy
import matplotlib.pyplot as plt
import os
import xlrd
from bokeh.plotting import Figure
from bokeh.io import curdoc
from bokeh.models import HBox, VBoxForm, VBox, ColumnDataSource, BoxSelectTool
from bokeh.sampledata.sample_geojson import geojson
#http://bokeh.pydata.org/en/0.11.1/docs/user_guide/geo.html
geoSouce=GeoJSONDataSource(geojson=geojson)
#http://bokeh.pydata.org/en/latest/docs/gallery/choropleth.html
plotFlag=1
myPath=os.path.dirname(os.path.realpath(__file__))
fid=open(os.join(myPath,'Net_generation_for_electric_power.csv'),'r')
#http://www.eia.gov/electricity/data.cfm#consumption
#electricty generation by STATE and FUEL TYPE. monthly data going back 20? years
#FOR RESIDENTIAL ELECTRICITY GENERATION ONLY. these values do not include electricit
#generated for industrial or commercial custoemrs
lines=[line.strip() for line in fid]
type(lines)
len(lines)
#lines[1]
fid.close()
#4 header lines, then one column label, then data
colHeaders=lines[4].split(',')
one=colHeaders[0]
type(one)
one.replace('"','')
colHeaders=[item.replace('"','') for item in colHeaders]
data=[row for row in lines[6:len(lines)]]
data=[item.replace('--','nan') for item in data]
dataTable=[row.split(',') for row in data]
#num rows
len(dataTable)
#num cols
len(dataTable[0])

#find unique list of states+us--find unique entries in col 0
dupeStatesFuels=[item[0] for item in dataTable]
len(dupeStatesFuels)
dupeStatesFuels=[item.strip('"') for item in dupeStatesFuels]
splitStatesFuels=[item.split(' : ') for item in dupeStatesFuels]
messyStates=[item[0] for item in splitStatesFuels]
states=set(messyStates)
ind=[i for i, x in enumerate(messyStates) if x=='United States']
splitStatesFuels[2][1]
fuels=set([item[1] for item in splitStatesFuels if len(item)>1])
#print fuels


#create a numpy array of the actual data
#how many states, how many fuels, how many timepoints
numStates=len(states)
numFuels=len(fuels)
#print numFuels
numDates=len(colHeaders)-3
dt=numpy.zeros((numFuels,numDates,numStates))
len(dataTable)
#numStates*(numFuels+1)

#loop through states, then fuels to get rows, then through dates to get columns
dataTable[2][3:5]
range(3,6)
for iState in range(numStates):
#for iState in range(2):
    for iFuel in range(numFuels):
        for iDate in range(numDates):
#        for iDate in range(1):
            thisX=iState*(numFuels+1)+iFuel+1
            thisY=iDate+3
            #print thisX
            #print dataTable[thisX][thisY]
            thisDatum=dataTable[thisX][thisY]
            #print thisDatum
            #print len(thisDatum)
            #print iFuel, iDate, iState, thisDatum
            #dt3d[iFuel][iDate][iState]=thisDatum
            if thisDatum.find('"')==-1:
                dt[iFuel][iDate][iState]=float(thisDatum)
            else:
                dt[iFuel][iDate][iState]=numpy.nan

#calculate annual means for 2013?
#find 2013
myYear=[i.find('2013') for i in colHeaders]
inds=[0]*len(colHeaders)
for i in range(len(colHeaders)):
    thisInd=myYear[i]
    #print thisInd, i
    if thisInd>0:
        inds[i]=i
    else:
        inds[i]=0

#print inds
#wheee let's hardcode 2013!
#dt2013=dt[0:numFuels][147:158][0:numStates]
#hmm, that comes out the wrong size...
dt2013=dt[:][:,147:158+1][:]
#no, I can do this the right way
keepInds=[item for item in inds if item>0]
#print keepInds
dt2013=dt[:][:,keepInds[0]:keepInds[-1]+1][:]
#not sure why I need :,range?????????
#oh, i was addressing it wrong==ONE set of []
dt2013=dt[:,keepInds[0]:keepInds[-1]+1,:]
dt2013.shape

thisData=numpy.zeros(12)
mean2013=numpy.zeros((numFuels,numStates))
totals2013=numpy.zeros((numFuels,numStates))
for iState in range(numStates):
    for iFuel in range(numFuels):
        thisData=dt2013[iFuel,:,iState]
        #average
        thismean=numpy.nanmean(thisData)
        mean2013[iFuel][iState]=thismean
        thistotal=numpy.nansum(thisData)
        totals2013[iFuel][iState]=thistotal

#fuels and states are "sets" not lists, so I need to extract them
#fuelsL=[x for x in fuels]
#statesL=[x for x in states]
#those are out of order
fuelsL=['']*numFuels
statesL=['']*numStates
for iFuel in range(numFuels):
    fuelsL[iFuel]=splitStatesFuels[iFuel+1][1]
row=0
for iState in range(0,len(splitStatesFuels),numFuels+1):
    #print row, iState,splitStatesFuels[iState][0]
    statesL[row]=splitStatesFuels[iState][0]
    row+=1

iState=0
xLocs=numpy.arange(numFuels)
barWidth=0.35
thisData=mean2013[:,iState]
# fig,ax=plt.subplots()
# # plt.plot(thisData,'x')
# # plt.bar(xLocs+barWidth/2.,thisData/1000.,barWidth)
# plt.semilogy(xLocs+barWidth/2.,thisData/1000., 'o')
# # plt.vlines(xLocs+barWidth/2.,[0]*numFuels,thisData/1000.,'--')
# plt.ylim((0,350))
# plt.yticks(numpy.linspace(0,350,8))
# plt.xticks(xLocs+barWidth,fuelsL,rotation='vertical')
# #plt.xlabel('Fuel source')
# plt.title(statesL[iState])
# plt.ylabel('$10^6$  MW-hr')
# plt.tight_layout()
# plt.tick_params(direction="out")
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
# plt.show()
#


#need three scales==all US, regions, states
#what are the regions? I'm also going to ditch DC
regionNames=['New England','Mountain','Middle Atlantic','West South Central','Pacific Noncontiguous',
             'South Atlantic','East North Central','West North Central','East South Central',
             'Pacific Contiguous','District Of Columbia']

statesAndRegions=[item for item in statesL if item != 'United States']
statesOnly=[item for item in statesAndRegions if item not in regionNames]
numRegions=len(regionNames)
numStatesOnly=len(statesOnly)

#plot each state--total for each fuel type
stateMax=numpy.zeros((numStates,1))
if plotFlag==1:
    for iState in range(numStates):
        # thisData=mean2013[:,iState]
        thisData=totals2013[:,iState]
        #print statesL[iState],numpy.nanmax(thisData)
        stateMax[iState]=numpy.nanmax(thisData)
        fig,ax=plt.subplots()
        # plt.plot(thisData,'x')
        plt.bar(xLocs+barWidth/2.,thisData/1000.,barWidth)
        # plt.plot(xLocs+barWidth/2.,thisData/1000., 'o--')
        if statesL[iState]=='United States':
            ymax=350*10
            ysteps=8
        elif statesL[iState] in regionNames:
            ymax=70*10
            ysteps=8
        else:
            ymax=35*10
            ysteps=8
        plt.ylim((0,ymax))
        plt.yticks(numpy.linspace(0,ymax,ysteps))
        plt.xticks(xLocs+barWidth,fuelsL,rotation='vertical',fontsize=16)
        plt.ylabel('$10^6$  MW-hr',fontsize=18)
        #plt.text(5,ymax*0.8,stateMax[iState])
        #plt.xlabel('Fuel source')
        plt.title('Total residential electricity generation in 2013 for '+statesL[iState],fontsize=20)
        #plt.tight_layout()
        plt.tick_params(direction="out")
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        fig.set_size_inches(18.5,10.5)
        # plt.show()
        plt.savefig(statesL[iState],bbox_inches='tight')
        plt.close(fig)
# numpy.savetxt('stateNames.txt',statesL,fmt='%s')
# numpy.savetxt('stateMax.txt',stateMax,fmt='%f')
#make a big plot of all states
#christ. clustered bar charts are a serious PITA. have to plot each one separately and control the spacing manually

# fig1,ax1=plt.subplot()
# initialGap=0.1
# start=initialGap
# width=1.0
# gap=0.05
# colors='rgbcmykrgbcmykrgbcmyk'
# # for iState in range(numStates):
# #     if statesL[iState] in statesOnly:
# ind=[iState for iState in range(numStates) if statesL[iState] in statesOnly]
# for iFuel in range(numFuels):
#     thisData=mean2013[iFuel,ind]
#     size=len(thisData)
#     thisX=numpy.linspace(start,start+width,size+1)[:-1]#this last bit takes all but the last element of the linspace
#     w=thisX[1]-thisX[0]
#     start=start+width+gap
#     plt.bar(thisX,thisData,w,color=list(colors[:size]))
#
# tick_loc = (numpy.arange(len(mean2013)) * (width+gap)) + initialGap + width/2
# ax.set_xticklabels(fuelsL)
# #ax.xaxis.set_major_locator(mtick.FixedLocator(tick_loc))
#
# plt.show()

#plot each fuel type--totals for each state
xLocs=numpy.arange(numStatesOnly)*1.1
barWidth=0.5
ind=[iState for iState in range(numStates) if statesL[iState] in statesOnly]
# fig,ax=plt.subplots(4,4)
if plotFlag==1:
    for iFuel in range(numFuels):
        # thisData=mean2013[iFuel,ind]
        thisData=totals2013[iFuel,ind]
        # plt.subplot(4,4,iFuel)
        fig,ax=plt.subplots()
        plt.bar(xLocs+barWidth/2.,thisData/1000.,barWidth)
        # plt.plot(xLocs+barWidth/2.,thisData/1000., 'o--')
        if iFuel==0:
            ymax=35*10
            ysteps=8
        else:
            ymax=15*10
            ysteps=6
        plt.ylim((0,ymax))
        plt.yticks(numpy.linspace(0,ymax,ysteps))
        #print iFuel, xLocs+barWidth
        plt.xlim((0,xLocs[-1]+barWidth))
        plt.xticks(xLocs+barWidth,statesOnly,rotation='vertical',fontsize=16)
        plt.ylabel('$10^6$  MW-hr',fontsize=18)
        #plt.text(5,ymax*0.8,stateMax[iState])
        #plt.xlabel('Fuel source')
        plt.title('Total residential electricity generation in 2013 using '+fuelsL[iFuel],fontsize=20)
        #plt.tight_layout()
        plt.tick_params(direction="out")
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        fig.set_size_inches(18.5,10.5)
        plt.savefig(fuelsL[iFuel],bbox_inches='tight')
        plt.close(fig)
# plt.show()
# plt.savefig('panel.eps')
# plt.close(fig)


#################

#Now, let's normalize that data by population, just for visualization purposes
#obtained population data for 2013 from census.gov
    # http://www.census.gov/popest/data/state/totals/2013/
# fid=open('NST-EST2013-01.csv','r')
# popLines=[line.strip() for line in fid]
# fid.close()
# #4 headerlines
# #hardcoding ..... whee!
# popData=[row for row in popLines[4:56]]
# #col 0 is location col 6 is 2013 data
# #remove quotes and split on commas
# popData=[item.replace('"','') for item in popData]
# popData=[item.split(',') for item in popData]
#OMG they use fucking commas in the numbers AND as the delimiters.
#start with their excel file.
xbook=xlrd.open_workbook('NST-EST2013-01.xls')
xsheet=xbook.sheet_by_index(0)
numRowsPop=xsheet.nrows - 1
#numColsPop=xsheet.ncols - 1
pops2013=numpy.zeros((numStates,1))*numpy.nan
for iRow in range(numRowsPop):
    thisStatePop=xsheet.cell_value(iRow,0)
    #loop through statesL to find IF this is one of them and WHICH ROW it is
    for iState in range(numStates):
        thisState=statesL[iState]
        if thisStatePop.encode('ascii','ignore').strip('.') == thisState:
            pops2013[iState]=xsheet.cell_value(iRow,6)


#recreate both sets of plots with population-normalized data

#one plot per state--actual states only
iState=0
xLocs=numpy.arange(numFuels)
barWidth=0.35
stateMaxNorm=numpy.zeros((numStates,1))
if plotFlag==1:
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            # thisData=mean2013[:,iState]/pops2013[iState]
            thisData=totals2013[:,iState]/pops2013[iState]
            #what scale? mean2013 is in 10^6 MW-hr
            #let's first get rid of the million
            #multiply by 10^6 so it's in MW-hr PER PERSON
            thisData=thisData*(10**6)
            #print statesL[iState],numpy.nanmax(thisData)
            stateMaxNorm[iState]=numpy.nanmax(thisData)
            fig,ax=plt.subplots()
            # plt.plot(thisData,'x')
            plt.bar(xLocs+barWidth/2.,thisData,barWidth)
            # plt.plot(xLocs+barWidth/2.,thisData/1000., 'o--')
            if statesL[iState]=='United States':
                ymax=1100*10
                ysteps=12
            # elif statesL[iState] in regionNames:
            #     ymax=4500
            #     ysteps=10
            else:
                ymax=4500*20
                ysteps=10
            plt.ylim((0,ymax))
            plt.yticks(numpy.linspace(0,ymax,ysteps))
            plt.xticks(xLocs+barWidth,fuelsL,rotation='vertical',fontsize=16)
            plt.ylabel('MW-hr per person',fontsize=18)
            #plt.text(5,ymax*0.8,stateMax[iState])
            #plt.xlabel('Fuel source')
            plt.title('Total residential electricity generation in 2013 for '+statesL[iState],fontsize=20)
            #plt.tight_layout()
            plt.tick_params(direction="out")
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            fig.set_size_inches(18.5,10.5)
            # plt.show()
            plt.savefig(statesL[iState]+'_normByPop',bbox_inches='tight')
            plt.close(fig)


#one plot per fuel type
xLocs=numpy.arange(numStatesOnly)*1.1
barWidth=0.5
ind=[iState for iState in range(numStates) if statesL[iState] in statesOnly]
# fig,ax=plt.subplots(4,4)
if plotFlag==1:
    for iFuel in range(numFuels):
        # thisData=mean2013[iFuel,ind]/pops2013[iState]
        goofyData=totals2013[iFuel,ind]/numpy.transpose(pops2013[ind])
        thisData=goofyData[0][:]
        #want in MW-hr not millions of MW-hr
        thisData=thisData*(10**6)
        # plt.subplot(4,4,iFuel)
        fig,ax=plt.subplots()
        plt.bar(xLocs+barWidth/2.,thisData,barWidth)
        # plt.plot(xLocs+barWidth/2.,thisData/1000., 'o--')
        if iFuel==0:
            ymax=100000
            ysteps=11
        else:
            ymax=75000
            ysteps=6
        plt.ylim((0,ymax))
        plt.yticks(numpy.linspace(0,ymax,ysteps))
        #print iFuel, xLocs+barWidth
        plt.xlim((0,xLocs[-1]+barWidth))
        plt.xticks(xLocs+barWidth,statesOnly,rotation='vertical',fontsize=16)
        plt.ylabel('MW-hr per person',fontsize=18)
        #plt.text(5,ymax*0.8,stateMax[iState])
        #plt.xlabel('Fuel source')
        plt.title('Total residential electricity generation in 2013 using '+fuelsL[iFuel],fontsize=20)
        #plt.tight_layout()
        plt.tick_params(direction="out")
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.subplots_adjust(bottom=0.15)
        fig.set_size_inches(18.5,10.5)
        plt.savefig(fuelsL[iFuel]+'_normByPop',bbox_inches='tight')
        plt.close(fig)









#ah, and plot as "percentage of all for this (state/fuel)"


#one plot per state--actual states only
iState=0
xLocs=numpy.arange(numFuels-1)
barWidth=0.35
stateMaxNorm=numpy.zeros((numStates,1))
if plotFlag==1:
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            #divide by all fuels amount, cnvert to pct
            thisData=100.*totals2013[:,iState]/totals2013[0,iState]
            fig,ax=plt.subplots()
            # plt.plot(thisData,'x')
            plt.bar(xLocs+barWidth/2.,thisData[1:],barWidth)
            # plt.plot(xLocs+barWidth/2.,thisData/1000., 'o--')
            ymax=100
            ysteps=11
            plt.ylim((0,ymax))
            plt.yticks(numpy.linspace(0,ymax,ysteps))
            plt.xticks(xLocs+barWidth,fuelsL[1:],rotation='vertical',fontsize=16)
            plt.ylabel('Percent of total fuel',fontsize=18)
            #plt.text(5,ymax*0.8,stateMax[iState])
            #plt.xlabel('Fuel source')
            plt.title('Total residential electricity generation in 2013 for '+statesL[iState],fontsize=20)
            #plt.tight_layout()
            plt.tick_params(direction="out")
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            fig.set_size_inches(18.5,10.5)
            plt.subplots_adjust(bottom=0.15)
            # plt.show()
            plt.savefig(statesL[iState]+'_pctBar',bbox_inches='tight')
            plt.close(fig)


#one plot per fuel type
xLocs=numpy.arange(numStatesOnly)*1.1
barWidth=0.5
ind=[iState for iState in range(numStates) if statesL[iState] in statesOnly]
# fig,ax=plt.subplots(4,4)
if plotFlag==1:
    for iFuel in range(1,numFuels):
        thisData=100.*totals2013[iFuel,ind]/totals2013[0,ind]
        fig,ax=plt.subplots()
        plt.bar(xLocs+barWidth/2.,thisData,barWidth)
        ymax=100
        ysteps=11
        plt.ylim((0,ymax))
        plt.yticks(numpy.linspace(0,ymax,ysteps))
        #print iFuel, xLocs+barWidth
        plt.xlim((0,xLocs[-1]+barWidth))
        plt.xticks(xLocs+barWidth,statesOnly,rotation='vertical',fontsize=16)
        plt.ylabel('MW-hr per person',fontsize=18)
        #plt.text(5,ymax*0.8,stateMax[iState])
        #plt.xlabel('Fuel source')
        plt.title('Total residential electricity generation in 2013 using '+fuelsL[iFuel],fontsize=20)
        #plt.tight_layout()
        plt.tick_params(direction="out")
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.subplots_adjust(bottom=0.15)
        fig.set_size_inches(18.5,10.5)
        plt.savefig(fuelsL[iFuel]+'_pctBar',bbox_inches='tight')
        plt.close(fig)



#save data to a csv for d3js

fidOut=open('2013Fuels.csv','w')
headerline=['state']
for iFuel in range(numFuels):
    headerline.append(fuelsL[iFuel])
fidOut.write(','.join(headerline))
fidOut.write('\n')
for iFuel in range(numFuels):
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            fidOut.write('%s,'%statesL[iState])
            thing=totals2013[iFuel,iState].tolist()
            fidOut.write('%f,'%thing)
        fidOut.write('\n')
fidOut.close()

#oops, need the transpose
fidOut=open('2013Fuels2.csv','w')
headerline=['fuel']
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        headerline.append(statesL[iState])
fidOut.write(','.join(headerline))
fidOut.write('\n')
for iFuel in range(numFuels):
    fidOut.write('%s,'%fuelsL[iFuel])
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            thing=totals2013[iFuel,iState].tolist()
            fidOut.write('%f,'%thing)
    fidOut.write('\n')
fidOut.close()

fidOut=open('2013FuelsUS.csv','w')
fidOut.write('fuel,US,USpct\n')
for iFuel in range(numFuels):
    fidOut.write('%s,'%fuelsL[iFuel])
    for iState in range(numStates):
        if statesL[iState]  == 'United States':
            thing=totals2013[iFuel,iState].tolist()
            if numpy.isnan(thing):
                fidOut.write('%f,%f'%(-99999,-99999))
            else:
                fidOut.write('%f,%f'%(thing,100.*thing/totals2013[0,iState].tolist()))
    fidOut.write('\n')
fidOut.close()

fidOut=open('2013FuelsWithPct.csv','w')
headerline=['fuel']
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        headerline.append(statesL[iState])
        headerline.append(statesL[iState]+'Pct')
fidOut.write(','.join(headerline))
fidOut.write('\n')
for iFuel in range(numFuels):
    fidOut.write('%s,'%fuelsL[iFuel])
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            thing=totals2013[iFuel,iState].tolist()
            if numpy.isnan(thing):
                fidOut.write('%f,%f,'%(-99999,-99999))
            else:
                fidOut.write('%f,%f,'%(thing,100.*thing/totals2013[0,iState].tolist()))
    fidOut.write('\n')
fidOut.close()

#Negative generation denotes that electric power consumed for plant use exceeds gross generation.



#calculate pollution "per mile driven"
#Ah, the EPA has "miles per gallon equivalent", where they use an industry standard
# of 33.7kW-hr per gallon of gas. Combine that with the car's fuel efficiency, adn we
#get a "kw-hr per mile" value
#yay! averaging all cars listed on fueleconomy.gov, I get an average of 338 watt-hours/mile
# http://www.fueleconomy.gov/feg/evsbs.shtml
#these are for all-electrics. not dealing with hybrids for now

#now I need pollution emitted PER WATT-HOUR, not per "ton" or anything.
#polllution per watt-hour of generated electricty

#here is some data
#http://ampd.epa.gov/ampd/
#nox, so2, co2 emissions per state for electric utilitities. does it contain the total electricty generated?
#oy, these are messy. I have data by state, power plant, fuel type. explore

#first, calculate emissions as a function of gross load. separate by fuel type only. how variable are they?
fid=open('EPADownload_emission_11-02-2014NoFuckingCommas.csv','r')
linesEm=[line.strip() for line in fid]
fid.close()
#col 0 is state, col 6 is so2(tons), 8 is nox (tons), 9 is co2(short tons), 12 is the number of primary fuels, 13&14 are the
#primary fuels (assume equal usage--split in half? exclude?
#22 is the gross load in MW-h)

dataEm=[row.split(',') for row in linesEm[2:]]
# dataEmX2=[row.split(',') for row in linesEm[1:] if '1' in row[12]]
# dataEm=[['']*len(dataEmX[0]) for i in range(len(dataEmX))]
# #remove stray double quotes
# for iRow in range(len(dataEmX)):
#     for iCol in range(len(dataEmX[0])):
#         thing=dataEmX[iRow][iCol]
#         if '"' in thing:
#             # print iCol,iRow,thing
#             thing.replace('"','')
#         dataEm[iRow][iCol]=thing
#what are the fuels called? need to match them to my fuel list
dupeFuelsEm=[item[13] for item in dataEm]
fuelsEmSet=set(dupeFuelsEm)


#this is too complicated and doesn't include PM
#http://www.eia.gov/electricity/state/unitedstates/
# #gives
# Sulfur Dioxide (lbs/MWh) 	2.0
# Nitrogen Oxide (lbs/MWh) 	1.2
# Carbon Dioxide (lbs/MWh) 	1,172
#for US averages


#aaaand using data from http://www.eia.gov/electricity/data.cfm#summary
#grams per mile driven ,assuming 340 w-hr/mile average
co2Coal=1132.46
co2Petroleum=1165.93
co2NaturalGas=682.1085
so2Coal=2.998
so2Petroleum=6.522
so2NaturalGas=0.0044
noxCoal=1.1138
noxPetroleum=1.893
noxNaturalGas=0.516
pollutionCO2=[]
pollutionSO2=[]
pollutionNOX=[]
for iState in range(numStates):
    #10^6 MW-hr
    if numpy.isnan(totals2013[1,iState]):
        thisCoal=0
    else:
        thisCoal=totals2013[1,iState]/totals2013[0,iState]
    if numpy.isnan(totals2013[2,iState]) and numpy.isnan(totals2013[3,iState]):
        thisPetroleum=0
    else:
        thisPetroleum=numpy.nansum([totals2013[2,iState],totals2013[3,iState]])/totals2013[0,iState]
    if numpy.isnan(totals2013[4,iState]) and numpy.isnan(totals2013[4,iState]):
        thisNaturalGas=0
    else:
        thisNaturalGas=numpy.nansum([totals2013[4,iState],totals2013[5,iState]])/totals2013[0,iState]
    thisCO2=thisCoal*co2Coal+thisPetroleum*co2Petroleum+thisNaturalGas*co2NaturalGas
    thisSO2=thisCoal*so2Coal+thisPetroleum*so2Petroleum+thisNaturalGas*so2NaturalGas
    thisNOX=thisCoal*noxCoal+thisPetroleum*noxPetroleum+thisNaturalGas*noxNaturalGas
    pollutionCO2.append(thisCO2)
    pollutionSO2.append(thisSO2)
    pollutionNOX.append(thisNOX)
fidOut=open('2013FuelsWithPctPoll.csv','w')
#fidOut=open('2013FuelsPoll.csv','w')
headerline=['fuel']
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        headerline.append(statesL[iState])
        headerline.append(statesL[iState]+'Pct')
fidOut.write(','.join(headerline))
fidOut.write('\n')
for iFuel in range(numFuels):
    fidOut.write('%s,'%fuelsL[iFuel])
    for iState in range(numStates):
        if statesL[iState] in statesOnly or statesL[iState] == 'United States':
            thing=totals2013[iFuel,iState].tolist()
            if numpy.isnan(thing):
                fidOut.write('%f,%f,'%(-99999,-99999))
            else:
                fidOut.write('%f,%f,'%(thing,100.*thing/totals2013[0,iState].tolist()))
    fidOut.write('\n')
fidOut.write('co2,')
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        fidOut.write('%f,-9999,'%(pollutionCO2[iState].tolist()))
fidOut.write('\n')
fidOut.write('so2,')
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        fidOut.write('%f,-9999,'%(pollutionSO2[iState].tolist()))
fidOut.write('\n')
fidOut.write('nox,')
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        fidOut.write('%f,-9999,'%(pollutionNOX[iState].tolist()))
fidOut.write('\n')

fidOut.close()

fidOut=open('2013FuelsPoll.csv','w')
fidOut.write('var pollution = [')
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        fidOut.write('{state: "%s", co2: %f, so2: %f, nox: %f},\n'%(statesL[iState],pollutionCO2[iState].tolist(),pollutionSO2[iState].tolist(),pollutionNOX[iState].tolist()))
fidOut.write('];')
fidOut.close()



fidOut=open('2013FuelsPollByState.csv','w')
for iState in range(numStates):
    if statesL[iState] in statesOnly or statesL[iState] == 'United States':
        fidOut.write('var pollution%s = [%f, %f, %f];\n'%(statesL[iState],pollutionCO2[iState].tolist(),pollutionSO2[iState].tolist(),pollutionNOX[iState].tolist()))
fidOut.close()
