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

def roomInit(name):
    # Rooms will always have two properties: neighbors of the room and name of the room.
    # The neighbors is a dictionary that contain the next room name in the direction of North(0), South(1), ...
    room = {}
    room['neighbors'] = {}
    room['name'] = name
    return room

def flatInit():
    # The only property for flat right now is rooms, that contains its rooms.
    flat = {}
    flat['rooms'] = {}
    return flat

# The functions starting with flatXXX() always work on a flat, so the first parameter is the flat to modify/query.
def flatAddRoom(flat, name):
    flat['rooms'][name] = roomInit(name)

def flatAddDoor(flat, room1, room2, dir):
    for r in [room1, room2]:
        if r not in flat['rooms']:
            flatAddRoom(flat, r)
    flat['rooms'][room1]['neighbors'][dir] = room2
    flat['rooms'][room2]['neighbors'][dir180(dir)] = room1

def flatRoomCount(flat):
    return len(flat['rooms']) - 2

# Player properties:
#   - the flat dictionary they are in
#   - a beenhere dictionary, so we know for each player where have they been (maybe we will be multiplayer layer)
def playerInit(flat, loc):
    player = {}
    player['flat'] = flat
    player['beenhere'] = {}
    playerSetLoc(player, loc)
    return player

# Player functions all start with playerXXX() similarly to flat, and they all get the player dictionary first.
def playerSetLoc(player, loc):
    player['loc'] = loc
    player['beenhere'][loc] = True

def playerGo(player, dir):
    neighbors = player['flat']['rooms'][player['loc']]['neighbors']
    if dir not in neighbors:
        return None

    playerSetLoc(player, neighbors[dir])

    return player['loc']

def playerScore(player):
    return len(player['beenhere']) - 2

def playerReport(player):
    print(f"Here you are: {player['loc']}")
    print()

# ba -> be
# ^     ^
# k  -> lr
# ^
# entrance

# flatAddDoor adds the rooms on demand, so we only need to construct the flat by doors...
flat = flatInit()
flatAddDoor(flat, "entrance", "kitchen", NORTH)
flatAddDoor(flat, "kitchen", "livingroom", EAST)
flatAddDoor(flat, "entrance", "exit", SOUTH)
flatAddDoor(flat, "kitchen", "bathroom", NORTH)
flatAddDoor(flat, "bathroom", "bedroom", EAST)
flatAddDoor(flat, "livingroom", "bedroom", NORTH)

print(f"Number of rooms: {flatRoomCount(flat)}")

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

# With all these helper functions the main program is kinda readable...
player = playerInit(flat, "entrance")
while True:
    playerReport(player)
    direction = whereToGo()
    newLoc = playerGo(player, direction)

    if newLoc is None:
        print("There is a wall here. Choose another direction.")
        continue

    if newLoc == "exit":
        print(f"You've left the flat.")
        print(f"Your score: {playerScore(player)}/{flatRoomCount(flat)}")
        print()
        break
