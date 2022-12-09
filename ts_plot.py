import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ts_plot(df, name, params): 
  
    # Adds start date to dataframe.
    # The start date sets the date from which decades are counted.
    # The start date also filters the dataframe by slicing the dataframe from that date.
    if params['start date'] not in df.index.values:
        df = pd.concat([df, pd.DataFrame( index = [params['start date']])])
    df.sort_index(inplace = True)
    df = df[params['start date']: ]
    
    idx = 0 # column index
    line_labels = [] # array for plot legend 
    dict_keys = params['columns']
    
    # Determine how many subplot columns are needed
    if (len(params['columns']) == 1):
        c = 1
    else:
        c = 2
    
    # defing the figure and axes
    fig, axes = plt.subplots(int(np.ceil(len(params['columns'])/2)), c, figsize=(16,12), squeeze = False)
    
    for i in range(int(np.ceil(len(params['columns'])/2))):
        for j in range(c): 
            daily_flag = False
            element = params['columns'][idx]
            unit = params['units'][idx]
            
            x = df.resample("10AS", closed = "left").count()
            x = x[x[element] > params['min decade records']]
            s_date_decade = x.index.min()
            e_date_decade = x.index.max()
            e_date_decade = e_date_decade.replace(year=e_date_decade.year + 9)

            x_ann = df.resample("1AS", closed = "left").count()
            x_ann = x_ann[x_ann[element] > params['min annual records']]
            s_date_ann = x_ann.index.min()
            e_date_ann = x_ann.index.max()
            e_date_ann = e_date_ann.replace(year=e_date_ann.year, month = 12, day = 31)

            df_ann = df[s_date_ann : e_date_ann]
            df_dec = df[s_date_decade : e_date_decade]

            df_ann = df_ann.resample('1AS').mean()

            df_avg = df_ann[dict_keys].mean()
            if (len(df_dec[element].resample('10AS').mean()) > 1):
                df_dec = df_dec.resample('10AS').mean()

            if (len(df_ann[element]) <= 1):
                axes[i][j].plot(df.index, df[element], color = "blue", label = "Daily")
                line_labels.append("Daily")
                daily_flag = True
            else:
                axes[i][j].plot(df_ann.index, df_ann[element], color = "lightgrey", label = "Annual")
                line_labels.append("Annual")
            if (len(df_dec) > 0):
                df_dec = pd.concat([df_dec, df_dec.loc[s_date_decade].to_frame().T.rename(index = {s_date_decade : s_date_decade.replace(year=s_date_decade.year - 10)})])
                df_dec.sort_index(inplace = True)
                df_dec.index = df_dec.index+ pd.DateOffset(years=10)
                axes[i][j].step(df_dec.index, df_dec[element], color = "black", lw = 3, label = "Decadal")
                line_labels.append("Decadal")
                axes[i][j].hlines(df_avg[element], df_ann.index.min(), df_ann.index.max(), linestyle="dashed", color = "grey", label = "Average")
                line_labels.append("Mean")

            # Removes duplicates from line_labels
            labels = list(dict.fromkeys(line_labels))

            # adds grid lines
            axes[i][j].grid(linestyle='-', linewidth=0.2)
            
            # Controls the y-axis based on the element's range
            # all values are negative
            if df_ann[element].min() < 0 and df_ann[element].max() < 0: 
                axes[i][j].set_ylim(df_ann[element].min() * 1.1, 0)
                if(daily_flag):
                    axes[i][j].set_ylim(df_[element].min() * 1.1, 0)
            # values are positive and negative
            if df_ann[element].min() < 0 and df_ann[element].max() > 0:
                axes[i][j].set_ylim(df_ann[element].min() * 1.1, df_ann[element].max() * 1.1)
                if(daily_flag):
                    axes[i][j].set_ylim(df[element].max() * 1.1, df[element].max() * 1.1)
                
            # all values are positive    
            if df_ann[element].min() > 0 and df_ann[element].max() > 0:
                axes[i][j].set_ylim(df_ann[element].max() * -0.05, df_ann[element].max() * 1.1)
                if(daily_flag):
                    axes[i][j].set_ylim(df[element].max() * -0.05, df[element].max() * 1.1)
                
            axes[i][j].set_title(element.upper(), fontsize = 20)
            axes[i][j].set_ylabel(unit, fontsize = 16)
            if ((idx + 1) < len(params['columns'])):
                idx = idx + 1
    if ((c != 1) and (len(params['columns'])%2 != 0)):
        axes.flat[-1].set_visible(False) # removes last plot


    fig.legend(
        labels=labels,
        loc="center right", 
        borderaxespad=0.1,  
    )

    plt.subplots_adjust(right=.87)
    fig.suptitle(name, fontsize=24)