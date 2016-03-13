# make a simple 2D FFT filter interactive with bokeh
#following demo sliders.py and CAO code

import numpy
from bokeh.models import BoxSelectTool, LassoSelectTool, ColumnDataSource, HBox, VBoxForm
from bokeh.plotting import Figure
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc
from scipy import misc
from bokeh.io import gridplot, show

#get data ... in this case the raw image
#how to get the image?
imageFile='P1040376.JPG'
imageRaw=misc.imread(imageFile,1)

#take FFT of image
imageFFT=numpy.fft.fft2(imageRaw)
imageFFT=numpy.fft.fftshift(imageFFT)

#set up an output grid that covers the appropriate fourier domain
x,y=numpy.meshgrid(range(imageFFT.shape[1]),range(imageFFT.shape[0]),indexing='xy')
x=x-imageFFT.shape[1]/2
y=y-imageFFT.shape[0]/2
r=numpy.sqrt(x*x+y*y) #pixels
theta=numpy.arctan2(x,y)


#apply the default filter to have a starting point
sf=1.0
bwSF=1.0
ori=(numpy.pi/180.0)*45.0
bwOri=(numpy.pi/180.0)*1.0
#here, make the SF filter
fmin=sf-bwSF/2.0
fmax=sf+bwSF/2.0
donutFilter=numpy.exp(-( (r-fmin )**2 / (2*fmax*fmax) ))
omax=ori+bwOri/2.0
omin=ori-bwOri/2.0

#first lobe of filter
t1=numpy.angle(numpy.exp(complex(0,1)*(theta-omin))) #center it
t1=numpy.exp(-( t1**2/(2*omax*omax)  )) #put a gaussian around it
#first lobe of filter on the other side of k-space
t2=numpy.angle(numpy.exp(complex(0,1)*(theta-omin-numpy.pi))) #center it
t2=numpy.exp(-( t2**2/(2*omax*omax)  )) #put a gaussian around it
#unite them all for the actual filter
customFilter=sf*(t1+t2)

#apply it to the FFT'd image
filteredFFT=imageFFT*customFilter
#reconstruct the filtered image
filteredImage=numpy.fft.ifft2(numpy.fft.fftshift(filteredFFT))


#set up the plots 
#need 4x4 grid for input image, FFT of input, filter itself (with sliders), and filtered image
#need size to be dynamic? need ranges to be right
inputPlot=Figure(plot_height=400, plot_width=400, title="input image",
               tools="crosshair, pan, reset, resize, save, wheel_zoom",
               x_range=[0,1], y_range=[0,1])

#http://bokeh.pydata.org/en/0.10.0/docs/gallery/image.html
inputPlot.image(image=[imageRaw],x=0,y=0,palette="Greys9")#need dw and dh? 
#would be awesome to have a custom palette that maps orientation to color like VV

inputFFTPlot=Figure(plot_height=400, plot_width=400, title="FFT of input image",
               x_range=[0,1], y_range=[0,1])
inputFFTPlot.image(image=[imageFFT],x=0,y=0,dw=10,dh=10,palette="Greys9")#need dw and dh? 

filterPlot=Figure(plot_height=400, plot_width=400, title="current filter",
               x_range=[0,1], y_range=[0,1])
filterPlot.image(image=[customFilter],x=0,y=0,palette="Spectral11")#need dw and dh? 

outputPlot=Figure(plot_height=400, plot_width=400, title="filtered image",
               x_range=[0,1], y_range=[0,1])
outputPlot.image(image=[filteredImage],x=0,y=0,palette="Greys9")#need dw and dh? 

#http://bokeh.pydata.org/en/0.10.0/docs/user_guide/layout.html
p=gridplot([ [inputPlot,inputFFTPlot], [filterPlot,outputPlot] ])

#set up the slider widgets
text = TextInput(title="title", value="Put your title here")
spatialFreq = Slider(title="Spatial Frequency (cycles/image)", value=1.0, start=0.0, end=10.0)
bandwidthSF = Slider(title ="spatial frequency bandwidth",value=1.0,start=0.1,end=5.0)
orientation = Slider(title="Orientation (deg)", value=45.0, start=0.0, end =360.0)
bandwidthOri = Slider(title ="orientation bandwidth",value=1.0,start=0.1,end=5.0)

#set up callbacks
#one for each input (text, sf, ori) 

#define the action  mechanism
def updateText(attrname, old, new):
    outputPlot.title=text.value
#initiate action if needed
text.on_change('value',updateText)

def updateFilter(attrname, old, new):
    #get the slider values
    sf=spatialFreq.value
    bwSF=bandwidthSF.value
    ori=(numpy.pi/180.0)*orientation.value
    bwOri=(numpy.pi/180.0)*bandwidthOri.value
    #here, make the SF filter
    fmin=sf-bwSF/2.0
    fmax=sf+bwSF/2.0
    donutFilter=numpy.exp(-( (r-fmin )**2 / (2*fmax*fmax) ))
    omax=ori+bwOri/2.0
    omin=ori-bwOri/2.0
    
    #first lobe of filter
    t1=numpy.angle(numpy.exp(complex(0,1)*(theta-omin))) #center it
    t1=numpy.exp(-( t1**2/(2*omax*omax)  )) #put a gaussian around it
    #first lobe of filter on the other side of k-space
    t2=numpy.angle(numpy.exp(complex(0,1)*(theta-omin-numpy.pi))) #center it
    t2=numpy.exp(-( t2**2/(2*omax*omax)  )) #put a gaussian around it
    #unite them all for the actual filter
    customFilter=sf*(t1+t2)
    
    #apply it to the FFT'd image
    filteredFFT=imageFFT*customFilter
    #reconstruct the filtered image
    filteredImage=numpy.fft.ifft2(numpy.fft.fftshift(filteredFFT))
    
for widget in [spatialFreq,bandwidthSF,orientation,bandwidthOri]:
    widget.on_change('value',updateFilter)
    
    
inputs = VBoxForm(children=[text,spatialFreq,bandwidthSF,orientation,bandwidthOri])
#curdoc().add_root(HBox(children=[input,plot]))
    
