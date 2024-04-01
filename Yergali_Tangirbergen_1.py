from time import sleep
from threading import Thread

# Implementation of Peterson's solution for mutual exclusion
class PetersonsSolution:
    def __init__(self):
        # Flags to indicate whether a process is ready to enter the critical section
        self.flag = [False, False]
        # Variable to keep track of whose turn it is to enter the critical section
        self.turn = 0
        # Shared counter variable to be manipulated by both processes
        self.counter = 10

    # Method for a process to enter the critical section
    def enter_cs(self, process_id):
        # Identify the other process
        other = 1 - process_id
        # Indicate readiness to enter critical section
        self.flag[process_id] = True
        # Declare that it's the other process's turn
        self.turn = other
        # Busy-wait until either the other process isn't ready or it's this process's turn
        while self.flag[other] and self.turn == other:
            pass  # Busy wait

    # Method for a process to exit the critical section
    def exit_cs(self, process_id):
        # Reset the flag indicating readiness to enter critical section
        self.flag[process_id] = False

    # First process logic
    def process1(self, process_id):
        # Enter critical section
        self.enter_cs(process_id)
        # Critical section: manipulating shared counter
        temp = self.counter
        temp += 4
        # Simulate some processing time
        sleep(1)
        # Update shared counter
        self.counter = temp
        # Exit critical section
        self.exit_cs(process_id)

    # Second process logic
    def process2(self, pid):
        # Enter critical section
        self.enter_cs(pid)
        # Critical section: manipulating shared counter
        temp = self.counter
        temp += 2
        # Simulate some processing time
        sleep(1)
        # Update shared counter
        self.counter = temp
        # Exit critical section
        self.exit_cs(pid)

# Instantiate the Peterson's solution object
solution = PetersonsSolution()
# Create threads for each process, targeting their respective methods
thread0 = Thread(target=solution.process1, args=(0,))
thread1 = Thread(target=solution.process2, args=(1,))

# Start both threads
thread0.start()
thread1.start()

# Wait for both threads to finish
thread0.join()
thread1.join()

# After both threads finish, print the final value of the shared counter
print(solution.counter)
