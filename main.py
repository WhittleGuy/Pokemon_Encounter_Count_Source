from pynput import keyboard
from pynput.keyboard import Listener

FILE = './count.txt'
STEP_SIZE = 2


class Counter:
    def __init__(self, file, step):
        self.file = file
        self.step = step

    def keyPress(self, key):
        currKey = ''
        try:
            currKey = str(key.char)
        except:
            if key == keyboard.Key.up:
                currKey = '{UP}'
            elif key == keyboard.Key.down:
                currKey = '{DOWN}'

        if currKey != '' and currKey != None:
            count = ''
            with open(self.file, 'r+') as text:
                count = text.readline()
            with open(self.file, 'w+') as text:
                if currKey == '{UP}':
                    count = str(int(count) + self.step)
                elif currKey == '{DOWN}':
                    count = str(int(count) - self.step)
                text.write(count)

    def run(self):
        keyboardListener = keyboard.Listener(on_press=self.keyPress)
        keyboardListener.start()
        input()


if __name__ == '__main__':
    EncounterMachine = Counter(FILE, STEP_SIZE)
    EncounterMachine.run()
