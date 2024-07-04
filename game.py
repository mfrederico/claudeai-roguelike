from map import GameMap
from entities import Player, Monster
from input_handler import InputHandler
from message_log import MessageLog
import random

class Game:
    def __init__(self):
        self.map = GameMap(160, 90)
        self.player = Player(self.map.width // 2, self.map.height // 2)
        self.monsters = self.spawn_monsters(5)
        self.message_log = MessageLog()
        self.input_handler = InputHandler()

    def spawn_monsters(self, num_monsters):
        monsters = []
        for _ in range(num_monsters):
            while True:
                x, y = random.randint(0, self.map.width - 1), random.randint(0, self.map.height - 1)
                if self.map.is_passable(x, y):
                    monsters.append(Monster(x, y))
                    break
        return monsters

    def update(self):
        action = self.input_handler.get_action()
        if action == 'quit':
            return False
        elif action in ['up', 'down', 'left', 'right']:
            dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[action]
            new_x, new_y = self.player.x + dx, self.player.y + dy
            if self.map.is_passable(new_x, new_y):
                self.player.move(dx, dy)
                self.message_log.add(f"Player moved {action}")
                self.update_monsters()
            else:
                self.message_log.add("Cannot move there")
        return True

    def update_monsters(self):
        for monster in self.monsters:
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            new_x, new_y = monster.x + dx, monster.y + dy
            if self.map.is_passable(new_x, new_y):
                monster.move(dx, dy)

    def run(self):
        while True:
            self.map.render(self.player, self.monsters)
            self.message_log.display()
            if not self.update():
                break

