#attempting to translate fuel viz into pure python!

__author__ = 'agrant'
import numpy
import os
import xlrd
#os.chdir('/Users/agrant/codes/d3learning')


xbook=xlrd.open_workbook('real_prices.xlsx')
#gasoline, monthly, sheet 6
xsheet=xbook.sheet_by_index(6)
#data in rows 40 to 504
#col 0 is date, col 2 is nominal price, col 3 is real price ($/gal)
gas=numpy.zeros((465,5))*numpy.nan
for iRow in range(465):
    thisDate=xlrd.xldate_as_tuple(xsheet.cell_value(iRow+40,0),0)
    gas[iRow][0]=thisDate[0]
    gas[iRow][1]=thisDate[1] #month
    gas[iRow][2]=thisDate[2]
    gas[iRow][3]=xsheet.cell_value(iRow+40,2)#nominal
    gas[iRow][4]=xsheet.cell_value(iRow+40,3)#real
xsheet=xbook.sheet_by_index(9)
#data in rows 40 to 468
#col 0 is date, col 2 is nominal price, col 3 is real price ($/gal)
diesel=numpy.zeros((429,5))*numpy.nan
for iRow in range(429):
    thisDate=xlrd.xldate_as_tuple(xsheet.cell_value(iRow+40,0),0)
    diesel[iRow][0]=thisDate[0]
    diesel[iRow][1]=thisDate[1] #month
    diesel[iRow][2]=thisDate[2]
    diesel[iRow][3]=xsheet.cell_value(iRow+40,2)
    diesel[iRow][4]=xsheet.cell_value(iRow+40,3)

#write out as a javascript variable
#myvar = [ {"name1":value1, "name2":value2}, {
fid=open('gas.txt','w')
for iRow in range(465):
    fid.write('{"date":"%04.0f-%02.0f-%02.0f", "nominal":%f, "real":%f},\n'%(gas[iRow][0], gas[iRow][1], gas[iRow][2],gas[iRow][3],gas[iRow][4]))
fid.close()
fid=open('diesel.txt','w')
for iRow in range(429):
    fid.write('{"date":"%04.0f-%02.0f-%02.0f", "nominal":%f, "real":%f},\n'%(diesel[iRow][0], diesel[iRow][1], diesel[iRow][2],diesel[iRow][3],diesel[iRow][4]))
fid.close()

#and make simple csv...... sigh
fid=open('gas.csv','w')
fid.write('date,nominal,real\n')
for iRow in range(465):
    fid.write('%04.0f-%02.0f-%02.0f,%f,%f\n'%(gas[iRow][0], gas[iRow][1], gas[iRow][2],gas[iRow][3],gas[iRow][4]))
fid.close()
fid=open('diesel.csv','w')
fid.write('date, nominal, real\n')
for iRow in range(429):
    fid.write('%04.0f-%02.0f-%02.0f,%f,%f\n'%(diesel[iRow][0], diesel[iRow][1], diesel[iRow][2],diesel[iRow][3],diesel[iRow][4]))
fid.close()

#ah, make a single file. need to line up the dates
#which starts earlier?
gasDates=gas[:,0]+gas[:,1]/12.0
dieselDates=diesel[:,0]+diesel[:,1]/12.0
if (dieselDates[0]<gasDates[0]):
    #diesel starts first--insert gas
    print 5
else:
    #gas starts first--insert diesel
    fuel=numpy.zeros((465,7))*numpy.nan
    #find first date for diesel
    for iRow in range(len(gas)):
        if gasDates[iRow]==dieselDates[0]:
            dieselStart=iRow
    for iRow in range(len(gas)):
        fuel[iRow][0]=gas[iRow][0]
        fuel[iRow][1]=gas[iRow][1]
        fuel[iRow][2]=gas[iRow][2]
        fuel[iRow][3]=gas[iRow][3]
        fuel[iRow][4]=gas[iRow][4]
        if iRow>=dieselStart:
            fuel[iRow][5]=diesel[iRow-dieselStart][3]
            fuel[iRow][6]=diesel[iRow-dieselStart][4]
        else:
            fuel[iRow][5]=-9999
            fuel[iRow][6]=-9999

fid=open('fuel.csv','w')
fid.write('date,gasnominal,gasreal,dieselnominal,dieselreal\n')
for iRow in range(465):
    if numpy.isnan(fuel[iRow][5]):
        fid.write('%04.0f-%02.0f-%02.0f,%f,%f,,\n'%(fuel[iRow][0], fuel[iRow][1], fuel[iRow][2],fuel[iRow][3],fuel[iRow][4]))
    else:
        fid.write('%04.0f-%02.0f-%02.0f,%f,%f,%f,%f\n'%(fuel[iRow][0], fuel[iRow][1], fuel[iRow][2],fuel[iRow][3],fuel[iRow][4],fuel[iRow][5],fuel[iRow][6]))
fid.close()
