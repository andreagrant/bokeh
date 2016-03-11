#making a little server version
#http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server-applications

import numpy

from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, vplot

#create plot without any data but define the ranges
myPlot = figure(x_range=(0,100), y_range=(0,100), toolbar_location=None)
#configure the plot stylings
myPlot.border_fill_color = 'black'
myPlot.background_fill_color = 'green'
myPlot.outline_line_color = None
myPlot.grid.grid_line_color=None

#add a text renderer .... still don't have any data!
textRend = myPlot.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
                       text_baseline="middle", text_align="center")
                       
i=0

dataSource= textRend.data_source

#create a callback that will add a number in a random location
#what is a callback? an action that happens when i interact?
def callback():
    global i
    dataSource.data['x'].append(numpy.random.random()*70+15)
    dataSource.data['y'].append(numpy.random.random()*70+15)
    dataSource.data['text_color'].append(RdYlBu3[i%3])
    dataSource.data['text'].append(str(i))
    dataSource.trigger('data',dataSource.data,dataSource.data)
    i=i+1
    
#add a button widget and configure it with the callbac---ahh, so the callback 
    #is the action that happens when I click on the button!
button = Button(label="press me!")
button.on_click(callback)

#put the button and plit in a layou and add it to the document
curdoc().add_root(vplot(button,myPlot))
                         