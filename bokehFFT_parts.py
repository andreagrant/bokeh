from bokeh.plotting import Figure, show
from scipy import misc
from bokeh.io import curdoc
from bokeh.models import HBox, VBoxForm, VBox, ColumnDataSource, BoxSelectTool
import numpy
from bokeh.models.widgets import Slider

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
r = numpy.sqrt(x*x+y*y) # units are pixels
theta = numpy.arctan2(x,y)
fband=[16,16]
SF = numpy.exp(-((r-fband[0])**2/(2.0*fband[1]*fband[1])))  
#SF=numpy.ones(r.shape)    

#create a giant array of inivisble circles to be selected, thus giving me coordinates in the image
circleSource=ColumnDataSource(data={'x':[numpy.ravel(x0)*10.0/imageFFT.shape[1]],'y':[numpy.ravel(y0)*10.0/imageFFT.shape[0]]})
p.circle('x','y',size=0.1,color="navy",alpha=0.5,source=circleSource)
p.select(BoxSelectTool).select_every_mousemove=False


    
#ori=45*(numpy.pi/180.0)
#oband=[ori*0.95, ori*1.05]
oband=[numpy.pi/4.0, numpy.pi/8.0]
t1 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]))) # center it
t1 = numpy.exp(-(t1**2/(2*oband[1]*oband[1]))) # and put a gaussian around it
# make the 2nd lobe on the other side of k-space
t2 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]-numpy.pi)))
t2 = numpy.exp(-(t2**2/(2*oband[1]*oband[1])))
customFilter = SF*(t1 + t2)
#numpy.savetxt('bokehCF.txt',customFilter)
source2 = ColumnDataSource(data={'image': [customFilter]})

p2 = Figure(x_range=[0, 10], y_range=[0, 10],plot_width=400,plot_height=400)
#p2.image(image=[customFilter], x=[0], y=[0], dw=[10], dh=[10])
p2.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source2,palette="Spectral11")


filteredFFT = imageFFT*customFilter
filteredImage = numpy.fft.ifft2(numpy.fft.fftshift(filteredFFT))
filteredImageReal=numpy.real(filteredImage)

source3 = ColumnDataSource(data={'image': [filteredImageReal]})

p3 = Figure(x_range=[0, 10], y_range=[0, 10],plot_width=400,plot_height=400)
#p2.image(image=[customFilter], x=[0], y=[0], dw=[10], dh=[10])
p3.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source3)

p.axis.visible=None
p2.axis.visible=None
p3.axis.visible=None


orientation = Slider(title="Orientation (deg)", value=45.0, start=0.0, end =360.0)
orientationWidth = Slider(title="Orientation bandwidth (deg)", value=22.5, start=0.0, end =45.0)
spatialFreq = Slider(title="Spatial frequency (cycles/image)", value=16.0, start=0.0, end =64.0)
spatialFreqWidth = Slider(title="spatial frequency bandwidth", value=0.0, start=0.0, end =16.0)
inputs=VBox(children=[orientation,orientationWidth,spatialFreq, spatialFreqWidth])
figs=HBox(children=[p,p2,p3])

def update(attrname,old,new):
    ori=orientation.value*(numpy.pi/180.0)
    oriWidth=orientationWidth.value*(numpy.pi/180.0)
    oband=[ori, ori-oriWidth]
    #oband=[ori, numpy.pi/8]
    t1 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]))) # center it
    t1 = numpy.exp(-(t1**2/(2*oband[1]*oband[1]))) # and put a gaussian around it
    # make the 2nd lobe on the other side of k-space
    t2 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]-numpy.pi)))
    t2 = numpy.exp(-(t2**2/(2*oband[1]*oband[1])))

    thisSF=spatialFreq.value
    sfWidth=spatialFreqWidth.value
    fband=[thisSF,thisSF-sfWidth]
    SF = numpy.exp(-((r-fband[0])**2/(2.0*fband[1]*fband[1])))  

    customFilter = SF*(t1 + t2)
    source2.data['image'] =customFilter
    #p2.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source2,palette="Spectral11")
    filteredFFT = imageFFT*customFilter
    filteredImage = numpy.fft.ifft2(numpy.fft.fftshift(filteredFFT))
    filteredImageReal=numpy.real(filteredImage)
    source3.data['image']=filteredImageReal
    #p3.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source3)
    thisTitle="Ori: %2.1f [%2.1f, %2.1f], SF: %2.1f, %2.1f"%(orientation.value,oband[0]*180/numpy.pi,
                oband[1]*180/numpy.pi,thisSF, sfWidth)
    p3.title=thisTitle
    
def updateSelection(attrname,old,new):
    inds=numpy.array(new)
    imageRawSelect = imageRaw[inds]
    source.data['image']=imageRawSelect
    numpy.savetxt('origImage.txt',imageRaw)
    numpy.savetxt('selImage.txt',imageRawSelect)
    numpy.savetxt('selInds.txt',inds)
    #p.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source)

    imageFFT = numpy.fft.fft2(imageRawSelect)
    imageFFT=numpy.fft.fftshift(imageFFT)
    x,y=numpy.meshgrid(range(imageFFT.shape[1]),range(imageFFT.shape[0]),indexing='xy')
    x = x - imageFFT.shape[1]/2
    y = y - imageFFT.shape[0]/2
    r = numpy.sqrt(x*x+y*y) # units are pixels
    
    ori=orientation.value*(numpy.pi/180.0)
    oriWidth=orientationWidth.value*(numpy.pi/180.0)
    oband=[ori, ori-oriWidth]
    #oband=[ori, numpy.pi/8]
    t1 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]))) # center it
    t1 = numpy.exp(-(t1**2/(2*oband[1]*oband[1]))) # and put a gaussian around it
    # make the 2nd lobe on the other side of k-space
    t2 = numpy.angle(numpy.exp(complex(0,1)*(theta-oband[0]-numpy.pi)))
    t2 = numpy.exp(-(t2**2/(2*oband[1]*oband[1])))

    thisSF=spatialFreq.value
    sfWidth=spatialFreqWidth.value
    fband=[thisSF,thisSF-sfWidth]
    SF = numpy.exp(-((r-fband[0])**2/(2.0*fband[1]*fband[1])))  

    customFilter = SF*(t1 + t2)
    source2.data['image']=customFilter
    #p2.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source2,palette="Spectral11")
    filteredFFT = imageFFT*customFilter
    filteredImage = numpy.fft.ifft2(numpy.fft.fftshift(filteredFFT))
    filteredImageReal=numpy.real(filteredImage)
    source3.data['image']=filteredImageReal
    #p3.image(image="image", x=[0], y=[0], dw=[10], dh=[10],source=source3)
    thisTitle="Ori: %2.1f [%2.1f, %2.1f], SF: %2.1f, %2.1f"%(orientation.value,oband[0]*180/numpy.pi,
                oband[1]*180/numpy.pi,thisSF, sfWidth)
    p3.title=thisTitle


for widget in [orientation,orientationWidth,spatialFreq, spatialFreqWidth]:
    widget.on_change('value',update)
#p.on_change('selected',updateSelection)
curdoc().add_root(HBox(children=[inputs,figs],width=800))
#circleSource.on_change('selected',updateSelection)