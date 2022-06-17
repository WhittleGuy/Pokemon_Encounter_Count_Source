#!/usr/local/bin/pipenv
from pynput import keyboard
from pynput.keyboard import Listener as KListener
from pynput.mouse import Listener as MListener
from PIL import Image, ImageGrab
import time

FILE = './count.txt'
SELECTION_AREA_CORNERS = [()]
STEP_SIZE = 2
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

    def on_click(self, x, y, button, pressed):
        if pressed:
            SELECTION_AREA_CORNERS[0] += (x, y)
        if len(SELECTION_AREA_CORNERS[0]) >= 4:
            return False

    def keyPress(self, key):
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
        print('Please select two opposite corners of the area you want to watch')
        with MListener(on_click=self.on_click) as listener:
            listener.join()

        keyboardListener = KListener(on_press=self.keyPress)
        keyboardListener.start()

        while True:
            image = ImageGrab.grab(bbox=SELECTION_AREA_CORNERS[0])
            cols = Image.Image.getcolors(image)
            if cols is not None and len(cols) == 1:
                if cols[0][1] == (255, 255, 255):
                    self.change_count('{+}')
                    time.sleep(5)
            else:
                time.sleep(0.125)


if __name__ == '__main__':
    AutoCounter = Counter(INCREMENT_LIST, DECREMENT_LIST, FILE, STEP_SIZE)
    AutoCounter.run()
