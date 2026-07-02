from concurrent.futures import thread
import threading
import time


barrier = threading.Barrier(3)


def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

def fill_module(bus: list[int],i:int):
    while bus[i] < 100:
        bus[i] += 50
        print(bus)
    return bus

def chargers(k: int) -> list[int]:
    cargadores: list[int] = [1] * k
    return cargadores

def thread_function(bus: list[int], chargers: list[int]):


    barrier.wait()  
    

    while True:
        for i in range(len(chargers)):
            if chargers[i] == 1:
                chargers[i] = 0
                print(f"[{threading.current_thread().name}] acquired charger {i}")
                for j in range(len(bus)):
                    fill_module(bus, j)
                chargers[i] = 1
                print(f"[{threading.current_thread().name}] released charger {i}")
                return bus
        print(f"No charger available, [{threading.current_thread().name}] is waiting...")
        time.sleep(5)

bus1 = bus(2)
print("Bus 1 modules:", bus1)
bus2 = bus(2)
print("Bus 2 modules:", bus2)
bus3 = bus(2)
print("Bus 3 modules:", bus3)
chargers_list = chargers(1)
print("Chargers:", chargers_list)
thread1 = threading.Thread(target=thread_function, args=(bus1, chargers_list))
thread2 = threading.Thread(target=thread_function, args=(bus2, chargers_list))
thread3 = threading.Thread(target=thread_function, args=(bus3, chargers_list))
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()


