import threading

# The buffer and its maximum capacity
buffer = [None] * 100
MAX_CAPACITY = 100

# The semaphores
semaphore_x = threading.Semaphore(1)  # Mutual exclusion semaphore
semaphore_y = threading.Semaphore(0)  # Count of filled slots
semaphore_z = threading.Semaphore(MAX_CAPACITY)  # Count of empty slots


def producer():
    global buffer
    # Producer loop
    while True:
        # Produce a pair of shoes (left and right)
        left_shoe, right_shoe = 'Left Shoe', 'Right Shoe'

        semaphore_z.acquire()  # Decrement empty slots count
        semaphore_z.acquire()  # Decrement for the second shoe

        semaphore_x.acquire()  # Enter critical section
        try:
            # Find the first available two consecutive empty slots
            for i in range(0, MAX_CAPACITY, 2):
                if buffer[i] is None and buffer[i + 1] is None:
                    buffer[i], buffer[i + 1] = left_shoe, right_shoe
                    break
                print(buffer)
        finally:
            semaphore_x.release()  # Leave critical section

        semaphore_y.release()  # Increment filled slots count
        semaphore_y.release()  # Increment for the second shoe


def consumer():
    global buffer
    # Consumer loop
    while True:
        semaphore_y.acquire()  # Decrement filled slots count
        semaphore_y.acquire()  # Decrement for the second shoe

        semaphore_x.acquire()  # Enter critical section
        try:
            # Fetch and remove a pair of shoes from the buffer
            for i in range(0, MAX_CAPACITY, 2):
                if buffer[i] is not None and buffer[i + 1] is not None:
                    buffer[i], buffer[i + 1] = None, None
                    # Package and ship the pair
                    break
                print(buffer)
        finally:
            semaphore_x.release()  # Leave critical section

        semaphore_z.release()  # Increment empty slots count
        semaphore_z.release()  # Increment for the second shoe


# Start the producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()