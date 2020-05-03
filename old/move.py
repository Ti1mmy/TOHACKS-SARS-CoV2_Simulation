import random
global p
p = []

class Person:
    xLoc = -1
    yLoc = -1
    status = "";
    b = -1
    dir = -1
    cons = 100

    def __init__(self, xLoc, yLoc, status):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.b = yLoc
        self.status = status
        self.dirY = random.randint(-100, 100)/self.cons
        self.dirX = random.randint(-100, 100)/self.cons
        if(self.dirY == 0): self.dirY = random.randint(-125, -100)/self.cons
        if(self.dirX == 0): self.dirX = random.randint(100, 125)/self.cons

    def move(self):
        self.yLoc += self.dirY
        self.xLoc += self.dirX
        if self.xLoc >= 300: 
            self.dirX = random.randint(-125, -100)/self.cons
            if(random.randint(1, 2) == 1): self.dirY = random.randint(-125, -100)/self.cons
            else: self.dirY = random.randint(100, 125)/self.cons
        if self.xLoc <= 100:
            self.dirX = random.randint(100, 125)/self.cons
            if(random.randint(1, 2) == 1): self.dirY = random.randint(-125, -100)/self.cons
            else: self.dirY = random.randint(100, 125)/self.cons
        if self.yLoc >= 300: 
            self.dirY = random.randint(-125, -100)/self.cons
            if(random.randint(1, 2) == 1): self.dirX = random.randint(-125, -100)/self.cons
            else: self.dirX = random.randint(100, 125)/self.cons
        if self.yLoc <= 100:
            self.dirY = random.randint(100, 125)/self.cons
            if(random.randint(1, 2) == 1): self.dirX = random.randint(-125, -100)/self.cons
            else: self.dirX = random.randint(100, 125)/self.cons
    
    def draw_person(self):
        ellipse(self.xLoc, self.yLoc, 5, 5)

def setup():
    global p
    size(640, 480)
    for i in range(0, 100):
        p.append(Person(random.randint(100, 300), random.randint(100, 300), "S"))

def draw():
    global p
    background(255, 255, 255)
    fill(0, 0, 0)
    for person in p:
        person.move()
        person.draw_person()
