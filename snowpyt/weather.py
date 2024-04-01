"""
Function to plot weather in a vizualisation relevant to identify specific weather events (melt, precip, wind) to snow pack metamosphism
S. Filhol, march 2024

See Github issue: https://github.com/ArcticSnow/snowpyt/issues/6

- function to plot weather record
	- temperature, blue below freezing, red abod (add fill in)
	- wind fill in when above 6 m/s

- try to make the plot a bokeh plot for interactivity
"""


import pandas as pd 
import matplotlib.pyplot as plt  
import numpy as np  



def plot_weather_history(df, resampling='12H', var_to_plot=['t', 'ws', 'sd']):
    """ Plot weather history in light of snow metamorphism history
    
    Args:
        df (dataframe): Dataframe with timeseries 
                            temperature (degC): 't'
                            wind speed (m/s): 'ws'
                            snowdepth (cm): 'sd' 
        resampling (str, optional): Resampling to apply to the timeseries, assuming hourly input
        var_to_plot (list, optional): List of variable to plot in a given order.
    """
    # resample timseries to coarser time resolution
    if resampling is not None:
        df_res = df.resample(resampling).mean()
    else:
        df_res = df
    
    def ax_plot_temp(df_sub, ax):
        df_sub['t_below_freezing'] = df_sub.t * (df_sub.t <=0)

        df_sub.t.plot(ax=ax)
        ax.fill_between(df_sub.index, df_sub.t_below_freezing, df_sub.t, color='r')
        ax.set_ylabel('Temperature\n[$^{o}C$]')
        
        return ax
        
        
    def ax_plot_ws(df_sub, ax):
        
        # curve used for shading
        df_sub['t_below_freezing'] = df_sub.t * (df_sub.t <=0)
        df_sub['ws_above_drifting'] = df_sub.ws * ((df_sub.ws >=6)) 
        df_sub['ws_below_drifting'] = 6
        df_sub.ws_below_drifting.loc[df_sub.ws<=6] = df_sub.ws.loc[df_sub.ws<=6]
        
        df_sub.ws.plot(ax=ax)
        #df_sub.ws_below_drifting.plot(ax=ax[1])
        ax.fill_between(df_sub.index, df_sub.ws_below_drifting, df_sub.ws, color='g')
        ax.set_ylabel('Wind speed\n[$m.s^{-1}$]')
        
        return ax
    
    def ax_plot_sd(df_sub, ax):
        df_sub.sd.plot(ax=ax, label=None)
        ax.fill_between(df_sub.index, 0, df_sub.sd.max()*1.2, where=df_sub.ws>=6, color='g', alpha=0.2, edgecolor=None, label='$P_{drifting}>0$')
        ax.fill_between(df_sub.index, 0, df_sub.sd.max()*1.2, where=df_sub.t>=0, color='r', alpha=0.2, edgecolor=None, label='melt')
        ax.legend()
        ax.set_ylabel('Snow depth\n[cm]')
        
        return ax
        

    fig, ax = plt.subplots(len(var_to_plot),1, sharex=True, figsize=(12,8))
    
    for i, var in enumerate(var_to_plot):
        if var == 't':
            ax[i] = ax_plot_temp(df_res, ax[i])
        elif var == 'ws':
            ax[i] = ax_plot_ws(df_res, ax[i])
        elif var == 'sd':
            ax[i] = ax_plot_sd(df_res, ax[i])
        elif var not in ['t', 'ws', 'sd']:
            raise Error(f'--> {var} is not available for plotting')
            
    plt.tight_layout()





