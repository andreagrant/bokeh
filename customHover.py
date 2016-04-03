# Many lessons learned from http://bokeh.pydata.org/en/latest/docs/user_guide/interaction.html
from bokeh.plotting import figure, output_file, show, hplot
from bokeh.models import ColumnDataSource, HoverTool, CustomJS

import numpy as np

output_file("hover_test.html")

imSize = 64.0
subtense = 16.0
minSize = -imSize/2+1
maxSize = imSize/2
x,y = np.meshgrid(np.arange(imSize),np.arange(imSize))
x += -imSize/2 + 0.5
y += -imSize/2 + 0.5
r = np.sqrt(x**2 + y**2)*subtense/imSize
theta = np.arctan2(x,y)

logR = np.log(r.flatten()) - min(np.log(r.flatten()))
# flip right visual field around to left hemisphere
logR[theta.flatten() > 0] = -logR[theta.flatten() > 0] 

# learned by trial nd error that the variable passed to CustomJS code needs to
# be dictionary of lists
lpCoords = {
    0: list(logR),
    1: list(np.abs(theta.flatten()))
}

ctxXrange = [np.min(lpCoords[0]),np.max(lpCoords[0])]
ctxYrange = [np.min(lpCoords[1]),np.max(lpCoords[1])]

# th utterly painful way for the brain-dead
RFsize = np.zeros(x.shape)
for iR in range(r.shape[0]):
    for iC in range(r.shape[1]):
        if r[iR,iC] < 1:
            RFsize[iR,iC] = 0.5
        else:
            RFsize[iR,iC] = np.log(r[iR,iC]) + 1

# create the figure panels
imageSpace = figure(width=400, height=400, tools="", x_range=[minSize,maxSize], y_range=[minSize,maxSize], toolbar_location=None, title='Image space')
V1 = figure(width=400, height=200, tools="", x_range=ctxXrange, y_range=ctxYrange, toolbar_location=None, title='Left V1    |    right V1')

# plot the image space
imageSpace.image(image=[np.random.random((imSize,imSize))], x=[minSize], y=[minSize], dw=[imSize], dh=[imSize], palette="Spectral11")
RFs = imageSpace.circle(x=x.flatten(), y=y.flatten(), size=RFsize.flatten()*10, color='olive', alpha=0, hover_color='olive', hover_alpha=1.0)

# set up a data source for cortex space
source1 = ColumnDataSource({'x':[],'y':[]})
ctx = V1.square('x', 'y', source=source1, color='yellow', size=30, alpha=0.4)

# Add a hover tool that sends current dot over to other plot
code = """
var lpCoords = %s
var data = {'x': [], 'y': []}
var cdata = RFs.get('data');
var indices = cb_data.index['1d'].indices
data['x'].push(lpCoords[0][indices[0]])
data['y'].push(lpCoords[1][indices[0]])

ctx.set('data', data)
"""  % lpCoords

callback = CustomJS(args={'RFs': RFs.data_source, 'ctx': ctx.data_source}, code=code)
imageSpace.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[RFs]))

show(hplot(imageSpace,V1))