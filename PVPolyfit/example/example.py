# A functional example of the PVPolyfit on FSEC's VCAD dataset.
# This VCAD module utilizes IV trace parameters as its electrical outputs
# Power Max Power Point (Pmpp) is used as the module output

# import necessary packages
from PVPolyfit.core import pvpolyfit
import pandas as pd

# Gather data
train_df = pd.read_csv('.//example//example_data//train_df.csv', index_col = 'datetime')
test_df = pd.read_csv('.//example//example_data//test_df.csv', index_col = 'datetime')

print(train_df, test_df)
# Ensure datetime index is of correct form '%m/%d/%Y %I:%M:%S %p'
train_df.index = pd.to_datetime(train_df.index, format= '%m/%d/%Y %H:%M').strftime('%m/%d/%Y %I:%M:%S %p')
train_df.index = pd.to_datetime(train_df.index, format= '%m/%d/%Y %H:%M').strftime('%m/%d/%Y %I:%M:%S %p')

# Designate column name for each variable
# You can either type in the column name or just access it through df.columns
Y_tag = 'Pmpp'

# xs can be of any length
xs = ['Irradiance', 'AmbientTemperature']
I_tag = 'Impp'
ghi_tag = 'GHI'
cs_tag = 'clearsky_ghi' #PVLib's clearsky GHI output - see https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.location.Location.get_clearsky.html for an example
highest_num_clusters = 10 # Iterate from [1, highest_num_clusters] for Kmeans's k clusters
highest_degree = 10 # Iterate from [1, highest_degree] for algorithm to choose degree of lowest RMSE
Y_high_filter = 10000 # To be depricated: filter out Y values higher than Y_high_filter
min_count_per_day = 8 # minimum amount of values per day

'''
Introducing PVPolyfit

PARAMETERS:

    train_df: df
        holds training data with columns and index specified below
    test_df: df
        holds testing data with columns and index specified below
    Y_tag: str
        column name of output tag
    xs: list of str
        list of column names for ANY NUMBER of covariates
    ghi_tag: str
        column name of GHI input
    cs_tag: str
        column name of clearsky GHI generated by pvlib simulation (link below)

USER MUST INPUT DF's WITH FOLLOWING COLUMNS:

|       Description      |  Original Use Case         |   Model Purpose          |
|------------------------|----------------------------|--------------------------|
| Output,       Y_tag:   | DC Power                   | Target for regression   |

| xs:              x1:   | POA Irradiance             | Covariate for regression  |
|                  x2:   | Ambient Temperature        | Covariate for regression |
|                        |--------------------------------------------------------
|                  ...   | Based on your application, |
|                        | add as many covariates as  |
|                        | you want                   | 

| Measured GHI, ghi_tag  | GHI (irradiance)    | Day classification       |
| PVLib Clearsky, cs_tag | Simulated GHI       | Day classification       |

'''

# run algorithm
pvpolyfit(train_df, test_df, Y_tag, xs, I_tag, ghi_tag, cs_tag, 
	      highest_num_clusters, highest_degree, Y_high_filter, min_count_per_day, 
              plot_graph = True, graph_type = 'regression', print_info = False)