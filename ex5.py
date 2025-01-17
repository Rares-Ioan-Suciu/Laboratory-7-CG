
import matplotlib.pyplot as plt
import random
from shapely.geometry import Polygon, Point

def generate_interior_point(pentagon):
    polygon = Polygon(pentagon)
    while True:
        x_min, x_max = min(p[0] for p in pentagon), max(p[0] for p in pentagon)
        y_min, y_max = min(p[1] for p in pentagon), max(p[1] for p in pentagon)

        candidate_point = Point(
            random.uniform(x_min + 0.1, x_max - 0.1),
            random.uniform(y_min + 0.1, y_max - 0.1)
        )
        if polygon.contains(candidate_point):
            return (candidate_point.x, candidate_point.y)


def generate_convex_pentagon_and_interior():
    y_collinear = random.uniform(-2, 2)
    x_values = sorted([random.uniform(-3, 3) for _ in range(3)])
    collinear_points = [(x, y_collinear) for x in x_values] # we first generate three collinear points on a horizonatl line
    #these points will be used to later generate the 4 points 4 edges triangulation

    
    y_above = y_collinear + random.uniform(1, 3)
    additional_points = [
        (x_values[0] - random.uniform(0.5, 1), y_above),
        (x_values[-1] + random.uniform(0.5, 1), y_above)
    ] # we afterwards generate two more points on another line for simplicity above the first collinear line 

    pentagon = sorted(collinear_points + additional_points)

    interior_point = generate_interior_point(pentagon)

    return pentagon, interior_point, collinear_points


def triangulation_six_points(example_num, pentagon, interior_point):
    plt.figure(figsize=(6, 6))
    plt.title(f"Example {example_num}: 6 Points, 10 Edges")
    plt.scatter(*zip(*pentagon), color="green", label="Pentagon Vertices")
    plt.scatter(*interior_point, color="red", label="Interior Point")
    
    for i, (x, y) in enumerate(pentagon, start=1):
        plt.text(x, y, f"P{i}", fontsize=10, ha="right")
    plt.text(interior_point[0], interior_point[1], "Interior", fontsize=10, color="blue", ha="right")


    for i in range(len(pentagon)):
        next_i = (i + 1) % len(pentagon)
        plt.plot([pentagon[i][0], pentagon[next_i][0]], [pentagon[i][1], pentagon[next_i][1]], "skyblue")
    
    for vertex in pentagon:
        plt.plot([interior_point[0], vertex[0]], [interior_point[1], vertex[1]], "pink", linestyle="dotted")
    
    plt.legend()
    plt.grid()
    plt.show()

def triangulation_four_points(example_num, collinear_points, interior_point):
    # we use the same three colinear points and the interior point, although we could have chosen one of the two other vertices also
    plt.figure(figsize=(6, 6))
    plt.title(f"Example {example_num}: 4 Points, 4 Edges")
    plt.scatter(*zip(*collinear_points), color="blue", label="Collinear Points")
    plt.scatter(*interior_point, color="red", label="Interior Point")

    for i, (x, y) in enumerate(collinear_points, start=1):
        plt.text(x, y, f"C{i}", fontsize=10, ha="right")
    plt.text(interior_point[0], interior_point[1], "E", fontsize=10, color="red", ha="right")
    for point in [collinear_points[0], collinear_points[-1]]:
        plt.plot([interior_point[0], point[0]], [interior_point[1], point[1]], "red", linestyle="dotted")

    plt.plot([collinear_points[0][0], collinear_points[-1][0]], 
             [collinear_points[0][1], collinear_points[-1][1]], "blue")
    
    plt.legend()
    plt.grid()
    plt.show()

def generate_examples():
    for i in range(1, 6):
        print(f"Generating Example {i}...")
        
        pentagon, interior_point, collinear_points = generate_convex_pentagon_and_interior()
        triangulation_six_points(i, pentagon, interior_point)
        triangulation_four_points(i, collinear_points, interior_point)
generate_examples()
