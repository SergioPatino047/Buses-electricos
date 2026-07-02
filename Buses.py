from concurrent.futures import thread
import threading
import time


def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

def fill_module(bus: list[int],i:int):
    while bus[i] < 100:
        bus[i] += 50
        print(f"[{threading.current_thread().name}] Bus: {bus}")
        time.sleep(0.8)
    return bus

def thread_function(bus: list[int], barrier: threading.Barrier, semaphore: threading.Semaphore):

    barrier.wait()

    semaphore.acquire()

    print(f"[{threading.current_thread().name}] started charging")

    for j in range(len(bus)):
        fill_module(bus, j)

    print(f"[{threading.current_thread().name}] finished charging")

    semaphore.release()

    return bus

def threads_buses(b: int, n: int, k: int):

    barrier = threading.Barrier(b)
    semaphore = threading.Semaphore(k)

    if b > k:
        bus_list = [bus(n) for _ in range(b)]
        threads_list = []

        for i in range(b):
            thread = threading.Thread(
                target=thread_function,
                args=(bus_list[i], barrier, semaphore),
                name=f"Bus-{i+1}"
            )

            threads_list.append(thread)
            thread.start()

        for thread in threads_list:
            thread.join()
    else:
        print("The number of buses must be greater than the number of charging stations.")

threads_buses(5, 5, 6)
