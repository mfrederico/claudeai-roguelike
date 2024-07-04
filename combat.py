import random
import config
from entities import Player

class Combat:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def render_combat_screen(self):
        print('\033[H\033[J', end='')  # Clear screen
        player_stats = self.get_entity_stats(self.player)
        monster_stats = self.get_entity_stats(self.monster)

        max_lines = max(len(player_stats), len(monster_stats))
        
        print("=" * 80)
        print(f"{'PLAYER':^39}|{'MONSTER':^40}")
        print("=" * 80)

        for i in range(max_lines):
            player_line = player_stats[i] if i < len(player_stats) else " " * 39
            monster_line = monster_stats[i] if i < len(monster_stats) else " " * 40
            print(f"{player_line:<39}|{monster_line:<40}")

        print("=" * 80)
        print("\nActions: [A]ttack, [D]efend, [R]un")

    def get_entity_stats(self, entity):
        stats = [
            f"Name: {entity.name}",
            f"HP: {entity.attributes['hit_points']}",
            f"Power: {entity.attributes['power']}",
            f"Magic: {entity.attributes['magic']}",
            f"Clarity: {entity.attributes['clarity']}",
        ]
        if isinstance(entity, Player):
            stats.extend([
                f"XP: {entity.attributes['experience']}",
                f"Level: {entity.attributes['level']}",
            ])
        return stats

    def player_attack(self):
        damage = random.randint(1, self.player.attributes['power'])
        self.monster.attributes['hit_points'] -= damage
        return f"You deal {damage} damage to the {self.monster.name}!"

    def monster_attack(self):
        damage = random.randint(1, self.monster.attributes['power'])
        self.player.attributes['hit_points'] -= damage
        return f"The {self.monster.name} deals {damage} damage to you!"

    def run(self):
        escape_chance = random.random()
        if escape_chance > 0.5:
            return True, "You successfully escaped!"
        else:
            return False, "You failed to escape!"

    def is_combat_over(self):
        if self.player.get_hit_points() <= 0:
            self.player.set_hit_points(0)  # Ensure HP doesn't go negative
            return True, "You have been defeated!"
        elif self.monster.get_hit_points() <= 0:
            xp_gain = self.monster.attributes['level'] * config.XP_GAIN_MULTIPLIER
            leveled_up = self.player.gain_xp(xp_gain)
            message = f"You have defeated the {self.monster.name}! You gain {xp_gain} XP!"
            if leveled_up:
                message += f"\nCongratulations! You've reached level {self.player.attributes['level']}!"
                message += f"\nYou've been fully healed to {self.player.get_hit_points():.2f} HP!"
            return True, message
        return False, ""

    def handle_combat_turn(self, action):
        if action == 'a':
            result = self.player_attack()
            monster_action = self.monster_attack()
            return f"{result}\n{monster_action}"
        elif action == 'd':
            # Implement defend logic here
            return "You defend against the monster's attack."
        elif action == 'r':
            escaped, message = self.run()
            if escaped:
                return message
            else:
                monster_action = self.monster_attack()
                return f"{message}\n{monster_action}"
        else:
            return "Invalid action. Please choose [A]ttack, [D]efend, or [R]un."

