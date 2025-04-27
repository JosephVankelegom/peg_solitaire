import numpy as np
import math
from numpy.linalg import norm
from copy import deepcopy
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Your points
points_original = np.array([
    [1846, 3280], [1850, 2533], [1840, 1432], [2549, 1780], [683, 2116],
    [356, 1750], [1070, 3293], [2570, 2140], [1081, 2482], [1466, 3271],
    [2185, 1417], [316, 2113], [1447, 1777], [742, 1378], [2204, 2155],
    [1465, 2147], [701, 1768], [1843, 1045], [1496, 1102], [296, 2470],
    [2206, 1777], [1465, 2879], [722, 2899], [1081, 1045], [2560, 2515],
    [1436, 1417], [1096, 2138], [1090, 2908], [2221, 2516], [1838, 2171],
    [1150, 1411], [2213, 2857], [685, 2485], [1829, 1798], [1117, 1756],
    [1471, 2548], [1826, 2891]
])

# Function to check if two slopes are parallel (within a tolerance)
def are_parallel(slope1, slope2, tolerance=0.1):
    return abs(slope1 - slope2) < tolerance

# Function to check if two slopes are perpendicular
def are_perpendicular(slope1, slope2, tolerance=0.1):
    return abs(slope1 * slope2 + 1) < tolerance  # Perpendicular slopes should multiply to -1

def order_points(values):
    def sum(x):
        total = 0
        for i in x:
            total += i
        return total
    return sorted(values, key=sum)
    
        
    

def mean_smaller_distance(values):
    num_of_close_p = 3
    total = 0
    for i in range(len(values)):
        smallest = []
        for j in range(len(values)):
            if i == j :
                continue
            dist = math.dist(values[i],values[j])
            smallest.append(dist)
            if len(smallest) > num_of_close_p:
                smallest.sort()
                smallest = smallest[0:num_of_close_p]
        for k in range(len(smallest)):
            total += smallest[k]
    total = total / (num_of_close_p*len(values))
    return total
# Set up the plot
plt.figure(figsize=(10, 8))

def get_lines(points, number_of_lines, slope=None):
    # List to store line equations (slope, intercept, and number of points)
    def get_lines_intern(points_set, result_lines):
        if len(points_set) < 2:
            return result_lines
        for p1 in points_set:
            best_line = None
            
            for p2 in points_set:
                if np.array_equal(p1, p2):
                    continue
                
                x = np.array([p1[0], p2[0]]).reshape(-1, 1)  # X-values of the two points
                y = [p1[1], p2[1]]  # y-values of the two points
                reg = LinearRegression().fit(x, y)
                slope = reg.coef_[0]
                intercept = reg.intercept_
                
                close_points = []
                for p3 in points:
                    distance = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
                    if distance < mean_dist/4:  # You can adjust the threshold as needed
                        close_points.append(p3)
                if best_line is None or len(best_line[2]) < len(close_points):
                    best_line =(slope, intercept, order_points(close_points))
            if best_line is not None:
                new_result_lines = deepcopy(result_lines)
                new_points = [p for p in points_set
                    if not any(np.array_equal(p, r) for r in best_line[2])
                ]
                
                new_result_lines.append(best_line)
                return get_lines_intern(new_points, new_result_lines)
                
    
    
    mean_dist = mean_smaller_distance(points)
    lines = []
    result = get_lines_intern(points, lines)
    return result

lines = get_lines(points_original, 7)
for i in lines:
    print(i[2])
# Sort lines by number of points they link (in descending order)
lines.sort(key=lambda x: len(x[2]), reverse=True)

# Keep only the top lines
lines = lines[:14]

# Check for parallel and perpendicular lines
parallel_lines = []
perpendicular_lines = []

for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        slope1, intercept1, _ = lines[i]
        slope2, intercept2, _ = lines[j]

        # Check if lines are parallel
        if are_parallel(slope1, slope2):
            parallel_lines.append((i, j))
        
        # Check if lines are perpendicular
        if are_perpendicular(slope1, slope2):
            perpendicular_lines.append((i, j))

# Ensure balance between parallel and perpendicular lines
# Adjust the number of lines to make parallel and perpendicular counts equal if necessary
if len(parallel_lines) > len(perpendicular_lines):
    parallel_lines = parallel_lines[:len(perpendicular_lines)]
elif len(parallel_lines) < len(perpendicular_lines):
    perpendicular_lines = perpendicular_lines[:len(parallel_lines)]
    
points = points_original

# Plot lines and check for parallel or perpendicular conditions
for line in lines:
    slope, intercept, count = line
    x_line = np.linspace(points[:, 0].min(), points[:, 0].max(), 200)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, label=f'Line: {slope:.2f}, Points: {count}', linestyle='--')

# Highlight parallel lines in blue and perpendicular lines in green
for (i, j) in parallel_lines:
    slope1, intercept1, _ = lines[i]
    slope2, intercept2, _ = lines[j]
    plt.plot(x_line, slope1 * x_line + intercept1, 'b--')  # Mark parallel lines in blue
    plt.plot(x_line, slope2 * x_line + intercept2, 'b--')  # Mark parallel lines in blue

for (i, j) in perpendicular_lines:
    slope1, intercept1, _ = lines[i]
    slope2, intercept2, _ = lines[j]
    plt.plot(x_line, slope1 * x_line + intercept1, 'g--')  # Mark perpendicular lines in green
    plt.plot(x_line, slope2 * x_line + intercept2, 'g--')  # Mark perpendicular lines in green

# Plot all points
plt.scatter(points[:, 0], points[:, 1], color='black', marker='x', label='Points')

# Display the legend and plot
plt.title("Best Lines Fitting Points (Parallel and Perpendicular Conditions)")
plt.grid(True)
plt.xlim(points[:, 0].min() - 50, points[:, 0].max() + 50)
plt.ylim(points[:, 1].min() - 50, points[:, 1].max() + 50)
#plt.show()
