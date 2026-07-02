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

def thread_function(bus: list[int]):

    semaphore.acquire()

    print(f"[{threading.current_thread().name}] started charging")
    for j in range(len(bus)):
        fill_module(bus, j)
    print(f"[{threading.current_thread().name}] finished charging")

    semaphore.release()

    return bus

def threads_buses(n: int):

    bus_instance = bus(n)
    
    thread = threading.Thread(
        target=thread_function,
        args=(bus_instance,)
    )
    return thread

def num_cargadores(k: int):
    global semaphore
    semaphore = threading.Semaphore(k)