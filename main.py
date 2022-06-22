#!/usr/local/bin/pipenv
from pynput import keyboard
from pynput.keyboard import Listener as KListener
from pynput.mouse import Listener as MListener
from PIL import Image, ImageGrab
import time

FILE = './count.txt'
PERCENT_FILE = './percent.txt'
PHASE_FILE = './last_phase.dat'
SELECTION_AREA_CORNERS = [()]
STEP_SIZE = 2
ENCOUNTER_CHANCE = 4096
INCREMENT_LIST = ('Key.up', 'Key.right')
DECREMENT_LIST = ('Key.down', 'Key.left')


class Counter:
    def __init__(self, step, increment_list, decrement_list, file, percent_file, phase_file, chance):
        count = None
        with open(file, 'r') as text:
            count = int(text.readline())

        self.increment_list = increment_list
        self.decrement_list = decrement_list
        self.file = file
        self.percent_file = percent_file
        self.phase_file = phase_file
        self.chance = chance
        self.step = step
        self.count = count

    def on_click(self, x, y, _, pressed):
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
            if action == '{+}':
                self.count += self.step
            elif action == '{-}':
                self.count -= self.step
            with open(self.file, 'w') as text:
                text.write(str(self.count))
            with open(self.percent_file, 'w') as percent:
                with open(self.phase_file, 'r') as phase:
                    last_phase = int(phase.readline())
                    per = f'{(self.count-last_phase)/self.chance:.3%}'
                    percent.write(per)

    def run(self):
        print('Please select two opposite corners of the area you want to watch')
        with MListener(on_click=self.on_click) as listener:
            listener.join()
        print(f'Monitoring {SELECTION_AREA_CORNERS[0]}...')
        print('Press <ctrl+c> to quit...')
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
    AutoCounter = Counter(STEP_SIZE, INCREMENT_LIST, DECREMENT_LIST,
                          FILE, PERCENT_FILE, PHASE_FILE, ENCOUNTER_CHANCE)
    AutoCounter.run()
