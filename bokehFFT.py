# make a simple 2D FFT filter interactive with bokeh
#following demo sliders.py and CAO code

import numpy
from bokeh.models import BoxSelectTool, LassoSelectTool, ColumnDataSource, HBox, VBoxForm
from bokeh.plotting import Figure
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc

#get data ... in this case the raw image
#how to get the image?
imageFile=''
imageRaw=Image.open(f)
#take FFT of image

#set up the plot (matplotlib imshow.....?)
#need size to be dynamic? need ranges to be right
outPlot=Figure(plot_height=400, plot_width=400, title="filtered image",
               tools="crosshair, pan, reset, resize, save, wheel_zoom",
               x_range=[0,1], y_range=[0,1])

#http://bokeh.pydata.org/en/0.10.0/docs/gallery/image.html
outPlot.image(image=filteredImage,x=[0],y=[0],palette="Greys")#need dw and dh? 
#would be awesome to have a custom palette that maps orientation to color like VV


#set up the slider widgets