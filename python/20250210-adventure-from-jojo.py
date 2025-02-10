# sudo apt install python3-termcolor
from termcolor import colored
# colors: red, green, yellow, blue, magenta, cyan, white

rooms = {}

def dir180(dir):
    if dir == "North":
        return "South"
    elif dir == "South":
        return "North"
    elif dir == "West":
        return "East"
    elif dir == "East":
        return "West"

def addRoom(roomname):
    newroom = {
        "name": roomname,
        "North": None,
        "South": None,
        "West": None,
        "East": None,
        "beenhere": False
    }
    rooms[roomname] = newroom
    return newroom

def addDoor(room1,room2,dir):
    room1[dir] = room2
    room2[dir180(dir)] = room1

entrance = addRoom("entrance")
kitchen = addRoom("kitchen")
livingroom = addRoom("livingroom")
exit = addRoom("exit")
bathroom = addRoom("bathroom")
bedroom = addRoom("bedroom")

addDoor(entrance,kitchen,"North")
addDoor(kitchen,livingroom,"East")
addDoor(entrance,exit,"South")
addDoor(kitchen,bathroom,"North")
addDoor(bathroom,bedroom,"East")
addDoor(livingroom,bedroom,"North")

print(f"Number of rooms: {len(rooms)-2}")

def report(loc):
    print(f"Here you are: {loc}")
    print()

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


def whereToGo():
    while True:
        dir = input(rainbow("Which direction do you want to go? (North, South, West, East) "))
        if dir == "North" or dir == "South" or dir == "East" or dir == "West":
            return dir
        else:
            print(rainbow("Be realistic.",colors = ["red","white","green"]))
            print()

# colors: red, green, yellow, blue, magenta, cyan, white

urloc = "entrance"
while True:
    report(urloc)
    rooms[urloc]["beenhere"] = True
    direction = whereToGo()
    newLoc = rooms[urloc][direction]
    if newLoc is None:
        print("There is a wall here. Choose another direction.")
    elif newLoc["name"] == "exit":
        score = 0
        print(f"You've left the flat.")
        for i in rooms.keys():
            if rooms[i]["beenhere"]:
                score += 1
        print(f"Your score: {score-1}/{len(rooms)-2}")
        print()
        break
    else:
        urloc = newLoc["name"]
