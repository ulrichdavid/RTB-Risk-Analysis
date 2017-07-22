# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 00:48:27 2017

@author: dulrich@kargo.com
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# graphing tools
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

# plotly
import plotly
plotly.offline.init_notebook_mode()
import plotly.graph_objs as go
from plotly.graph_objs import *

class distribution():
    def __init__(self, file="apd_distribution.csv", graph=True, graph_type="pie", category="TET"):
        df = pd.read_csv(file)
        
        columns = [] # distribution
        portion = [] # instances
        prices = [] # prices

        # get dataframe in properly order        
        sorted_df = df.reindex([0,1,6,3,4,5,2])
        for index, row in sorted_df.iterrows():
            columns.append(row["DISTRIBUTION"])
            prices.append(row["TOTAL_PRICE"])
            portion.append(row["INSTANCES"])
        
        if graph:
            if graph_type == "hist":
                self.histogram(columns, prices, category)
            else:
                self.pie(columns, portion, category)
        
    def histogram(self, column_names, values, cat):
        data = [go.Bar(x=column_names, y=values, name="Prices", marker=dict(color='rgb(59,178,3)'))]
        graph_title = "RTB Revenue by " + cat
        layout = go.Layout(
            title=graph_title,
            xaxis=dict(
                title="Total Exposure Time (MS)",
                tickfont=dict(
                    size=14,
                    color='rgb(107, 107, 107)'
                )
            ),
            yaxis=dict(
                title='Total Revenue (USD)',
                titlefont=dict(
                    size=16,
                    color='rgb(107, 107, 107)'
                ),
                tickfont=dict(
                    size=14,
                    color='rgb(107, 107, 107)'
                )
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1
        )
        fig = go.Figure(data=data, layout = layout)
        
        # save graph to html file
        plotly.offline.plot(fig, filename="tet dist.html") 
        
    def pie(self, column_names, values, cat):
        graph_title = "Network Distribution by " + cat + " (MS)"
        fig = {
          "data": [
            {
              "values": values,
              "labels": column_names,
              "hoverinfo":"label+percent",
              "type": "pie"
            }],
          "layout": {
                "title":graph_title
            }
        }        
        plotly.offline.plot(fig, filename="tet pie.html")