from queue import Queue
import threading
import time

def num_cargadores(k: int):
    global semaphore
    semaphore = threading.Semaphore(k)

def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

def fill_module(bus: list[int],i:int):
    while bus[i] < 100:
        bus[i] += 15
        if bus[i] > 100:
            bus[i] = 100
        print(f"[{threading.current_thread().name}] Bus: {bus}")
        time.sleep(0.8)
    return bus

def thread_function(bus):

    semaphore.acquire()

    print(f"[{threading.current_thread().name}] started charging")
    for i in range(len(bus)):
        fill_module(bus, i)
    print(f"[{threading.current_thread().name}] finished charging")

    semaphore.release()

def threads_buses(num_modules, bus_id):

    bus_instance = bus(num_modules)

    return threading.Thread(
        target=thread_function,
        args=(bus_instance,),
        name=f"Bus-{bus_id}"
    )

def generate_buses(num_modules):
    bus_id = 1
    while True:
        thread = threads_buses(num_modules, bus_id)
        bus_queue.put(thread)
        print(f"[Generator] Bus-{bus_id} arrived.")
        bus_id += 1
        time.sleep(5)  

def dispatcher():

    while True:

        thread = bus_queue.get()
        thread.start()
        bus_queue.task_done()

num_cargadores(5)
bus_queue = Queue()

dispatcher_thread = threading.Thread(
    target=dispatcher,
    daemon=True
)

dispatcher_thread.start()

generate_buses(5)