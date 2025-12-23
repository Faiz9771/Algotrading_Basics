#Threading basics
#a lightweight process


import threading 
import numpy as np
import time

def rand_Gen():
    for a in range(20):
        if event.is_set():
            break
        else:
            print(a)
            time.sleep(1)

event = threading.Event()
thr2 = threading.Thread(target=rand_Gen)
#U wont see the diff on ide
#better try it out on the temrinal

thr2.daemon=True
thr2.start()

def greet():
    for i in range(10):
        print("hello ")
        time.sleep(1)

greet()
event.set()

