#!/usr/bin/python
from pynput import keyboard
from pynput.keyboard import Listener

# Set text file and step parameters
FILE = './count.txt'
STEP_SIZE = 2

# Input all valid key presses and action
INCREMENT_LIST = ('Key.up', 'Key.right')
DECREMENT_LIST = ('Key.down', 'Key.left')


class Counter:
    def __init__(self, increment_list, decrement_list, file, step):
        count = None
        with open(file, 'r') as text:
            count = int(text.readline())

        self.increment_list = increment_list
        self.decrement_list = decrement_list
        self.file = file
        self.step = step
        self.count = count

    def keyPress(self, key):

        if self.active:
            action = None
            try:
                key = key.char
            except AttributeError:
                key = str(key)

            if key in INCREMENT_LIST:
                action = '{+}'
            elif key in DECREMENT_LIST:
                action = '{-}'
            self.change_count(action)

    def change_count(self, action):
        if action != None:
            with open(self.file, 'w') as text:
                if action == '{+}':
                    self.count = self.count + self.step
                elif action == '{-}':
                    self.count = self.count - self.step
                text.write(str(self.count))

    def run(self):
        keyboardListener = keyboard.Listener(on_press=self.keyPress)
        keyboardListener.start()
        input()


if __name__ == '__main__':
    EncounterMachine = Counter(INCREMENT_LIST, DECREMENT_LIST, FILE, STEP_SIZE)
    EncounterMachine.run()
