import random

INFECTION_RADIUS = 6
CHANCE_OF_INFECTION = 20


def is_infected(position1, position2):
    if (position2[0] - INFECTION_RADIUS <= position1[0] and position1[0] <= position2[0] + INFECTION_RADIUS) and (position2[1] - INFECTION_RADIUS <= position1[1] and position1[1] <= position2[1] + INFECTION_RADIUS):
        return random.randrange(100) < CHANCE_OF_INFECTION
    else:
        return False

class Person:
    infected = False
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position

    
person1 = Person(False, [50, 50])
person2 = Person(False, [49, 48])

if is_infected(person1.position, person2.position):
    person1.infected = True

print(person1.infected)


    
