from bokeh.models import CustomJS, ColumnDataSource, BoxSelectTool, Range1d, Rect
from bokeh.plotting import figure, output_file, show, hplot

output_file("boxselecttool_callback.html")

s1 = ColumnDataSource(data=dict(x=[0.5], y=[0.5], width=[.3], height=[.3]))
s2 = ColumnDataSource(data=dict(x=s1.data['x'], y=s1.data['y']))


callback = CustomJS(args=dict(s1=s1,s2=s2), code="""
        // get data source from Callback args
        var d1 = s1.get('data');
        var d2 = s2.get('data');

        /// get BoxSelectTool dimensions from cb_data parameter of Callback
        var geometry = cb_data['geometry'];

        /// calculate Rect attributes
        var width = geometry['x1'] - geometry['x0'];
        var height = geometry['y1'] - geometry['y0'];
        var x = geometry['x0'] + width/2;
        var y = geometry['y0'] + height/2;

        /// update data source with new Rect attributes
        d1['x'].push(x);
        d1['y'].push(y);
        d1['width'].push(width);
        d1['height'].push(height);
        
        // try for other source, too
        d2['x'].push(x);
        d2['y'].push(y);

        // trigger update of data source
        s1.trigger('change');
        s2.trigger('change');
    """)

box_select = BoxSelectTool(callback=callback)

p1 = figure(plot_width=300,
           plot_height=300,
           tools=[box_select],
           title='Select Here',
           x_range=Range1d(start=0.0, end=1.0),
           y_range=Range1d(start=0.0, end=1.0))
           
p2 = figure(plot_width=300,
           plot_height=300,
           title='Plot Here',
           x_range=Range1d(start=0.0, end=1.0),
           y_range=Range1d(start=0.0, end=1.0))
           
layout = hplot(p1, p2)

rect = Rect(x='x',
            y='y',
            width='width',
            height='height',
            fill_alpha=0.3,
            fill_color='#009933')

p1.add_glyph(s1, rect, selection_glyph=rect, nonselection_glyph=rect)
p2.circle('x', 'y', source=s2, alpha=0.6, size=20)

show(layout)