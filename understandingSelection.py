#how to select a portion of the data to act on?
# https://github.com/bokeh/bokeh/blob/ad2d8923fa8902ae05ede19e9a977b943b860200/examples/plotting/server/selection_update.py
# http://bokeh.pydata.org/en/latest/docs/gallery.html#gallery


# https://github.com/bokeh/bokeh/tree/master/examples/plotting/server
# http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server-applications

from bokeh.models import HBox, ColumnDataSource, BoxSelectTool, VBox
from bokeh.plotting import Figure
import numpy
from bokeh.models.widgets import Slider
from bokeh.io import curdoc

imageRaw = numpy.random.rand(256,256)
source = ColumnDataSource(data={'image': [imageRaw]})


p = Figure(x_range=[0, 10], y_range=[0, 10],plot_width=400,plot_height=400,
           tools="crosshair, box_select, pan, reset, resize, save, wheel_zoom")
p.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source)


imageFFT = numpy.fft.fft2(imageRaw)
imageFFT=numpy.fft.fftshift(imageFFT)

x0,y0=numpy.meshgrid(range(imageFFT.shape[1]),range(imageFFT.shape[0]),indexing='xy')
x = x0 - imageFFT.shape[1]/2
y = y0 - imageFFT.shape[0]/2


circleSource=ColumnDataSource(data={'x':[numpy.ravel(x0)*10.0/imageFFT.shape[1]],'y':[numpy.ravel(y0)*10.0/imageFFT.shape[0]]})
p.circle('x','y',size=0.1,color="navy",alpha=0.5,source=circleSource)
p.select(BoxSelectTool).select_every_mousemove=False
orientation = Slider(title="Orientation (deg)", value=45.0, start=0.0, end =360.0)
orientationWidth = Slider(title="Orientation bandwidth (deg)", value=22.5, start=0.0, end =45.0)
spatialFreq = Slider(title="Spatial frequency (cycles/image)", value=16.0, start=0.0, end =64.0)
spatialFreqWidth = Slider(title="spatial frequency bandwidth", value=0.0, start=0.0, end =16.0)
inputs=VBox(children=[orientation,orientationWidth,spatialFreq, spatialFreqWidth])
#figs=HBox(children=[p,p2,p3])
figs=HBox(children=[p])

def updateSelection(attrname,old,new):
    inds=numpy.array(new)
    imageRawSelect = imageRaw[inds]
    source.data['image']=imageRawSelect
    numpy.savetxt('origImage.txt',imageRaw)
    numpy.savetxt('selImage.txt',imageRawSelect)
    numpy.savetxt('selInds.txt',inds)
    
curdoc().add_root(HBox(children=[inputs,figs],width=800))
#p.on_change('selected',updaeSelection)
