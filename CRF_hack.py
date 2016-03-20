import numpy as np
from bokeh.plotting import Figure, hplot, vplot
#https://github.com/bokeh/bokeh/issues/3531 for Figure vs. figure
from bokeh.io import curdoc
# the following for the alternate form of page lay-out
#from bokeh.models import HBox, VBox
from bokeh.models.widgets import Slider, Button
from bokeh.models import ColumnDataSource
from bokeh.models.glyphs import MultiLine
# set up params for basic CRF w/ baseline offset (provided by presence of flankers)
contrast = np.arange(0,1,.01)
alpha= 0.6
baseline = 0.3

    
# interactive tools
nRep = 7 # eventually turn this into an option
redrawButton = Button(label="New Sample", type="success")
CNRslider = Slider(title="CNR", value=1.0, start=0.0, end=2.0)
 



#set up staring data set
CNR=CNRslider.value
response = contrast**alpha + baseline
response_plus_noise = response + (np.random.random(contrast.shape)-0.5)/CNR
# sim some data
data = np.zeros([nRep,3])
for iRep in range(nRep):
    stim = baseline + np.array([0.08,0.16,0.32])**alpha + (np.random.random((1,3))-0.5)/CNR
    fonly = baseline + np.random.random()-0.5
    data[iRep,:] = stim - fonly
thing=[(np.random.random(contrast.shape)-0.5)/CNR+baseline]
#set up data object to hand to the plot
sourceLine=ColumnDataSource(dict(
    xs=[[0,1],contrast,contrast,contrast],
    ys=[[baseline,baseline],thing,response, response_plus_noise]
    ))   
p1 = Figure(plot_width=300,
               plot_height=300,
               title='CNR = %2.1f' %CNRslider.value, title_text_font_size='14pt',
               x_range=[0.0, 1.0],
               y_range=[-0.5, 1.5])


lineGlyph=MultiLine(xs="xs", ys="ys")
p1.add_glyph(sourceLine,lineGlyph)
p2 = Figure(plot_width=300,
               plot_height=300,
               title='simulated results (n=%d)' %nRep, title_text_font_size='14pt',
               x_range=[0.05, 0.35],
               y_range=[-0.2, 1.0])

curdoc().add_root(hplot(vplot(CNRslider,redrawButton),p1,p2)) #vform, from bokeh.io also works in there

## Alternate method of formatting page:
#inputs=VBox(children=[redrawButton,CNRslider])
#figs=HBox(children=[p1,p2])
#curdoc().add_root(HBox(children=[inputs,figs],width=800))

def update(attrname,old,new):
    CNR = CNRslider.value
    print "my CNR: ", CNR
    response = contrast**alpha + baseline
    response_plus_noise = response + (np.random.random(contrast.shape)-0.5)/CNR
    # sim some data
    data = np.zeros([nRep,3])
    for iRep in range(nRep):
        stim = baseline + np.array([0.08,0.16,0.32])**alpha + (np.random.random((1,3))-0.5)/CNR
        fonly = baseline + np.random.random()-0.5
        data[iRep,:] = stim - fonly
       
    #p1.line([0,1], [baseline,baseline], line_dash=[8,8], color = 'green')
    #p1.line(contrast, (np.random.random(contrast.shape)-0.5)/CNR+baseline, alpha=0.6, color='green')
    #p1.line(contrast,response, alpha=0.6, color='black')
    #p1.line(contrast,response_plus_noise, alpha=0.6, color='black')
    sourceLine.data['xs']=[[0,1],contrast,contrast,contrast]
    sourceLine.data['ys']=[[baseline,baseline],[(np.random.random(contrast.shape)-0.5)/CNR+baseline],response, response_plus_noise]
 

    p1.title = 'CNR = %2.1f' %CNR

    p2.line([0,1], [0,0], line_dash=[8,8], color = 'green')
    for iC,c in enumerate([0.08,0.16,0.32]):
        p2.circle(c*np.ones([nRep]), data[:,iC], color='red', fill_alpha=0.3, line_alpha=0.3)
    for iC,c in enumerate([0.08,0.16,0.32]):
        p2.circle(c, np.mean(data[:,iC]), color='red')
        p2.line([c,c], np.mean(data[:,iC]) + np.std(data[:,iC])/np.sqrt(nRep)*np.array([-1,1]), color='red')
    
CNRslider.on_change('value',update)

    


