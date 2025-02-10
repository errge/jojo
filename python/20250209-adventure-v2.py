#!/usr/bin/python3

import sys

#    LT
#    KP
#    E

rooms = {}

def add_room(name, north = None, south = None, east = None, west = None):
    def ensure_room(name):
        if name not in rooms:
            rooms[name] = {
                'name': name,
                'north': None,
                'south': None,
                'east': None,
                'west': None
            }
    def link_rooms(room, other, there, back):
        if other is not None:
            rooms[room][there] = rooms[other]
            rooms[other][back] = rooms[room]

    for r in [name, north, south, east, west]:
        if r is not None:
            ensure_room(r)

    link_rooms(name, north, 'north', 'south')
    link_rooms(name, south, 'south', 'north')
    link_rooms(name, east, 'east', 'west')
    link_rooms(name, west, 'west', 'east')

add_room('Entrance', north = 'Kitchen')
add_room('Kitchen', north = 'Living room', east = 'Pantry')
add_room('Living room', east = 'Toilet')

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
