from bokeh.plotting import Figure, show
from scipy import misc
from bokeh.io import curdoc
from bokeh.models import HBox

imageFile='head.png'
imageRaw=misc.imread(imageFile,1)

#inputPlot=Figure(plot_height=400, plot_width=400, title="input image",
#               tools="crosshair, pan, reset, resize, save, wheel_zoom",
#               x_range=[0,1], y_range=[0,1])
#inputPlot.image(image=[imageRaw],x=0,y=0,palette="Greys9")#need dw and dh? 
#curdoc().add_root(HBox(children=[inputPlot],width=800))

p = Figure(x_range=[0, 10], y_range=[0, 10])
p.image(image=[imageRaw], x=[0], y=[0], dw=[10], dh=[10], palette="Greys9")
curdoc().add_root(HBox(children=[p],width=800))
