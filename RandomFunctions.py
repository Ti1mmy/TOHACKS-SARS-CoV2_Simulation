import random

INFECTION_RADIUS = 6
CHANCE_OF_INFECTION = 20
PEOPLE_INFECTED = []
BASE_TIME = 1000000000 #add

# when we put the code together remember to make an if that checks if person is already True. efficiecny
def is_infected(position1, position2):
    if (position2[0] - INFECTION_RADIUS <= position1[0] and position1[0] <= position2[0] + INFECTION_RADIUS) and (position2[1] - INFECTION_RADIUS <= position1[1] and position1[1] <= position2[1] + INFECTION_RADIUS):
        return random.randrange(100) < CHANCE_OF_INFECTION
    else:
        return False

class Person:
    infected = False
    timeInfected = 0
    position = []

    def __init__(self, infected, position):
        self.infected = infected
        self.position = position

    
person1 = Person(False, [50, 50])
person2 = Person(False, [49, 48])

if is_infected(person1.position, person2.position):
    person1.infected = True
    person1.timeInfected = time.time()
    PEOPLE_INFECTED.append(person1)

print(person1.infected)

#add
CURE_RATE = 1

def cure():
    for i in range(len(PEOPLE_INFECTED)):
        if random.randrange(100) < CURE_RATE and time.time() - PEOPLE_INFECTED[i].timeInfected >= BASE_TIME:
            luckyBoi = random.choice(PEOPLE_INFECTED)
            PEOPLE_INFECTED.pop(luckyBoi)
            luckyBoi.infected = False








positions = []

for i in range(len[positions]):
    for j in range(i+1, len[positions]):
        distance = ((positions[j][0]-positions[i][0])^2 +(positions[j][1] - positions[i][1])^2)^(1/2)

        if distance <= INFECTION_RANGE:
