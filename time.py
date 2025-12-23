import time
import numpy as np


def fib(n):
    if n<=1:
        return n
    else:
        return(fib(n-1)+fib(n-2))


def main():
    num = np.random.randint(1,25)
    print("%dth fibonacci number is: %d" %(num,fib(num)))


starttime=time.time()
timeout=time.time()+60*2

while time.time() <= timeout:
    try:
        main()
        time.sleep(5-(time.time()-starttime)%5.0)
    except KeyboardInterrupt:
        print("Keyboard exception")
        exit()