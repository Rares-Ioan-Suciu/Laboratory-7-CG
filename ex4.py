import matplotlib.pyplot as plt
import math
import random

def generate_random_convex_polygon(n):
    angles = sorted(random.uniform(0, 2 * math.pi) for _ in range(n)) 
    points = {} # we first generate n random angles, in our case 7 and sort them in oredr, all to obtain a convex 7-vertex polygon
    #of course the polygon doesn t have to be a convex one, but it s easier to generate like this.
    for i, angle in enumerate(angles):
        x = math.cos(angle)
        y = math.sin(angle) # we get the coordonates from the angles using polar values
        label = chr(65 + i)
        points[label] = (x, y)

    return points

def define_triangulation(points): # we creayte the tirnagulation by starting from a vantage point and creating the diagonals to the other poins
    vertices = list(points.keys())
    edges = []

    for i in range(len(vertices)):
        edges.append((vertices[i], vertices[(i + 1) % len(vertices)]))


    vantage_point = vertices[0] # we choose the vantage point as the first point
    # we can do this as the polygon is convex and we don't have to worry about our diagonal going out of the polygon

    for vertex in vertices[1:]:
        edges.append((vantage_point, vertex))

    return edges # we add the diagonalks and return them along with the other edges.

def three_color_polygon(points):
    vertices = list(points.keys())
    coloring = {}

    vantage_point = vertices[0]
    coloring[vantage_point] = 0  # we first assign a color to the vantage point, as this point is connected to all the rest
    # this color won t be used anymore


    for i, vertex in enumerate(vertices[1:]):
        coloring[vertex] = (i % 2) + 1  # We go through te rest of the points and alternate between Red (1) and Green (2)

    return coloring

def plot_triangulated_polygon(points, edges, coloring):
    fig, ax = plt.subplots()
    color_map = ['blue', 'red', 'green']
    for edge in edges:
        v1, v2 = edge
        x_coords = [points[v1][0], points[v2][0]]
        y_coords = [points[v1][1], points[v2][1]]
        ax.plot(x_coords, y_coords, color='black', lw=1)
    for vertex, (x, y) in points.items():
        vertex_color = color_map[coloring[vertex]]
        ax.plot(x, y, 'o', color=vertex_color, markersize=10)
        ax.text(x + 0.05, y + 0.05, vertex, fontsize=12, color='black')

    ax.set_aspect('equal')
    plt.show()

def main():
    num_points = 7 
    for i in range(5): # we generate 5 examples, but this number vcould be bigger, again the exam session is not kind on time, and the OS exam won't be passed by itself
        print(f"\nExample {i + 1}:")
        points = generate_random_convex_polygon(num_points)
        edges = define_triangulation(points)
        coloring = three_color_polygon(points)


        print("Vertices:", points)
        print("Edges:", edges)
        print("Coloring:", coloring)

        plot_triangulated_polygon(points, edges, coloring)
        
main()
