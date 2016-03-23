import numpy as np
from bokeh.plotting import Figure, hplot, vplot
#https://github.com/bokeh/bokeh/issues/3531 for Figure vs. figure
from bokeh.io import curdoc
# the following for the alternate form of page lay-out
from bokeh.models import HBox, VBox, ColumnDataSource
from bokeh.models.widgets import Slider, Button

# set up params for basic CRF w/ baseline offset (provided by presence of flankers)
contrast = np.arange(0,1,.01)

# interactive tools
redrawButton = Button(label="New Sample", type="success")
offsetSlider = Slider(title="baseline (offset)", value=0.3, start=0.0, end=0.5)
alphaSlider = Slider(title="alpha (R = C^alpha)", value=0.4, start=0.0, end=2.0)
CNRslider = Slider(title="CNR", value=2.0, start=0.0, end=5.0)
nREPslider = Slider(title="n subj", value=7, start=0, end=50, step=1)
    
p1 = Figure(plot_width=300,
               plot_height=300,
               title='CNR = %2.1f' %CNRslider.value, title_text_font_size='14pt',
               x_range=[0.0, 1.0],
               y_range=[-0.5, 1.5])

p2 = Figure(plot_width=300,
               plot_height=300,
               title='simulated results (n=%d)' %nREPslider.value, title_text_font_size='14pt',
               x_range=[0.05, 0.35],
               y_range=[-0.2, 1.0])
offset = offsetSlider.value
alpha = alphaSlider.value
CNR = CNRslider.value
nRep = int(nREPslider.value)

# set up everything we want to plot as column data sources
response = ColumnDataSource(data=dict(x=contrast,y=contrast**alpha + offset))
response_plus_noise = ColumnDataSource(data=dict(x=contrast,y=contrast**alpha + offset + (np.random.random(contrast.shape)-0.5)/CNR))
baseline = ColumnDataSource(data=dict(x=contrast,y=offset*np.ones(contrast.shape)))
baseline_plus_noise = ColumnDataSource(data=dict(x=contrast,y=offset+(np.random.random(contrast.shape)-0.5)/CNR))

# sim some data
data = np.zeros([nRep,3])
for iRep in range(nRep):
    stim = offset + np.array([0.08,0.16,0.32])**alpha + (np.random.random((1,3))-0.5)/CNR
    fonly = offset + (np.random.random()-0.5)/CNR
    data[iRep,:] = stim - fonly

p1.line('x','y',source=baseline, line_dash=[8,8], color = 'green')
p1.line('x','y',source=baseline_plus_noise, alpha=0.6, color='green')
p1.line('x','y',source=response, alpha=0.6, color='black')
p1.line('x','y',source=response_plus_noise, alpha=0.6, color='black')
p1.title = 'CNR = %2.1f' %CNR

p2.line([0,1], [0,0], line_dash=[8,8], color = 'green')
data_all = []
data_eb = []

for iC,c in enumerate([0.08,0.16,0.32]):
    data_all.append(ColumnDataSource(data=dict(x=c*np.ones([nRep]),y=data[:,iC])))
    p2.circle('x', 'y', source=data_all[iC], color='red', fill_alpha=0.3, line_alpha=0.3)
data_means = ColumnDataSource(data=dict(x=np.array([0.08,0.16,0.32]),y=np.mean(data,axis=0)))
p2.line('x', 'y', source=data_means, color='red')
for iC,c in enumerate([0.08,0.16,0.32]):
    data_eb.append(ColumnDataSource(data=dict(x=[c,c],y=np.mean(data[:,iC]) + np.std(data[:,iC])/np.sqrt(nRep)*np.array([-1,1]))))    
    p2.line('x', 'y', source=data_eb[iC], color='red')

curdoc().add_root(hplot(vplot(CNRslider,offsetSlider,nREPslider,alphaSlider,redrawButton),p1,p2)) #vform, from bokeh.io also works in there

## Alternate method of formatting page:
#inputs=VBox(children=[redrawButton,CNRslider])
#figs=HBox(children=[p1,p2])
#curdoc().add_root(HBox(children=[inputs,figs],width=800))

def update(attrname,old,new):
    CNR = CNRslider.value
    nRep = int(nREPslider.value)
    alpha = alphaSlider.value
    offset = offsetSlider.value
    response.data['y'] = contrast**alpha + offset
    response_plus_noise.data['y'] = contrast**alpha + offset + (np.random.random(contrast.shape)-0.5)/CNR
    baseline.data['y'] = offset*np.ones(contrast.shape)
    baseline_plus_noise.data['y'] = offset+(np.random.random(contrast.shape)-0.5)/CNR 
    p1.title = 'CNR = %2.1f' %CNR
    # sim some data
    data = np.zeros([nRep,3])
    for iRep in range(nRep):
        stim = offset + np.array([0.08,0.16,0.32])**alpha + (np.random.random((1,3))-0.5)/CNR
        fonly = offset + (np.random.random()-0.5)/CNR
        data[iRep,:] = stim - fonly
    # and push to plots
    for iC,c in enumerate([0.08,0.16,0.32]):
        data_all[iC].data['y'] = data[:,iC]
        data_all[iC].data['x'] = c*np.ones([nRep])
    data_means.data['y'] = np.mean(data,axis=0)
    for iC,c in enumerate([0.08,0.16,0.32]):
        data_eb[iC].data['y'] = np.mean(data[:,iC]) + np.std(data[:,iC])/np.sqrt(nRep)*np.array([-1,1])  

CNRslider.on_change('value',update)
nREPslider.on_change('value',update)
alphaSlider.on_change('value',update)
offsetSlider.on_change('value',update)
redrawButton.on_change('clicks',update)

    


