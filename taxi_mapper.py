#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import re
#import matplotlib.pyplot as plt
#%matplotlib inline

#conda install -c conda-forge geopy
# or
#pip install geopy
from geopy.distance import vincenty

def detect_problem(pattern, x):
    try:
        if pattern.match(x) == None:
            return 1
        else:
            return 0
    except:
        return 1
    return 1  

def get_minute_section(x):
    if x < 10:
        return 1
    elif x >= 10 and x < 20:
        return 2
    elif x >= 20 and x<30:
        return 3
    elif x >= 30 and x < 40:
        return 4
    elif x >= 40 and x < 50:
        return 5
    else:
        return 6


def csv_mapper(line_input):
    # key,fare_amount,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
    split_line = line_input.split(',')

    input_fields = dict()
    input_fields['key'] = split_line[0]
    input_fields['fare_amount'] = split_line[1]
    input_fields['pickup_datetime'] = split_line[2]
    input_fields['pickup_longitude'] = split_line[3]
    input_fields['pickup_latitude'] = split_line[4]
    input_fields['dropoff_longitude'] = split_line[5]
    input_fields['dropoff_latitude'] = split_line[6]
    input_fields['passenger_count'] = split_line[7]

    problem = 0
    
    output_fields = dict()

    # distance between pickup and dropoff
    try:
        output_fields['distance'] = np.int(np.ceil(vincenty(
            (input_fields['pickup_latitude'], input_fields['pickup_longitude']),
            (input_fields['dropoff_latitude'], input_fields['dropoff_longitude'])
        ).miles))
    except:
        output_fields['distance'] = 0
        problem = 1

    if (output_fields['distance'] <= 0):
        output_fields['distance'] = 0
        problem = 1;

    # fare_amount
    output_fields['fare_amount_bin'] = np.int(np.ceil(np.float64(input_fields['fare_amount'])))
    if(output_fields['fare_amount_bin'] < 0):
        problem = 1
        
    # pickup_datetime
    output_fields['pickup_datetime'] = pd.to_datetime(input_fields['pickup_datetime'], format='%Y-%m-%d %H:%M:%S %Z')
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.weekday.html
    # The day of the week with Monday=0, Sunday=6  
    output_fields['pickup_day_of_week'] = output_fields['pickup_datetime'].weekday()
    output_fields['pickup_day'] = output_fields['pickup_datetime'].day
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.month.html
    # The month as January=1, December=12
    output_fields['pickup_month'] = output_fields['pickup_datetime'].month
    output_fields['pickup_hour'] = output_fields['pickup_datetime'].hour
    output_fields['pickup_minute'] = output_fields['pickup_datetime'].minute
    output_fields['pickup_minute_section'] = get_minute_section(output_fields['pickup_minute'])
    
    # pickup_longitude
    pattern = re.compile('^[-]?[0-9]+[.][0-9]+$')
    if pattern.match(input_fields['pickup_longitude']) == None:
        problem = 1
    
    if (problem == 0):
        output_fields['pickup_longitude_whole'] = np.int16(input_fields['pickup_longitude'].split('.')[0])
        output_fields['pickup_longitude_mantissa'] = np.str(input_fields['pickup_longitude'].split('.')[1].ljust(6,'0')) 
        
        output_fields['pickup_longitude_mantissa_1'] = np.int8(output_fields['pickup_longitude_mantissa'][0:1])
        output_fields['pickup_longitude_mantissa_2'] = np.int8(output_fields['pickup_longitude_mantissa'][1:2])
        output_fields['pickup_longitude_mantissa_3'] = np.int8(output_fields['pickup_longitude_mantissa'][2:3])
        output_fields['pickup_longitude_mantissa_4'] = np.int8(output_fields['pickup_longitude_mantissa'][3:4])
        output_fields['pickup_longitude_mantissa_5'] = np.int8(output_fields['pickup_longitude_mantissa'][4:5])
        output_fields['pickup_longitude_mantissa_6'] = np.int8(output_fields['pickup_longitude_mantissa'][5:6])

    # pickup_latitude    
    pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
    if pattern.match(input_fields['pickup_latitude']) == None:
        problem = 1

    if (problem == 0):        
        output_fields['pickup_latitude_whole'] = np.int16(input_fields['pickup_latitude'].split('.')[0])
        output_fields['pickup_latitude_mantissa'] = np.str(input_fields['pickup_latitude'].split('.')[1].ljust(6,'0')) 

        output_fields['pickup_latitude_mantissa_1'] = np.int8(output_fields['pickup_latitude_mantissa'][0:1])
        output_fields['pickup_latitude_mantissa_2'] = np.int8(output_fields['pickup_latitude_mantissa'][1:2])
        output_fields['pickup_latitude_mantissa_3'] = np.int8(output_fields['pickup_latitude_mantissa'][2:3])
        output_fields['pickup_latitude_mantissa_4'] = np.int8(output_fields['pickup_latitude_mantissa'][3:4])
        output_fields['pickup_latitude_mantissa_5'] = np.int8(output_fields['pickup_latitude_mantissa'][4:5])
        output_fields['pickup_latitude_mantissa_6'] = np.int8(output_fields['pickup_latitude_mantissa'][5:6])
       
    # dropoff_longitude
    pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
    if detect_problem(pattern, input_fields['dropoff_longitude']) == 1:
        problem = 1
        
    if (problem == 0):
        output_fields['dropoff_longitude_whole'] = np.int16(input_fields['dropoff_longitude'].split('.')[0])
        output_fields['dropoff_longitude_mantissa'] = np.str(input_fields['dropoff_longitude'].split('.')[1].ljust(6,'0')) 
        
        output_fields['dropoff_longitude_mantissa_1'] = np.int8(output_fields['dropoff_longitude_mantissa'][0:1])
        output_fields['dropoff_longitude_mantissa_2'] = np.int8(output_fields['dropoff_longitude_mantissa'][1:2])
        output_fields['dropoff_longitude_mantissa_3'] = np.int8(output_fields['dropoff_longitude_mantissa'][2:3])
        output_fields['dropoff_longitude_mantissa_4'] = np.int8(output_fields['dropoff_longitude_mantissa'][3:4])
        output_fields['dropoff_longitude_mantissa_5'] = np.int8(output_fields['dropoff_longitude_mantissa'][4:5])
        output_fields['dropoff_longitude_mantissa_6'] = np.int8(output_fields['dropoff_longitude_mantissa'][5:6])        
        
    # dropoff_latitude    
    pattern = re.compile('^[-]?[0-9]+\.[0-9]+$')
    if detect_problem(pattern, input_fields['dropoff_latitude']) == 1:
        problem = 1
        
    if (problem == 0):
        output_fields['dropoff_latitude_whole'] = np.int16(input_fields['dropoff_latitude'].split('.')[0])
        output_fields['dropoff_latitude_mantissa'] = np.str(input_fields['dropoff_latitude'].split('.')[1].ljust(6,'0')) 
        
        output_fields['dropoff_latitude_mantissa_1'] = np.int8(output_fields['dropoff_latitude_mantissa'][0:1])
        output_fields['dropoff_latitude_mantissa_2'] = np.int8(output_fields['dropoff_latitude_mantissa'][1:2])
        output_fields['dropoff_latitude_mantissa_3'] = np.int8(output_fields['dropoff_latitude_mantissa'][2:3])
        output_fields['dropoff_latitude_mantissa_4'] = np.int8(output_fields['dropoff_latitude_mantissa'][3:4])
        output_fields['dropoff_latitude_mantissa_5'] = np.int8(output_fields['dropoff_latitude_mantissa'][4:5])
        output_fields['dropoff_latitude_mantissa_6'] = np.int8(output_fields['dropoff_latitude_mantissa'][5:6])   
        
    # passenger_count
    output_fields['passenger_count'] = np.int(input_fields['passenger_count'])
    
    if (problem == 0):
        sys.stdout.write("{},{},{},{},{},{},{}".format(input_fields['key'],
                                                       output_fields['fare_amount_bin'],
                                                       output_fields['pickup_day_of_week'],
                                                       output_fields['pickup_day'],
                                                       output_fields['pickup_month'],
                                                       output_fields['pickup_hour'],
                                                       output_fields['pickup_minute_section']))
                         
        sys.stdout.write(",{},{},{},{},{},{},{}".format(output_fields['pickup_longitude_whole'],        
                                                        output_fields['pickup_longitude_mantissa_1'],
                                                        output_fields['pickup_longitude_mantissa_2'],
                                                        output_fields['pickup_longitude_mantissa_3'],
                                                        output_fields['pickup_longitude_mantissa_4'],
                                                        output_fields['pickup_longitude_mantissa_5'],
                                                        output_fields['pickup_longitude_mantissa_6']))
                                                       
        sys.stdout.write(",{},{},{},{},{},{},{}".format(output_fields['pickup_latitude_whole'],
                                                        output_fields['pickup_latitude_mantissa_1'],
                                                        output_fields['pickup_latitude_mantissa_2'],
                                                        output_fields['pickup_latitude_mantissa_3'],
                                                        output_fields['pickup_latitude_mantissa_4'],
                                                        output_fields['pickup_latitude_mantissa_5'],
                                                        output_fields['pickup_latitude_mantissa_6']))
                                                       
        sys.stdout.write(",{},{},{},{},{},{},{}".format(output_fields['dropoff_longitude_whole'],
                                                        output_fields['dropoff_longitude_mantissa_1'],
                                                        output_fields['dropoff_longitude_mantissa_2'],
                                                        output_fields['dropoff_longitude_mantissa_3'],
                                                        output_fields['dropoff_longitude_mantissa_4'],
                                                        output_fields['dropoff_longitude_mantissa_5'],
                                                        output_fields['dropoff_longitude_mantissa_6']))
                                                       
        sys.stdout.write(",{},{},{},{},{},{},{}".format(output_fields['dropoff_latitude_whole'],
                                                        output_fields['dropoff_latitude_mantissa_1'],
                                                        output_fields['dropoff_latitude_mantissa_2'],
                                                        output_fields['dropoff_latitude_mantissa_3'],
                                                        output_fields['dropoff_latitude_mantissa_4'],
                                                        output_fields['dropoff_latitude_mantissa_5'],
                                                        output_fields['dropoff_latitude_mantissa_6']))
        
        sys.stdout.write(",{}".format(output_fields['distance']))
        sys.stdout.write(",{}\n".format(output_fields['passenger_count']))
    
#if __name__ == "__main__":
#    for line in sys.stdin:
#        for word in line.split():
#            sys.stdout.write("{}\t1\n".format(word))

if __name__ == "__main__":
    for line in sys.stdin:
        if line[:4] == "key,":
            #sys.stdout.write("{}\n".format(line))
            pass 

        else:
            csv_mapper(line)
    #csv_mapper("2009-06-15 17:26:21.0000001,4.5,2009-06-15 17:26:21 UTC,-73.844311,40.721319,-73.84161,40.712278,1")
