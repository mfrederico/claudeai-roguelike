from map import GameMap
from entities import Player, Monster, Chest
from input_handler import InputHandler
from message_log import MessageLog
from combat import Combat
import random
import config
import time

class Game:
    def __init__(self):
        self.map = GameMap(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.player = None
        self.monsters = None
        self.chests = None
        self.message_log = None
        self.input_handler = InputHandler()
        self.initialize_game()
        self.in_combat = False
        self.in_chest_screen = False
        self.current_combat = None
        self.current_chest = None

    def initialize_game(self):
        self.player = Player(config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2)
        self.monsters = self.spawn_monsters(config.NUM_MONSTERS)
        self.chests = self.spawn_chests(config.NUM_CHESTS)
        self.message_log = MessageLog()

    def spawn_chests(self, num_chests):
        chests = []
        for _ in range(num_chests):
            while True:
                x, y = random.randint(0, self.map.width - 1), random.randint(0, self.map.height - 1)
                if self.map.is_passable(x, y) and not any(m.x == x and m.y == y for m in self.monsters):
                    chests.append(Chest(x, y))
                    break
        return chests

    def open_chest(self):
        for chest in self.chests:
            if chest.x == self.player.x and chest.y == self.player.y:
                self.display_chest_screen(chest)
                return
        self.message_log.add("There's no chest here to open.")

    def display_chest_screen(self, chest):
        print('\033[H\033[J', end='')  # Clear screen
        print("=" * 40)
        print("You've found a treasure chest!")
        print("=" * 40)

        if chest.item:
            print(f"\nInside, you find: {chest.item.get_description()}")
            print(f"\nYour current armor: {self.player.armor or 'None'}")
            print("\nDo you want to equip this armor?")
            print("Press 'Y' to equip, or any other key to leave it.")
            
            action = self.input_handler.get_key().lower()
            if action == 'y':
                result = chest.item.use(self.player)
                self.message_log.add(result)
            else:
                self.message_log.add("You decide to leave the armor.")
        else:
            print("\nThe chest is empty.")
        
        self.chests.remove(chest)
        print("\nPress any key to continue...")
        self.input_handler.get_key()


    def update(self):
        if self.in_combat:
            combat_result = self.handle_combat()
            if combat_result is not None:
                return combat_result
        elif self.in_chest_screen:
            chest_result = self.handle_chest()
            if chest_result is not None:
                return chest_result
        else:
            action = self.input_handler.get_action()
            if action == 'quit':
                return False
            elif action == 'restart':
                self.initialize_game()
                self.message_log.add("Game restarted with the same map.")
            elif action in ['up', 'down', 'left', 'right']:
                dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[action]
                new_x, new_y = self.player.x + dx, self.player.y + dy
                if self.map.is_passable(new_x, new_y):
                    self.player.move(dx, dy)
                    healed_amount = self.player.heal_by_moving()
                    move_message = f"Player moved {action}"
                    if healed_amount > 0:
                        move_message += f" and healed {healed_amount:.2f} HP"
                    self.message_log.add(move_message)
                    self.update_monsters()
                    self.check_for_combat()
                    self.check_for_chest()
                else:
                    self.message_log.add("Cannot move there")
            elif action == 'open':
                self.open_chest()
        return True

    def check_for_chest(self):
        for chest in self.chests:
            if chest.x == self.player.x and chest.y == self.player.y:
                self.message_log.add("You see a chest here. Press 'O' to open it.")

    def open_chest(self):
        for chest in self.chests:
            if chest.x == self.player.x and chest.y == self.player.y:
                self.current_chest = chest
                self.in_chest_screen = True
                return
        self.message_log.add("There's no chest here to open.")

    def handle_chest(self):
        if not self.current_chest:
            self.in_chest_screen = False
            return None

        print('\033[H\033[J', end='')  # Clear screen
        print("=" * 40)
        print("You've found a treasure chest!")
        print("=" * 40)

        if self.current_chest.item:
            print(f"\nInside, you find: {self.current_chest.item.get_description()}")
            print(f"\nYour current armor: {self.player.armor or 'None'}")
            print("\nDo you want to equip this armor?")
            print("Press 'Y' to equip, or any other key to leave it.")

            action = self.input_handler.get_key().lower()
            if action == 'y':
                result = self.current_chest.item.use(self.player)
                self.message_log.add(result)
            else:
                self.message_log.add("You decide to leave the armor.")
        else:
            print("\nThe chest is empty.")

        self.chests.remove(self.current_chest)
        print("\nPress any key to continue...")
        self.input_handler.get_key()

        self.in_chest_screen = False
        self.current_chest = None
        return None

    def spawn_monsters(self, num_monsters):
        monsters = []
        regions = self.divide_map_into_regions(config.REGION_DIVISIONS_X, config.REGION_DIVISIONS_Y)
        monsters_per_region = num_monsters // len(regions)
        
        for region in regions:
            for _ in range(monsters_per_region):
                monster = self.spawn_monster_in_region(region)
                if monster:
                    monsters.append(monster)
        
        # Spawn any remaining monsters randomly
        while len(monsters) < num_monsters:
            x, y = random.randint(0, self.map.width - 1), random.randint(0, self.map.height - 1)
            if self.map.is_passable(x, y) and not any(m.x == x and m.y == y for m in monsters):
                monsters.append(Monster(x, y))
        
        return monsters

    def divide_map_into_regions(self, num_x, num_y):
        regions = []
        region_width = self.map.width // num_x
        region_height = self.map.height // num_y
        
        for i in range(num_x):
            for j in range(num_y):
                x1 = i * region_width
                y1 = j * region_height
                x2 = min((i + 1) * region_width - 1, self.map.width - 1)
                y2 = min((j + 1) * region_height - 1, self.map.height - 1)
                regions.append((x1, y1, x2, y2))
        
        return regions

    def spawn_monster_in_region(self, region):
        x1, y1, x2, y2 = region
        for _ in range(config.MAX_SPAWN_ATTEMPTS):
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
            if self.map.is_passable(x, y):
                return Monster(x, y)
        return None

    def check_for_combat(self):
        for monster in self.monsters:
            if monster.x == self.player.x and monster.y == self.player.y:
                self.in_combat = True
                self.current_combat = Combat(self.player, monster)
                return


    def equip_armor(self):
        print("\nAvailable armor types:")
        for armor in config.ARMOR_TYPES:
            print(f"- {armor}")
        armor_choice = input("Enter the armor type you want to equip: ").capitalize()
        result = self.player.equip_armor(armor_choice)
        self.message_log.add(result)


    def handle_combat(self):
        self.current_combat.render_combat_screen()
        action = self.input_handler.get_combat_action()
        result = self.current_combat.handle_combat_turn(action)
        print(result)
        input("Press Enter to continue...")

        combat_over, message = self.current_combat.is_combat_over()
        if combat_over:
            print(message)
            input("Press Enter to continue...")
            self.in_combat = False
            if "defeated" in message.lower():
                if "You have been defeated!" in message:
                    self.message_log.add("Game Over! You have been defeated.")
                    display_gravestone()
                    return False
                else:
                    self.monsters.remove(self.current_combat.monster)
                    self.message_log.add(f"You defeated the {self.current_combat.monster.name}!")
            self.current_combat = None
        return None

    def update_monsters(self):
        for monster in self.monsters:
            if random.random() < config.MONSTER_MOVE_CHANCE:
                dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                new_x, new_y = monster.x + dx, monster.y + dy
                if self.map.is_passable(new_x, new_y):
                    monster.move(dx, dy)

    def run(self):
        while True:
            if not self.in_combat and not self.in_chest_screen:
                self.map.render(self.player, self.monsters, self.chests)
                self.message_log.display()
                print("\nUse WASD to move, O to open chests, Q to quit")
            if not self.update():
                break

def display_gravestone():
    gravestone = r"""
         .---.
        /     \
        |  R I P  |
        |   He    |
        |  Died   |
        | Playing |
        |   RPG   |
        =========
          \   /
           \ /
           |||
           |||
           |||
           |||
         \=====/

    Game Over!
    Press any key to exit...
    """
    print(gravestone)
    input()
