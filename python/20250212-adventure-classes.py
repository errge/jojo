#!/usr/bin/python3

# sudo apt install python3-termcolor
from termcolor import colored

# colors: red, green, yellow, blue, magenta, cyan, white
def rainbow(text,colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]):
    colorsi = 0
    rainbowtext = ""
    for i in text:
        if i != " ":
            rainbowtext += colored(i,colors[colorsi])
            colorsi = (colorsi+1) % len(colors)
        else:
            rainbowtext += i
    return rainbowtext

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
def dir180(dir):
    return (dir + 2) % 4

class Room:
    def __init__(self, name):
        self.neighbors = {}
        self.name = name

class Flat:
    def __init__(self):
        self.rooms = {}

    def addRoom(self, name):
        self.rooms[name] = Room(name)

    def addDoor(self, room1, room2, dir):
        for r in [room1, room2]:
            if r not in self.rooms:
                self.addRoom(r)
        self.rooms[room1].neighbors[dir] = room2
        self.rooms[room2].neighbors[dir180(dir)] = room1

    def roomCount(self):
        return len(self.rooms)-2

class Player:
    def __init__(self, flat, loc):
        self.flat = flat
        self.beenhere = {}
        self.setLoc(loc)

    def setLoc(self, loc):
        self.loc = loc
        self.beenhere[loc] = True

    def go(self, dir):
        neighbors = self.flat.rooms[self.loc].neighbors
        if dir not in neighbors:
            return None

        self.setLoc(neighbors[dir])

        return self.loc

    def score(self):
        return len(self.beenhere) - 2

    def report(self):
        print(f"Here you are: {self.loc}")
        print()

# ba -> be
# ^     ^
# k  -> lr
# ^
# ee
flat = Flat()
flat.addDoor("entrance", "kitchen", NORTH)
flat.addDoor("kitchen", "livingroom", EAST)
flat.addDoor("entrance", "exit", SOUTH)
flat.addDoor("kitchen", "bathroom", NORTH)
flat.addDoor("bathroom", "bedroom", EAST)
flat.addDoor("livingroom", "bedroom", NORTH)

print(f"Number of rooms: {flat.roomCount()}")

def whereToGo():
    while True:
        dir = input(rainbow("Which direction do you want to go? (North, South, West, East) "))
        match dir:
            case 'North':
                return NORTH
            case 'East':
                return EAST
            case 'South':
                return SOUTH
            case 'West':
                return WEST
            case _:
                print(rainbow("Be realistic.",colors = ["red","white","green"]))
                print()

player = Player(flat, "entrance")
while True:
    player.report()
    direction = whereToGo()
    newLoc = player.go(direction)

    if newLoc is None:
        print("There is a wall here. Choose another direction.")
        continue

    if newLoc == "exit":
        print(f"You've left the flat.")
        print(f"Your score: {player.score()}/{flat.roomCount()}")
        print()
        break
