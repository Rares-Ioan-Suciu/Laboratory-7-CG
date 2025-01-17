import turtle
import math

def draw_polygon(points, color): 
    turtle.penup()
    turtle.goto(points[0])
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for point in points[1:]:
        turtle.goto(point)
    turtle.goto(points[0])
    turtle.end_fill() # we use the turtel module in python to draw the points given and the polygon in lexicographic order first thing

def scale_points(points, scaling): # scaling all the points to better visualzie them
    return [(x * scaling, y * scaling) for x, y in points]

def find_intersection(ray_start, ray_end, seg_start, seg_end):
    x1, y1 = ray_start
    x2, y2 = ray_end
    x3, y3 = seg_start
    x4, y4 = seg_end # in order to know where to end a ray, to create a visualization that only fills the polygon, we are find the interstionc of the 
    # of the ray with the edge in order to not exceed the boundries

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) 
    if abs(denom) < 1e-4:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom
    if 0 <= t <= 1 and 0 <= u <= 1: 
        intersect_x = x1 + t * (x2 - x1)
        intersect_y = y1 + t * (y2 - y1)
        return intersect_x, intersect_y

    return None

def rotate_ray(center, radius, steps, polygon):
    cameraX, cameraY = center # we use this fucntion to rotate around the polygon given, in order to fill it in, we start by using the camera position
    angle_step = 360 / steps # the bigger the number of steps, the more lines t
    for step in range(steps):
        angle = math.radians(step * angle_step)
        ray_end = (cameraX + radius * math.cos(angle), cameraY + radius * math.sin(angle),)

        closest_intersection = None
        min_distance = float("inf")
        for i in range(len(polygon)):
            seg_start = polygon[i]
            seg_end = polygon[(i + 1) % len(polygon)]
            intersection = find_intersection(center, ray_end, seg_start, seg_end)
            if intersection:
                dist = math.sqrt((intersection[0] - cameraX) ** 2 + (intersection[1] - cameraY) ** 2)
                if dist < min_distance:
                    min_distance = dist
                    closest_intersection = intersection

        if closest_intersection:
            turtle.penup()
            turtle.goto(center)
            turtle.pendown()
            turtle.goto(closest_intersection)
            turtle.update()


def main():
    turtle.setup(width=1000, height=800)
    turtle.speed(0)
    turtle.tracer(0, 0)

    scale_factor = 70

    points = [
        (0, 5), (-1, -2), (3, -2), (3, 0), (3, 2), (1, 2)
    ] 
    points = scale_points(points, scale_factor)

     # Exercise a):
    turtle.clear()
    interior_point_a = (0, 1 * scale_factor) # we placed the camera same as in the geogebra such that is able to see both in the ear clipping part and in the rest of the polygon
    draw_polygon(points, "purple")

    labels = ["P1", "P3", "P2", "P4", "P6", "P5"]
    turtle.color("blue")
    for i, point in enumerate(points):
        turtle.penup()
        turtle.goto(point)
        turtle.dot(10)
        turtle.write(labels[i], align="left", font=("Arial", 14, "normal"))
    turtle.color("red")
    turtle.goto(interior_point_a)
    turtle.dot(12, "red")
    turtle.write("Camera", align="left", font=("Arial", 14, "bold"))

    turtle.color("yellow")
    rotate_ray(interior_point_a, 20 * scale_factor, 1440, points)

    turtle.update()
    turtle.penup()
    turtle.goto(-300, -200)
    turtle.update()

    #Exercise b)
    turtle.clear()
    draw_polygon(points, "beige")
    intersection_point = (2.34, -2) # this point is the intersection of our separator line P1P5 extended and the line P2P3
    scaled_inter_point = (intersection_point[0] * scale_factor, intersection_point[1] * scale_factor)
    turtle.penup()
    turtle.goto(scaled_inter_point)
    turtle.dot(10, "blue")
    turtle.write("(2.34, -2)", align="left", font=("Arial", 14, "normal"))

    turtle.color("green")
    turtle.penup()
    turtle.goto(points[5])
    turtle.pendown()
    turtle.color("black")
    turtle.goto(scaled_inter_point) # draw the separating lines of our two imagianry subpolygons, that we want our cameras to monitor

    labels = ["P1", "P3", "P2", "P4", "P6", "P5"]
    turtle.color("blue")
    for i, point in enumerate(points):
        turtle.penup()
        turtle.goto(point)
        turtle.dot(10)
        turtle.write(labels[i], align="left", font=("Arial", 14, "normal"))


    subpolygon1 = [points[0], points[1], scaled_inter_point, points[5]] # we make two imaginary subpolygons from the big polygon, the first one correspondss to what
    subpolygon2 = [points[5], scaled_inter_point, points[2], points[3], points[4]] # thw camera from the trinagle/ear clipping could see, and the second subpolygon
    #is meant to first showcase what the blindspot of camera 1 is and then be covered by a second camera
    #of cousre this second camera could see more of the polygon, but the scope of the animation is to prove that 2 camera can conver the whole polygon

    camera1 = (0.4 * scale_factor, 3.7 * scale_factor)  # we place camera 1 insinde the ear clipping and the second one inside the second polygon
    camera2 = (2.2 * scale_factor, 1.3 * scale_factor)  # we have changed the postion from the geogebra to shocase that there are a variety of solutions.

    turtle.color("pink")
    turtle.goto(camera1)
    turtle.dot(12, "pink")
    turtle.write("Camera 1", align="left", font=("Arial", 14, "bold"))
    rotate_ray(camera1, 15 * scale_factor, 1440, subpolygon1)

    turtle.color("white")
    turtle.goto(camera2)
    turtle.color("blue")
    turtle.color("green")
    rotate_ray(camera2, 15 * scale_factor, 1440, subpolygon2)
    turtle.goto(camera2)
    turtle.color("yellow")
    turtle.dot(12, "yellow")
    turtle.write("Camera 2", align="left", font=("Arial", 14, "bold"))

    turtle.update()
    turtle.penup()
    turtle.goto(-300, -200)
    turtle.update()
    turtle.done()

if __name__ == "__main__":
    main()
