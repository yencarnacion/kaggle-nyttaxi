
Ideas
maybe just focus on middle 97.5 of fare_amount


```python
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import re
import gc
#%matplotlib inline
```


```python
!head train10k.csv
```


```python
%%time 
#train = pd.read_csv('train.csv', sep=',', header=0, parse_dates=['pickup_datetime'], 
#                    dtype={'key':np.str,'fare_amount':np.float64,'pickup_datetime': np.str,
#                    'pickup_longitude': np.str, 'pickup_latitude': np.str,
#                    'dropoff_longitude': np.str, 'dropoff_latitude': np.str,
#                    'passenger_count': np.int})
train = pd.read_csv('train.csv', sep=',', header=0, 
                    dtype={'key':np.str,'fare_amount':np.str,'pickup_datetime': np.str,
                    'pickup_longitude': np.str, 'pickup_latitude': np.str,
                    'dropoff_longitude': np.str, 'dropoff_latitude': np.str,
                    'passenger_count': np.str})
```


```python
%%time
train['pickup_datetime'] = pd.to_datetime(train['pickup_datetime'], format='%Y-%m-%d %H:%M:%S %Z')
```


```python
%%time
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.weekday.html
# The day of the week with Monday=0, Sunday=6
train['pickup_day_of_week'] = train['pickup_datetime'].dt.weekday
```


```python
train['pickup_day'] = train['pickup_datetime'].dt.day
```


```python
%%time
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.month.html
# The month as January=1, December=12
train['pickup_month'] = train['pickup_datetime'].dt.month
```


```python
train['pickup_hour'] = train['pickup_datetime'].dt.hour
```


```python
train['pickup_minute_section'] = train['pickup_datetime'].dt.minute
train['pickup_minute_section'] = train['pickup_minute_section'].map(lambda x: 1 if x < 10 else (2 if x >= 10 and x < 20 else (3 if x >= 20 and x<30 else (4 if x >= 30 and x < 40 else (5 if x >= 40 and x < 50 else (6))))))
```


```python
train.drop(['pickup_datetime'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
# Drop rows with bad pickup locations
pattern = re.compile('^[-]?[0-9]+[.][0-9]+$')
train['pickup_longitude_problem'] = train['pickup_longitude'].map(lambda x: 1 if pattern.match(x) == None else 0)
train.drop(train[train['pickup_longitude_problem'] == 1].index, inplace=True)
train.drop(['pickup_longitude_problem'], axis=1, inplace=True)
```


```python
train['pickup_longitude_whole'] = train['pickup_longitude'].map(lambda x: np.int16(x.split('.')[0]))
```


```python
train['pickup_longitude_mantissa'] = train['pickup_longitude'].map(lambda x: np.str(x.split('.')[1].ljust(6,'0')))
```


```python
train.drop(['pickup_longitude'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
train['pickup_longitude_mantissa_1'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[0:1]))
```


```python
train['pickup_longitude_mantissa_2'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[1:2]))
```


```python
train['pickup_longitude_mantissa_3'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[2:3]))
```


```python
train['pickup_longitude_mantissa_4'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[3:4]))
```


```python
train['pickup_longitude_mantissa_5'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[4:5]))
```


```python
train['pickup_longitude_mantissa_6'] = train['pickup_longitude_mantissa'].map(lambda x: np.int8(x[5:6]))
```


```python
train.drop(['pickup_longitude_mantissa'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
# Drop rows with bad pickup locations
pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
train['pickup_latitude_problem'] = train['pickup_latitude'].map(lambda x: 1 if pattern.match(x) == None else 0)
train.drop(train[train['pickup_latitude_problem'] == 1].index, inplace=True)
train.drop(['pickup_latitude_problem'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
train['pickup_latitude_whole'] = train['pickup_latitude'].map(lambda x: np.int16(x.split('.')[0]))
```


```python
train['pickup_latitude_mantissa'] = train['pickup_latitude'].map(lambda x: np.str(x.split('.')[1].ljust(6,'0')))
```


```python
train.drop(['pickup_latitude'], axis=1, inplace=True)
```


```python
train['pickup_latitude_mantissa_1'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[0:1]))
```


```python
train['pickup_latitude_mantissa_2'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[1:2]))
```


```python
train['pickup_latitude_mantissa_3'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[2:3]))
```


```python
train['pickup_latitude_mantissa_4'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[3:4]))
```


```python
train['pickup_latitude_mantissa_5'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[4:5]))
```


```python
train['pickup_latitude_mantissa_6'] = train['pickup_latitude_mantissa'].map(lambda x: np.int8(x[5:6]))
```


```python
train.drop(['pickup_latitude_mantissa'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
# Drop rows with bad dropoff locations
pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
def detect_problem(x):
    try:
        if pattern.match(x) == None:
            return 1
        else:
            return 0
    except:
        return 1
    return 1
```


```python
train['dropoff_longitude_problem'] = train['dropoff_longitude'].map(detect_problem)
train.drop(train[train['dropoff_longitude_problem'] == 1].index, inplace=True)
train.drop(['dropoff_longitude_problem'], axis=1, inplace=True)
```


```python
train['dropoff_longitude_whole'] = train['dropoff_longitude'].map(lambda x: np.int16(x.split('.')[0]))
```


```python
train['dropoff_longitude_mantissa'] = train['dropoff_longitude'].map(lambda x: np.str(x.split('.')[1].ljust(6,'0')))
```


```python
train.drop(['dropoff_longitude'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
train['dropoff_longitude_mantissa_1'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[0:1]))
```


```python
train['dropoff_longitude_mantissa_2'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[1:2]))
```


```python
train['dropoff_longitude_mantissa_3'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[2:3]))
```


```python
train['dropoff_longitude_mantissa_4'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[3:4]))
```


```python
train['dropoff_longitude_mantissa_5'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[4:5]))
```


```python
train['dropoff_longitude_mantissa_6'] = train['dropoff_longitude_mantissa'].map(lambda x: np.int8(x[5:6]))
```


```python
gc.collect()
```


```python
train.drop(['dropoff_longitude_mantissa'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
# Drop rows with bad dropoff locations
pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
def detect_problem(x):
    try:
        if pattern.match(x) == None:
            return 1
        else:
            return 0
    except:
        return 1
    return 1
train['dropoff_latitude_problem'] = train['dropoff_latitude'].map(detect_problem)
train.drop(train[train['dropoff_latitude_problem'] == 1].index, inplace=True)
train.drop(['dropoff_latitude_problem'], axis=1, inplace=True)
```


```python
train['dropoff_latitude_whole'] = train['dropoff_latitude'].map(lambda x: np.int16(x.split('.')[0]))
```


```python
train['dropoff_latitude_mantissa'] = train['dropoff_latitude'].map(lambda x: np.str(x.split('.')[1].ljust(6,'0')))
```


```python
# **stops here with memory error**
train.drop(['dropoff_latitude'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
train['dropoff_latitude_mantissa_1'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[0:1]))
```


```python
train['dropoff_latitude_mantissa_2'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[1:2]))
```


```python
train['dropoff_latitude_mantissa_3'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[2:3]))
```


```python
train['dropoff_latitude_mantissa_4'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[3:4]))
```


```python
train['dropoff_latitude_mantissa_5'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[4:5]))
```


```python
train['dropoff_latitude_mantissa_6'] = train['dropoff_latitude_mantissa'].map(lambda x: np.int8(x[5:6]))
```


```python
gc.collect()
```


```python
train.drop(['dropoff_latitude_mantissa'], axis=1, inplace=True)
```


```python
%%time
train['fare_amount'] = train['fare_amount'].astype(np.float64)
```


```python
%%time
train['fare_amount_bin'] = train['fare_amount'].map(np.ceil).astype(np.int)
```


```python
# there are trips with negative fare
train['negative_fares']=train['fare_amount'].map(lambda x: 1 if x<0 else 0)
train.drop(train[train['negative_fares'] == 1].index, inplace=True)
train.drop(['negative_fares'], axis=1, inplace=True)
```


```python
train.drop(['fare_amount'], axis=1, inplace=True)
```


```python
gc.collect()
```


```python
%%time
train['passenger_count'] = train['passenger_count'].astype(np.int)
```


```python
# there are trips with 0 passengers
train['passenger_count'].map(lambda x: 1 if x == 0 else 0).sum()
```


```python
# number of fares na or null
# print(train['fare_amount'].isna().sum())
# print(train['fare_amount'].isnull().sum())
```


```python
# number of trips with fares of $0
# train['fare_amount'].map(lambda x: 1 if x == 0 else 0).sum()
```


```python
train['fare_amount_bin'].value_counts()
```


```python
train['fare_amount_bin'].describe()
```


```python
train.info()
```
