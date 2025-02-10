#!/usr/bin/python3

import sys

#    LT
#    KP
#    E

# hely
kitchen = {
    'name': 'Kitchen',
    'north': None, # living_room
    'south': None, # entrance
    'east': None, # pantry,
    'west': None
}

entrance = {
    'name': 'Entrance',
    'north': kitchen,
    'south': None,
    'east': None,
    'west': None
}

living_room = {
    'name': 'Living room',
    'north': None,
    'south': kitchen,
    'east': None, # toilet
    'west': None
}

pantry = {
    'name': 'Pantry',
    'north': None,
    'south': None,
    'east': None,
    'west': kitchen
}

toilet = {
    'name': 'Toilet',
    'north': None,
    'south': None,
    'east': None,
    'west': living_room
}

living_room['east'] = toilet
kitchen['north'] = living_room
kitchen['south'] = entrance
kitchen['east'] = pantry

# terkep: hely nev -> hely
rooms = {}
for loc in [toilet, pantry, living_room, entrance, kitchen]:
    rooms[loc['name']] = loc

def report(location_name, visited):
    print(f'You are at location {location_name}, visited {len(visited)} locations so far')
    # if then elsek, vicces uzenetekkel a locationokrol

def wheretogo():
    while True:
        print('Where do you want to go? (n, s, e, w) ', end='')
        user_response = input()
        match user_response:
            case 'n':
                return 'north'
            case 's':
                return 'south'
            case 'w':
                return 'west'
            case 'e':
                return 'east'
            case _:
                print('Please select correct direction!')


def main():
    location_name = 'Entrance'
    visited = {
        location_name: True
    }
    while True:
        report(location_name, visited)
        if len(visited) == len(rooms):
            break
        direction = wheretogo()
        new_location = rooms[location_name][direction]
        if new_location is None:
            print('There is only a wall in that direction')
            continue
        location_name = new_location['name']
        visited[location_name] = True
    print('You won, you visited all locations')

main()
