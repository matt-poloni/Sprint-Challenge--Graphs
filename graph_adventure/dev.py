from room import Room
from player import Player
from world import World
from adv import rg_3, rg_9, rg_12, rg_18, rg_500

import random

# Load world
world = World()

roomGraph = rg_500
world.loadGraph(roomGraph)
world.printRooms()
player = Player("Matt Poloni", world.startingRoom)


# FILL THIS IN
opposite = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
ones, twos, nodes, branches, cycles = {}, {}, {}, {}, {}
visited = set()
def prune(include=None):
    # By default, consider the whole graph
    if include is None:
        include = roomGraph
    # Initialize with all rooms that need to be covered
    remaining = set(include.keys())
    # Reset deadends (rooms w/ 1 link)
    global ones; ones = {}
    # Reset hallways (rooms w/ 2 links)
    global twos; twos = {}
    # Reset nodes (rooms w/ > 2 links)
    global nodes; nodes = {}
    # While there are still rooms to process
    while len(remaining) > 0:
        # Randomly select a remaining room
        id = remaining.pop()
        # Grab the (x, y) pair (for intermediate visuals)
        xy = roomGraph[id][0]
        # Grab all immediate connections in coverage area
        links = {d: i for (d, i) in roomGraph[id][1].items() if i in include}
        # Count number of relevant connections
        num_links = len(links)
        if num_links == 1:
            # Mark as deadend
            ones[id] = [xy, links]
        elif num_links == 2:
            # Mark as hallway
            twos[id] = [xy, links]
        elif num_links > 2:
            # Mark as node
            nodes[id] = [xy, links]
prune()
print('ONES', len(ones))
print('TWOS', len(twos))
print('NODES', len(nodes))
while len(ones) > 0:
    prune({**twos, **nodes})
print('ONES', len(ones))
print('TWOS', len(twos))
print('NODES', len(nodes))
traversalPath = []


# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
