import threading
import time

# Buffer size is 100 shoes, or 50 pairs
BUFFER_MAX_SIZE = 100  # Maximum number of shoes
BUFFER_MAX_PAIRS = BUFFER_MAX_SIZE // 2  # Maximum number of pairs

# Semaphores
mutex = threading.Semaphore(1)  # X semaphore for mutual exclusion, initially 1
empty = threading.Semaphore(BUFFER_MAX_SIZE)  # Y semaphore for counting empty pair spaces, initially 50 pairs
full = threading.Semaphore(0)  # Z semaphore for counting full spaces, initially 0

buffer = []  # Shared buffer


def producer1():
    pair_number = 0
    while True:
        time.sleep(1.8)  # Simulate time taken to produce a pair of shoes

        # Produce a pair (left and right shoe)
        pair_number += 1
        left_shoe = f'Left Shoe {pair_number}'
        right_shoe = f'Right Shoe {pair_number}'

        empty.acquire()
        empty.acquire()  # Decrease twice for two places

        mutex.acquire()

        # Place the left shoe in the buffer
        buffer.append(left_shoe)
        # Place the right shoe in the buffer
        buffer.append(right_shoe)

        print(f'Produced by 1: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2}\n')

        mutex.release()

        full.release()
        full.release()


def producer2():
    pair_number = 0
    while True:
        time.sleep(1.5)  # Simulate time taken to produce a pair of shoes

        # Produce a pair (left and right shoe)
        pair_number += 1
        left_shoe = f'Left {pair_number}'
        right_shoe = f'Right {pair_number}'

        empty.acquire()
        empty.acquire()  # Decrease twice for two places

        mutex.acquire()

        # Place the left shoe in the buffer
        buffer.append(left_shoe)
        # Place the right shoe in the buffer
        buffer.append(right_shoe)

        print(f'Produced by 1: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2}\n')

        mutex.release()

        full.release()
        full.release()


def producer3():
    pair_number = 0
    while True:
        time.sleep(1.9)  # Simulate time taken to produce a pair of shoes

        # Produce a pair (left and right shoe)
        pair_number += 1
        left_shoe = f'L {pair_number}'
        right_shoe = f'R {pair_number}'

        empty.acquire()
        empty.acquire()  # Decrease twice for two places

        mutex.acquire()

        # Place the left shoe in the buffer
        buffer.append(left_shoe)
        # Place the right shoe in the buffer
        buffer.append(right_shoe)

        print(f'Produced by 3: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after production: {len(buffer)/2}\n')

        mutex.release()

        full.release()
        full.release()


def consumer():
    while True:
        full.acquire()
        full.acquire()  # Decrease twice for two places

        mutex.acquire()

        # Fetch left shoe from the buffer
        left_shoe = buffer.pop(0)
        # Fetch right shoe from the buffer
        right_shoe = buffer.pop(0)

        print(f'Consumed: [{left_shoe}, {right_shoe}]')
        print(f'Buffer state: {buffer}')
        print(f'Pairs in buffer after consumption: {len(buffer)/2}\n')

        mutex.release()

        empty.release()
        empty.release()

        time.sleep(1.2)  # Simulate time taken to package and ship a pair of shoes


# Create and start producers and consumer threads
producer1_thread = threading.Thread(target=producer1)
producer2_thread = threading.Thread(target=producer2)
producer3_thread = threading.Thread(target=producer3)
consumer_thread = threading.Thread(target=consumer)

producer1_thread.start()
producer2_thread.start()
producer3_thread.start()
consumer_thread.start()

producer1_thread.join()
producer2_thread.join()
producer3_thread.join()
consumer_thread.join()
