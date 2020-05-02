
import random

INFECTION_RADIUS = 6
CHANCE_OF_INFECTION = 20

# basically if its in the square it ll run the probability thingy to see if infected
def is_infected(position1, position2):
    if (position2[0] - INFECTION_RADIUS <= position1[0] and position1[0] <= position2[0] + INFECTION_RADIUS) or (position2[1] - INFECTION_RADIUS <= position1[1] and position1[1] <= position2[1] + INFECTION_RADIUS):
        return random.randrange(100) <= CHANCE_OF_INFECTION

class Person:
    infected = False #technically we can just create each object with this already filled out right?
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position
