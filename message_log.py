
class MessageLog:
    def __init__(self, max_messages=5):
        self.messages = []
        self.max_messages = max_messages

    def add(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def display(self):
        print("\nMessage Log:")
        for message in self.messages:
            print(message)
