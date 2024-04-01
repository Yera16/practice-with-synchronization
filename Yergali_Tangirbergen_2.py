from threading import Lock, Thread
from time import sleep

class SharedCounter:
    def __init__(self):
        # Initializing the shared counter
        self.counter = 50
        # Initializing two locks for synchronization
        self.lock1 = Lock()
        self.lock2 = Lock()

    # Method for process 1 to increment the shared counter
    def process1(self):
        # Acquiring lock 1 to ensure exclusive access
        self.lock2.acquire()
        try:
            # Reading the current value of the counter
            register = self.counter
            # Incrementing the counter
            register += 10
            # Simulating some work with sleep
            sleep(1)
            # Updating the shared counter
            self.counter = register
        finally:
            # Releasing lock 1 to allow other threads to access the shared resource
            self.lock2.release()

    # Method for process 2 to decrement the shared counter
    def process2(self):
        # Acquiring lock 2 to ensure exclusive access
        self.lock1.acquire()
        try:
            # Reading the current value of the counter
            register = self.counter
            # Decrementing the counter
            register -= 10
            # Simulating some work with sleep
            sleep(1)
            # Updating the shared counter
            self.counter = register
        finally:
            # Releasing lock 2 to allow other threads to access the shared resource
            self.lock1.release()

# Creating an instance of SharedCounter
shared_counter = SharedCounter()

# Creating threads for each process
thread1 = Thread(target=shared_counter.process1)
thread2 = Thread(target=shared_counter.process2)

# Starting the threads
thread2.start()  # Process 2 starts first
thread1.start()  # Process 1 starts after Process 2

# Waiting for both threads to finish execution
thread2.join()
thread1.join()

print(shared_counter.counter)
