from pynput import keyboard
from pynput.keyboard import Listener


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
            with open(self.file, 'r') as text:
                count = text.readline()
            if currKey == '{UP}':
                with open(self.file, 'w') as text:
                    count = str(int(count) + self.step)
                    text.write(count)
            elif currKey == '{DOWN}':
                with open(self.file, 'w') as text:
                    count = str(int(count) - self.step)
                    text.write(count)

    def run(self):
        keyboardListener = keyboard.Listener(on_press=self.keyPress)
        keyboardListener.start()
        input()


EncounterMachine = Counter('./count.txt', 2)
EncounterMachine.run()
