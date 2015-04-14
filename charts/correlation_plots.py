__author__ = 'alfiya'
from collections import OrderedDict

import numpy as np

from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource


def correlation_plot(corr, output_filename):
    """
    Creates interactive plot from correlation matrix
    :param corr: data frame with correlation matrix made from pd.DataFrame.corr()
    :param output_filename: output html filename for plot
    """
    names = list(corr.columns.values)
    xname = []
    yname = []
    color = []
    alpha = []
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            xname.append(n1)
            yname.append(n2)

            a = min(corr.iloc[i,j], 0.9) + 0.1
            alpha.append(a)

            if corr.iloc[i,j] > 0:
                color.append("orange")
            elif corr.iloc[i,j] < 0:
                color.append('green')
            else:
                color.append('lightgrey')


    source = ColumnDataSource(
        data=dict(
            xname=xname,
            yname=yname,
            colors=color,
            alphas=alpha,
            corr=corr.values.flatten(),
        )
    )

    output_file(output_filename)

    p = figure(title="Correlation matrix",
        x_axis_location="above", tools="resize,hover,save",
        x_range=list(reversed(names)), y_range=names)
    p.plot_width = 1000
    p.plot_height = 1000

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
         color='colors', alpha='alphas', line_color=None)

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('names', '@yname, @xname'),
        ('corr', '@corr'),
    ])

    show(p)      # show the plot
