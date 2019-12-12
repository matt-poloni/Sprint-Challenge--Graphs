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
    # While there are still rooms to process...
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
def branch():
    # While there's at least one deadend...
    while len(ones) > 0:
        # Reset the visited set in case it has leftover values
        global visited; visited = set()
        # Grab the ID and links of a random deadend
        # (ignore coordinates)
        id, (_, links) = ones.popitem()
        # Grab the only direction out of the deadend
        direction = [*links.keys()][0]
        # Initialize path (dirs) & rooms (IDs)
        path = [direction]
        rooms = [id]
        # While you're in (effectively) a hallway...
        while (id := links[direction]) in twos:
            # Grab exits
            links = twos[id][1]
            # Grab only the new direction (not where you came)
            direction = [d for d in links.keys() if d != opposite[direction]][0]
            # Add that direction to the path
            path.append(direction)
            # Add the room ID to rooms
            rooms.append(id)
            # Remove the room from available hallways
            del twos[id]
        # Grab the reversed path that got you to the deadend
        rev_path = [*reversed([opposite[d] for d in path])]
        # Grab the reversed rooms that got you to the deadend
        rev_rooms = [*reversed([r for r in rooms])]
        # For each room on the way to the deadend...
        for i, room in enumerate(rev_rooms):
            # If that room is a branching off point...
            # (ignore zero, our starting point)
            if room != 0 and room not in visited and room in branches:
                # For each existing branch from that room...
                for branch in branches[room].values():
                    # Grab the following index
                    nxt = i+1
                    # Insert the branched path at that index
                    rev_path[nxt:nxt] = branch['path']
                    # Insert the branched rooms at that index
                    rev_rooms[nxt:nxt] = branch['rooms']
                # Remove the branches for that room from availability
                del branches[room]
        # Grab the ID of the room you're returning to
        last_room = links[direction]
        # gone = rooms[0] # Just for debugging
        # Remove the pivot from the room list and add the return
        rooms = [*rooms[1:], last_room]
        # print(rev_path, path)
        # print(rev_rooms, gone, rooms)
        # Create the full-round trip path & rooms
        final_path = [*rev_path, *path]
        final_rooms = [*rev_rooms, *rooms]
        # If that ID already has other branches...
        if id in branches:
            # Add the path & rooms in the proper direction
            # (opposite because we just returned to that room)
            branches[id][opposite[direction]] = {
                'path': final_path,
                'rooms': final_rooms
            }
        else:
            # Otherwise, add the room as a branching-off point
            branches[id] = {
                opposite[direction]: {
                    'path': final_path,
                    'rooms': final_rooms
                }
            }
prune()
# print('ONES', len(ones))
# print('TWOS', len(twos))
# print('NODES', len(nodes))
while len(ones) > 0:
    branch()
    prune({**twos, **nodes})

pruned = World()
world.loadGraph({**twos, **nodes})
world.printRooms()

print('ONES', len(ones))
print('TWOS', len(twos))
print('NODES', len(nodes))
print(branches[0])
print(len(branches))


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
