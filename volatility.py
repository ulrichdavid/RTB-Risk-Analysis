# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 00:07:54 2017

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

class vt():
    def __init__(self, file='domain_metrics_ytd.csv', graph=True, scale=False, kf="DOMAIN", kf_parse = False):
        df = pd.read_csv(file)
        self.vectors = {}

        df.fillna(0, inplace=True)
        
        if kf_parse:
            df[kf] = df['ARTICLE'].str.split('/').str.get(7)
        
        df['apd_cv'] = df['STD_APD'] / df['AVG_APD']
        df['tet_cv'] = df['STD_TET'] / df['AVG_TET']
        df['tui_cv'] = df['STD_TUI'] / df['AVG_TUI']
        df['inview_ratio'] = (df['FI_SUM'] / df['FI_COUNT']) * 100

        apd_min, apd_max = df['apd_cv'].min(), df['apd_cv'].max()
        tet_min, tet_max = df['tet_cv'].min(), df['tet_cv'].max()
        tui_min, tui_max = df['tui_cv'].min(), df['tui_cv'].max()
        
        if scale:
            for row in df.iterrows():
                self.vectors[row[1][kf]] = {}
                self.vectors[row[1][kf]].update({"apd":self.scale_unity(row[1]["apd_cv"], apd_min, apd_max)})
                self.vectors[row[1][kf]].update({"tet":self.scale_unity(row[1]["tet_cv"], tet_min, tet_max)})
                self.vectors[row[1][kf]].update({"tui":self.scale_unity(row[1]["tui_cv"], tui_min, tui_max)})
        else:            
            for row in df.iterrows():
                self.vectors[row[1][kf]] = {}
                self.vectors[row[1][kf]].update({"apd":row[1]["apd_cv"]})
                self.vectors[row[1][kf]].update({"tet":row[1]["tet_cv"]})
                self.vectors[row[1][kf]].update({"tui":row[1]["tui_cv"]})            
            
        graph_name = "Top 10 Publisher Metric Volatility"
        
        print(df.head())
        
        if graph:
            Graph().graph(vectors = self.vectors, file = graph_name)
        
    def scale_unity(self,value,v_min,v_max):
        avg = (v_min + v_max) / 2
        rng = (v_max - v_min) / 2
        return (value - avg) / rng

class creative_analysis():
    def __init__(self, file="middlebanner.csv", graph=True):
        df = pd.read_csv(file)
        pubs = []
        apd = []
        tet = []
        pod = []

        for row in df.iterrows():
            pubs.append(row[1]["PUBLISHER"])
            apd.append(row[1]["APD"])
            tet.append(row[1]["TET"])
            pod.append(row[1]["PERCENT_OF_DWELL"])
            
        if graph:
            # pod apd and tet
            apd = go.Bar(
                            x=pubs,
                            y=apd,
                            name="Active Page Dwell",
                            marker=dict(color='rgb(74,200,235)'))
            tet = go.Bar(
                            x=pubs,
                            y=tet,
                            name="Total Exposure Time",
                            marker=dict(color='rgb(202,238,94)'))  
            
            data = [apd, tet]
            layout = go.Layout(title='MiddleBanner Impact', xaxis=dict(tickangle=-45), barmode='group')
            fig = go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig, filename="Top Pub Interstitial Impact.html")  
            
            # plot POD
            
            pod = go.Bar(
                            x=pubs,
                            y=pod,
                            name="Active Page Dwell",
                            marker=dict(color='rgb(237,83,175)')) 
            
            data = [pod]
            layout = go.Layout(title='MiddleBanner Percent of Dwell', xaxis=dict(tickangle=-45), barmode='group')
            fig = go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig, filename="Top Pub MiddleBanner POD.html")              
            
class ft():
    def __init__(self, file="ytd_format_metrics.csv", graph=True):
        df = pd.read_csv(file)
        
        df['apd_cv'] = df['STD_APD'] / df['AVG_APD']
        df['tet_cv'] = df['STD_TET'] / df['AVG_TET']
        df['tui_cv'] = df['STD_TUI'] / df['AVG_TUI']
        df['inview_ratio'] = (df['FI_SUM'] / df['FI_COUNT']) * 100    

        formats = []
        apd = []
        tet = []
        tui = []

        for row in df.iterrows():
            formats.append(row[1]["FORMAT"])
            apd.append(row[1]["apd_cv"])
            tet.append(row[1]["tet_cv"])
            tui.append(row[1]["tui_cv"])
            
        if graph:
            apd = go.Bar(
                            x=formats,
                            y=apd,
                            name="Active Page Dwell",
                            marker=dict(color='rgb(74,200,235)'))
            tet = go.Bar(
                            x=formats,
                            y=tet,
                            name="Total Exposure Time",
                            marker=dict(color='rgb(202,238,94)'))
            tui = go.Bar(
                            x=formats,
                            y=tui,
                            name="Time Until Inview",
                            marker=dict(color='rgb(237,83,175)'))            
            data = [apd, tet, tui]
            layout = go.Layout(title='Format Volatility (Ordered by TET)', xaxis=dict(tickangle=-45), barmode='group')
            fig = go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig, filename="YTD Format Volatility.html")
            
class Graph():
    def graph(self, vectors, precision = 2, file = ""):
        x = [] # apd
        y = [] # tet
        z = [] # tui
        titles = [] # hover titles for Plotly
        
        # split vectors into X, Y, Z coordinates
        for key, value in vectors.items():
            x.append(value['apd'])
            y.append(value['tet'])
            z.append(value['tui'])
            titles.append(key)
        
        # scale values
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
               
        trace = go.Scatter3d(
            x = x, y = y, z = z,
            mode='markers',
            marker = dict(
                        color='rgba(97,123,155)', 
                        size = 12,
                        symbol='circle',
                        line = dict(color='rgb(22, 25, 32)', width=2),
                        opacity=0.9
                        ),
            text=titles
            )
        data = [trace]
        layout = go.Layout(
                            title=file,
                            scene = dict(
                            xaxis = dict(
                                 title="X: Active Page Dwell",
                                 backgroundcolor="rgb(74,200,235)",
                                 gridcolor="rgb(255, 255, 255)",
                                 showbackground=True,
                                 zerolinecolor="rgb(0,0, 0)",),
                            yaxis = dict(
                                title="Y: Total Exposure Time",
                                backgroundcolor="rgb(202,238,94)",
                                gridcolor="rgb(255, 255, 255)",
                                showbackground=True,
                                zerolinecolor="rgb(0,0, 0)"),
                            zaxis = dict(
                                title="Z: Time Until Inview",
                                backgroundcolor="rgb(237,83,175)",
                                gridcolor="rgb(255, 255, 255)",
                                showbackground=True,
                                zerolinecolor="rgb(0, 0, 0)",),),
                            width=1000,
                            margin=dict(
                            r=10, l=10,
                            b=10, t=50)
                          )                        
        fig = go.Figure(data=data, layout=layout)
        
        #plotly.offline.iplot(fig, filename='eta_scatter')
        plotly.offline.plot(fig, filename=file+".html")
