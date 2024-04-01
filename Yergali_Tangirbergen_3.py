import threading
import time

# Buffer size is 100 shoes, or 50 pairs
BUFFER_MAX_SIZE = 100  # Maximum number of shoes
BUFFER_MAX_PAIRS = BUFFER_MAX_SIZE // 2  # Maximum number of pairs

# Semaphores
mutex = threading.Semaphore(1)  # Semaphore for mutual exclusion, initially 1
empty = threading.Semaphore(BUFFER_MAX_SIZE)  # Semaphore for counting empty spaces, initially 100 spaces
full = threading.Semaphore(0)  # Semaphore for counting full spaces, initially 0

buffer = []  # Shared buffer


# Producer 1 function
def producer1():
    pair_number = 0
    while True:
        time.sleep(1.8)  # Simulate time taken to produce a pair of shoes

        # Produce a pair (left and right shoe)
        pair_number += 1
        left_shoe = f'Left Shoe {pair_number}'
        right_shoe = f'Right Shoe {pair_number}'

        # Acquire two empty spaces
        empty.acquire()
        empty.acquire()

        mutex.acquire()  # Acquire mutex for accessing buffer

        # Place the left shoe in the buffer
        buffer.append(left_shoe)
        # Place the right shoe in the buffer
        buffer.append(right_shoe)

        # Display production details
        print(f'Produced by 1: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2} of {BUFFER_MAX_PAIRS}\n')

        mutex.release()  # Release mutex after accessing buffer

        # Release two full spaces
        full.release()
        full.release()


# Producer 2 function (similar to producer 1)
def producer2():
    pair_number = 0
    while True:
        time.sleep(1.5)  # Simulate time taken to produce a pair of shoes

        pair_number += 1
        left_shoe = f'Left {pair_number}'
        right_shoe = f'Right {pair_number}'

        empty.acquire()
        empty.acquire()

        mutex.acquire()

        buffer.append(left_shoe)
        buffer.append(right_shoe)

        print(f'Produced by 2: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2} of {BUFFER_MAX_PAIRS}\n')

        mutex.release()

        full.release()
        full.release()


# Producer 3 function (similar to producer 1)
def producer3():
    pair_number = 0
    while True:
        time.sleep(1.9)  # Simulate time taken to produce a pair of shoes

        pair_number += 1
        left_shoe = f'L {pair_number}'
        right_shoe = f'R {pair_number}'

        empty.acquire()
        empty.acquire()

        mutex.acquire()

        buffer.append(left_shoe)
        buffer.append(right_shoe)

        print(f'Produced by 3: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2} of {BUFFER_MAX_PAIRS}\n')

        mutex.release()

        full.release()
        full.release()


# Consumer function
def consumer():
    while True:
        full.acquire()  # Wait for a full space
        full.acquire()  # Wait for another full space

        mutex.acquire()

        # Fetch left shoe from the buffer
        left_shoe = buffer.pop(0)
        # Fetch right shoe from the buffer
        right_shoe = buffer.pop(0)

        print(f'Consumed: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after consumption: {len(buffer)/2} of {BUFFER_MAX_PAIRS}\n')

        mutex.release()

        empty.release()  # Release an empty space
        empty.release()  # Release another empty space

        time.sleep(1.6)  # Simulate time taken to package and ship a pair of shoes


# Create producer and consumer threads
producer1_thread = threading.Thread(target=producer1)
producer2_thread = threading.Thread(target=producer2)
producer3_thread = threading.Thread(target=producer3)
consumer_thread = threading.Thread(target=consumer)

# Start producer and consumer threads
producer1_thread.start()
producer2_thread.start()
producer3_thread.start()
consumer_thread.start()

# Wait for all threads to finish
producer1_thread.join()
producer2_thread.join()
producer3_thread.join()
consumer_thread.join()
