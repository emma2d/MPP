def calculate_standard_deviation(data):
    # Calculate the mean
    mean = sum(data) / len(data)
    
    # Calculate the sum of squared differences from the mean
    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    
    # Calculate the variance
    variance = sum_squared_diff / len(data)
    
    # Calculate the standard deviation (square root of the variance)
    standard_deviation = variance ** 0.5
    
    return standard_deviation

# Example usage
data = [1, 2, 3, 4, 5]
result = calculate_standard_deviation(data)
print("Standard deviation:", result)
