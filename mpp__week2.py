import csv
from bubble_sort_week2 import bubble_sort

def read_columns_from_csv (filename, column_name):

    # Given a csv file this function will read in defined column header and return the contents as a list.
    # : param list : filename : Path to the CSV file and column_name : Name of the target column
    # : return : a list from the specified column

    with open (filename , mode = 'r') as file:
        csv_file = csv.DictReader (file)
        column_data = []

        for row in csv_file:
            if column_name in row:
                column_data.append(int(row[column_name]))

    return (column_data)


def get_minimum_value (list):

    # Given a list of numbers as input this function will return the minimum value .
    # : param list : the list of numbers given as input
    # : return : the minimum value in the list

    minimum = list [0]
    for l in list:
        if l < minimum:
            minimum = l
    return minimum

def get_average (list) :

# Given a list of numbers as input this function will return the numerical average .
# : param list : the list of numbers given as input
# : return : the numerical average of the list 

    total = 0
    for l in list :
        total += l

    average = total / len ( list )
    return average

def get_median_value ( list ) :

    # Given a list of numbers as input this function will return the median value .
    # : param list : the function bubble_sort and a list of numbers are given as inputs
    # : return : the median (middle) value of the list

    list1 = list.copy()
    bubble_sort ( list1 )
    median = list1 [ int ( len ( list1 ) /2) ]
    return median



def get_mode (list) :

    # Given a list of numbers as input this function will return the mode value (apears most often) .
    # : param list : a list of numbers are given as inputs
    # : return : the mode value of the list
    
    highest_freq = 0
    mode = scores [0]
    for score in scores :
        frequency = 0
        for score2 in scores :
            if score == score2 :
                frequency += 1
        if frequency > highest_freq :
            mode = score
            highest_freq = frequency
    return mode

def get_maximum_value ( list ) :

    # Given a list of numbers as input this function will return the maximum value .
    # : param list : the list of numbers given as input
    # : return : the maximum value in the list

    maximum = list [0]
    for l in list :
        if maximum > l :
            maximum = l
        return maximum
    
def get_sum_of_sq_diff(list):

    # Given a list of numbers and average of the numbers as inputs this function will return the sum of the squared difference.
    # : param list : the list of numbers and a function called "get_average" are given as inputs
    # : return : the sum of squared differences of the list
       
    mean = get_average(list)
    return sum((x - mean) ** 2 for x in list)
     

def get_variance(list):

    # Given a list of numbers and the sum of squared differences of the numbers as inputs this function will return the variance.
    # : param list : the list of numbers and a function called "get_sum_of_sq_diff" are given as inputs
    # : return : the variance of the list

    sum_squared_diff = get_sum_of_sq_diff(list)
    return sum_squared_diff / len(list)
    
def get_stddev(list):

    # Given a list of numbers and the variance of the numbers as inputs this function will return the standard deviation.
    # : param list : the list of numbers and a function called "get_variance" are given as inputs
    # : return : the standard deviation of the list

    variance = get_variance(list)
    return variance ** 0.5 

if __name__ == "__main__" :

    csv_file_path = 'example.csv'
    column_name = 'Score'
    scores = read_columns_from_csv(csv_file_path, column_name)

    #scores = read_columns_from_csv ('example.csv')

    average = get_average (scores)
    minimum = get_minimum_value (scores)
    maximum = get_maximum_value (scores)
    median = get_median_value (scores)
    mode = get_mode (scores)
    var = get_variance (scores)
    stddev = get_stddev (scores)
   

print(f' Average : { average } \n Median : { median } \n Smallest : { minimum } \n Largest : { maximum } ')
print(f' Mode : { mode } \n Variance : {var} \n Stanard Deviation : {stddev}')

import statistics

minimum_value = min(scores)
average_value = statistics.mean(scores)
median_value = statistics.median(scores)
mode_value = statistics.mode(scores)

print("Using the 'statistics' library \nthe minimum value is " + str(minimum_value) + '\n' + "the average is " + str(average_value) + '\n' + "the median is " + str(median_value) + '\n' + "and the mode is " + str(mode_value) )