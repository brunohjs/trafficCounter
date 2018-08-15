import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def vector(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def module(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

def angleVectors(u, v):
    scalar = u[0] * v[0] + u[1] * v[1]
    mod = module(u) * module(v)
    angle = math.cos(scalar/mod)
    return math.degrees(angle)