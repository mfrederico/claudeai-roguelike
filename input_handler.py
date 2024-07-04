import os

if os.name == 'nt':
    import msvcrt
else:
    import sys
    import tty
    import termios

class InputHandler:
    def get_key(self):
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8').lower()
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.lower()

    def get_action(self):
        key = self.get_key()
        if key == 'q':
            return 'quit'
        elif key == 'r':
            return 'restart'
        elif key in ['w', 'a', 's', 'd']:
            return {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}[key]
        elif key == 'o':
            return 'open'
        return None

    def get_combat_action(self):
        while True:
            key = self.get_key()
            if key in ['a', 'd', 'r']:
                return key
