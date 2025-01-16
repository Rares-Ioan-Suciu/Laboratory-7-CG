import turtle
import math


#to solve this exercise and animate the whole process, in order to prove that the camera can see in the whole polygon, we will use the turtle python library

def draw_poly(points, color):  # we use this fucntion to draw the polygon, the points and the edges
    turtle.penup()
    turtle.goto(points[0])
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for point in points[1:]:
        turtle.goto(point)
    turtle.goto(points[0]) 
    turtle.end_fill() 

def scaling_points(points, scale): # an easy function to return all the points scaled using the 
    return [(x * scale, y * scale) for x, y in points]

def compute_centroid(polygon):
    x_coords = [p[0] for p in polygon]
    y_coords = [p[1] for p in polygon]
    centroid_x = sum(x_coords) / len(polygon)
    centroid_y = sum(y_coords) / len(polygon)
    return centroid_x, centroid_y # computing the centroid just as sum of coordoantes over the number of them

def find_intersection(polygon, ray_start, ray_end):
    """
    We use this function to fint the intersection point between the ray and the polygon such that the ray doens t exceed the boundries of the polygon
    """
    
    def on_segment(p, q, r):
        """"
         Function to check if the point q lies on the line segment defined by points p and r.
        """
        return (
            min(p[0], r[0]) <= q[0] <= max(p[0], r[0])
            and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])
        )

    def orientation(p, q, r):
        """
        we determine the orientation of three points (p, q, r), in order to determin relative postiong of two vectors

        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # 0 would mean points are colinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    def segments_intersect(p1, q1, p2, q2):
       
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # if the orientaions are different that means that that two lines will intereesct
        if o1 != o2 and o3 != o4:
            return True

        # the special cases where three of the pints are collinear
        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False

    def line_intersection(p1, q1, p2, q2):
        """
        Function to actually compute the intersection of two of the lines
        """
        a1 = q1[1] - p1[1]
        b1 = p1[0] - q1[0]
        c1 = a1 * p1[0] + b1 * p1[1]

        a2 = q2[1] - p2[1]
        b2 = p2[0] - q2[0]
        c2 = a2 * p2[0] + b2 * p2[1]  # we first compute some helper variable to easier compute the determinatn

        determinant = a1 * b2 - a2 * b1
        if determinant == 0:
            return None # usinf the deteminat to find intersection points, if it's 0 the the lines are parallel

        # Calculate intersection point
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant

        return x, y

    closest_intersection = None
    min_distance = float('inf')

    for i in range(len(polygon)):  # we go through each edge of the polygon and return the closest intersection of the ray with said edhges
        p1, p2 = polygon[i], polygon[(i + 1) % len(polygon)] 
        if segments_intersect(ray_start, ray_end, p1, p2):
            intersection = line_intersection(ray_start, ray_end, p1, p2)
            if intersection:
                distance = math.hypot(ray_start[0] - intersection[0], ray_start[1] - intersection[1])
                if distance < min_distance:
                    closest_intersection = intersection
                    min_distance = distance

    return closest_intersection

def rotate_ray(polygon, center, radius, steps):
    """
    We rotate a ray around the center point, in our case the camera, ensuring it doesn't exceed the polygon boundary.
    """
    angle_step = 360 / steps # the step size, the smaller it ease, the more filled the polygon will be
    for step in range(steps):
        angle = math.radians(step * angle_step) 
        ray_end = (center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle))
        intersection = find_intersection(polygon, center, ray_end)
        if intersection: # we draw the ray from the camera to the closest interseection
            turtle.penup()
            turtle.goto(center)
            turtle.pendown()
            turtle.color("green")  # Ray color
            turtle.goto(intersection)
            turtle.update()


def main():

    points = [
        (4, -4), (6, -4), (9, -6), (11, -6), (11, 6),
        (9, 6), (6, 4), (4, 4),
        (-5, 6), (-7, 4), (-7, -4), (-5, -6)
    ]  # the given points, computed for the first six the simetric with respect to Ox and sorted them in lexicographic order
     
    turtle.setup(width=1600, height=1000)
    turtle.speed(0)
    turtle.tracer(0, 0) # we first setup the screen on which the animation will be played, these measuerments can be changed 

    scaling_factor = 45  # we use a scaling factor in order to havwe a better visualization

    points = scaling_points(points, scaling_factor)
    interior_point = compute_centroid(points) # we scale tghe pints and  build the interior pint that will be our camera as the centroid of our polygon
    #there could be different points that satisfy the requierments, the main idea being that it should be on the Ox axis, the symetry axis of th polygon
    #the centoroid will have the coordonates (1.99,0)

    draw_poly(points, "red")

    turtle.penup()
    turtle.color("blue")
    for i, point in enumerate(points, start=1): 
        turtle.goto(point)
        turtle.dot(10)
        turtle.write(f"P{i}", align="left", font=("Arial", 14, "normal"))

    turtle.goto(interior_point)
    turtle.dot(12, "red")
    turtle.write("Camera/Guard", align="left", font=("Arial", 14, "bold"))

    rotate_ray(points, interior_point, 50 * scaling_factor, 14400) #here we create a ray that will not exceed the bounds of the polygon an rotate it in order to showcase
    #that the camera point can see anywhere inside the polygon. The 14400 will produce ana nimation that fills the whole polygon, but is a bit slow, consider changing to a
    # smaller number to see it move faster

    turtle.done()

if __name__ == "__main__":
    main()
