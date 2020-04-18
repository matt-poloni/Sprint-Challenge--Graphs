import unittest
import io
from ast import literal_eval
from contextlib import redirect_stdout

from adv import traversal_path
from room import Room
from player import Player
from world import World

class Test(unittest.TestCase):
    def setUp(self):
        file_path="maps/main_maze.txt"
        with open(file_path, "r") as f:
            map_file = f.read()

        self.world = World()
        self.room_graph = literal_eval(map_file)
        self.world.load_graph(self.room_graph)

        self.player = Player(self.world.starting_room)


    def test_valid(self):
        visited_rooms = set()
        visited_rooms.add(self.player.current_room)

        for move in traversal_path:
            print_trap = io.StringIO()
            # Supress print output
            with redirect_stdout(print_trap):
                self.player.travel(move)
                visited_rooms.add(self.player.current_room)

        self.assertEqual(len(visited_rooms), len(self.room_graph))


    def test_mvp(self):
        self.assertLessEqual(len(traversal_path), 2000)


    @unittest.skipIf(
        len(traversal_path) >= 960,
        "Traversal is longer than stretch threshold"
    )
    def test_stretch(self):
        self.assertLessEqual(len(traversal_path), 960)


if __name__ == '__main__':
    # Enable verbose output by default
    unittest.main(verbosity=2)