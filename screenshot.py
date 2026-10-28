import pyscreeze
import time
name = input('Enter the name image')
time.sleep(2)
eval(f'image1 = pyscreeze.screenshot("{name}.png")')