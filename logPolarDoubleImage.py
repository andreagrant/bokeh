# 
from bokeh.plotting import figure, output_file, show, hplot
from bokeh.models import ColumnDataSource, HoverTool, CustomJS

output_file("logPolarDoubleImage.html")

import numpy as np
import math

from PIL import Image
banjo = Image.open("/Users/caolman/Desktop/Projects/VirtualV1sion/banjo.jpg")
inputImg = np.asarray(banjo.crop((70,15,326,271)).resize((64,64)))
inputImg = np.mean(inputImg,axis=2)
inputImg = inputImg[::-1,:]
# start with an image and a subtense
#inputImg = np.random.random((64,64))
subtense = 8.0 # degrees

# create an image space -- this will define subtense limits and size of cortes
imSize = inputImg.shape[0] # pixels
# for plot ranges later
minSize = -imSize/2.+1
maxSize = imSize/2.
# create coordinate systems
x,y = np.meshgrid(np.arange(float(imSize)),np.arange(float(imSize)))
x += -imSize/2. + 0.5
y += -imSize/2. + 0.5
r = np.sqrt(x**2 + y**2)*subtense/imSize
theta = np.arctan2(x,y)

# Start from cortex end and create a list of image pixels that contributes
# to cortex RF.  Later, these will become pooled channel responses
ctxRes = 1.0
minRFsize = 0.125
# Engel 1997 will give us dimensions of cortex:  ecc = exp(0.063(d+ 36.54))
# For sanity, jetison central 0.5 deg
# inverting that ... log(ecc) = 0.063*(d + 36.54) ... d = log(ecc)/0.063 - 36.54
ctxLength = math.ceil(np.log(subtense/2)/0.063 - np.log(0.25)/0.63)
nHypercolumns = ctxLength/ctxRes
horizontalMeridianInCtx = np.arange(nHypercolumns)*ctxRes # this is location, in mm, on corte
RFcenters = np.exp(0.063*horizontalMeridianInCtx) - 1 + minRFsize
RFradii = RFcenters/4
RFradii[RFradii < minRFsize] = minRFsize

# now that we know, down the horizontal meridian, how much pooling we want to do
# march out and figure out how wide V1 needs to be in the other directionat each
# eccentricity
arcLengths = np.pi*RFcenters
dCs = RFcenters[1:] - RFcenters[0:-1] # how much spacing down meridian
dCs = np.append(dCs,dCs[len(dCs)-1])
# do the 2 hemispheres separately so we don't lose our minds ... starting with right ...
# but use same coordinate system, with left V1 getting the negative numbers
#
# we're going to come out of this with a list of lists, matching each (valid) (x,y)
# coordinate in cortex to a set of pixels in the input image
leftCtxCoords = []
leftCtxFeeders = []
rightCtxCoords = []
rightCtxFeeders = []
leftRFradiiPixelSpace = []
rightRFradiiPixelSpace = []
leftRFcentersPixelSpace = []
rightRFcentersPixelSpace = []
for iR in range(len(RFcenters)): 
    ctxX = horizontalMeridianInCtx[iR] # right hemi
    nYs = int(math.ceil(arcLengths[iR]/dCs[iR])) # match resolution in theta to resolution in r
    for iTheta in range(nYs):
        # now put a blob around those coords to define feeders
        theta = np.pi*iTheta/nYs + np.pi*0.5/nYs
        imgX = RFcenters[iR]*imSize/subtense*np.sin(theta)
        imgY = RFcenters[iR]*imSize/subtense*np.cos(theta)
        mask = np.sqrt((x-imgX)**2 + (y-imgY)**2)*subtense/imSize < RFradii[iR]
        if np.sum(mask):
            ctxY= (iTheta - round(nYs/2))*ctxRes
            leftCtxCoords.append([-ctxX-2,ctxY])
            #leftCtxFeeders.append(np.dstack((x[mask],y[mask])).reshape((np.sum(mask),2)))
            rightCtxCoords.append([ctxX+2,ctxY])
            #rightCtxFeeders.append(np.dstack((-x[mask],y[mask])).reshape((np.sum(mask),2)))
            leftRFradiiPixelSpace.append(RFradii[iR]*imSize/subtense)
            rightRFradiiPixelSpace.append(RFradii[iR]*imSize/subtense)
            leftRFcentersPixelSpace.append([imgX,imgY])
            rightRFcentersPixelSpace.append([-imgX,imgY])
            
bothHemiCoords = leftCtxCoords + rightCtxCoords
#bothHemiFeeders = leftCtxFeeders + rightCtxFeeders
bothHemiRFcenters = leftRFcentersPixelSpace + rightRFcentersPixelSpace
bothHemiRFradii = leftRFradiiPixelSpace + rightRFradiiPixelSpace
# learned by trial nd error that the variable passed to CustomJS code needs to
# be dictionary of lists
ctxCoords = {
    0: list(np.array(bothHemiCoords)[:,0]),
    1: list(np.array(bothHemiCoords)[:,1])
}
ctxXrange = [np.min(ctxCoords[0]),np.max(ctxCoords[0])]
ctxYrange = [np.min(ctxCoords[1]),np.max(ctxCoords[1])]

RFsize = np.array(bothHemiRFradii)
RFcenters = np.array(bothHemiRFcenters)

# create the figure panels
imageSpace1 = figure(width=400, height=400, tools="", x_range=[minSize,maxSize], y_range=[minSize,maxSize], toolbar_location=None, title='Image space')
imageSpace2 = figure(width=400, height=400, tools="", x_range=[minSize,maxSize], y_range=[minSize,maxSize], toolbar_location=None, title = 'Subtense +/- 4 deg.')
V1 = figure(width=400, height=200, tools="", x_range=ctxXrange, y_range=ctxYrange, toolbar_location=None, title='Left V1     |    right V1')

# plot the image space
imageSpace1.image(image=[inputImg], x=[minSize], y=[minSize], dw=[imSize], dh=[imSize])#, palette="Spectral11")
imageSpace1.segment(x0=[-3,0],y0=[0,-3],x1=[3,0],y1=[0,3], color='red', line_width=3)
RFstatic1 = imageSpace1.circle(x=RFcenters[:,0], y=RFcenters[:,1], size=RFsize*4, alpha=0, color = 'gray', hover_color='yellow', hover_alpha=0.8)
RFdynamic1 = imageSpace1.circle(x=[], y=[], size=[], alpha=0.8, color = 'green')
imageSpace1.xaxis.visible = None
imageSpace1.yaxis.visible = None

# plot the RFs w/o the image
imageSpace2.segment(x0=[-3,0],y0=[0,-3],x1=[3,0],y1=[0,3], color='red', line_width=3)
RFstatic2 = imageSpace2.circle(x=RFcenters[:,0], y=RFcenters[:,1], size=RFsize*4, alpha=0.3, color = 'gray', hover_color='yellow', hover_alpha=0.8)
RFdynamic2 = imageSpace2.circle(x=[], y=[], size=[], alpha=0.8, color = 'green')
imageSpace2.xaxis.visible = None
imageSpace2.yaxis.visible = None

# set up a data source for cortex space
ctxStatic = V1.square(x=ctxCoords[0], y=ctxCoords[1], color='gray', size=5, alpha=0.5, hover_color='red', hover_alpha=0.5)
ctxDynamic = V1.square('x', 'y', source=ColumnDataSource({'x':[],'y':[]}), color='orange', size=10, alpha=0.8)

# Add a hover tool for imageSpace plot ... should create projective field
code1 = """
var ctxCoords = %s
var data = {'x': [], 'y': []}
var cdata = RFs.get('data')
var indices = cb_data.index['1d'].indices
for (i=0; i< indices.length; i++) {
    data['x'].push(ctxCoords[0][indices[i]])
    data['y'].push(ctxCoords[1][indices[i]])
}
ctx.set('data', data)
"""  % ctxCoords

callback = CustomJS(args={'RFs': RFstatic1.data_source, 'ctx': ctxDynamic.data_source}, code=code1)
imageSpace1.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[RFstatic1]))

callback = CustomJS(args={'RFs': RFstatic2.data_source, 'ctx': ctxDynamic.data_source}, code=code1)
imageSpace2.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[RFstatic2]))

# hover tool for ctx-space plot ... should pick out one RF
code2 = """
var data = {'x': [], 'y': [], 'size': []}
var imgdata = RFstatic1.get('data')
var cdata = ctx.get('data')
var indices = cb_data.index['1d'].indices
data['x'].push(imgdata.x[indices[0]]);
data['y'].push(imgdata.y[indices[0]]);
data['size'].push(imgdata.size[indices[0]])
RFdynamic1.set('data', data)
RFdynamic2.set('data', data)
""" 
callback = CustomJS(args={'RFstatic1': RFstatic1.data_source, 'RFdynamic1': RFdynamic1.data_source, 'RFdynamic2': RFdynamic2.data_source, 'ctx': ctxStatic.data_source}, code=code2)
V1.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[ctxStatic]))

show(hplot(imageSpace1,imageSpace2,V1))
