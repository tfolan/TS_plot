# TS_plot

TS_plot is a generalized time series plotting function designed to quickly and accurately convey a large amount of information through professional-quality plots. It takes a Pandas' dataframe, a string (plot title), and a dictionary.


### Signature

ts_plot(df, title, params)

Params
* start date
    * a datetime object
    * sets the date from which decades are counted
    * slices the dataframe and removes earlier dates
* columns
    * list of strings
    * consisting of columns to be plotted
* units
    * list of strings
    * consisting of the units for each plotted column
* annual threshold:
    * the minimium number of records needed to calculate an annual average
* decade threshold:
    * the minumium number of records needed to calculate a decadal average



See Example.ipynb for applied examples.
